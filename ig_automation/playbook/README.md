# Saved Instagram knowledge playbook

## Files this process uses

| Where | What | Access |
| --- | --- | --- |
| `ig_automation/playbook/build_playbook.py` | The builder | code |
| `ig_automation/playbook/prompts/` | Grouping and cleanup instructions sent to the model | code |
| `ig_automation/playbook/tests/` | Offline tests | code |
| `IG/*/*_description.md`, `*_transcript.txt`, `*_ocr.txt` | The saved posts | read only |
| `knowledge_library/` | Everything the builder writes: topics, saved groupings, playbook, logs, cache | written |
| `~/.codex/auth.json` | Codex sign-in, linked into `knowledge_library/.runtime/` | read only |

Nothing else in the project imports or runs this builder, and no timer starts it.

The builder reads every `IG/*/*_description.md` note and the available `*_transcript.txt`
and `*_ocr.txt` files in the same post folder, including carousel audio transcripts.
It first groups the sources into a saved topic library. Only then does it compare
overlapping advice to produce a cleaned playbook with sources and conflicting claims.
It produces English paraphrases, not transcript dumps.
Images and video are not re-analyzed; any knowledge missing from the existing notes and
text evidence remains outside this build. Dated post folders without notes are reported.

The grouping instructions live in [prompts/group_topics.md](prompts/group_topics.md).
This first stage preserves every source and gives each topic a scope, use cases, and
source links. It does not choose winning advice or write the playbook yet. A post may
belong to multiple topics. The saved topic notes are references for a later skill;
they do not install or enable skills.

The exact cleanup request and selection criteria live in
[prompts/clean_playbook.md](prompts/clean_playbook.md). Both batch comparison and the
mandatory final cleanup use that prompt. The final cleanup runs even for a single
batch. It compares drafts from the saved topic groups, chooses the best supported
specific version of overlapping advice, and explains the selection. Duplicate prose
is removed from the playbook; the source files remain accessible in the source index.
If no version has evidence of effectiveness, it labels the best available instructions
as untested instead of claiming that they work.

Everything generated goes under `instagram_saves/knowledge_library/`. This folder is
ignored by Git. The builder does not write into the vault, change original posts, send
chat messages, or install a schedule. Run it manually for now.

## Run

From `/home/homepi/Work/ig/instagram_saves`:

```bash
python3 ig_automation/playbook/build_playbook.py --dry-run
python3 -u ig_automation/playbook/build_playbook.py --stage topics
```

Review `knowledge_library/Topic index.md` and its linked topic notes. Then build the
playbook from that saved grouping:

```bash
python3 -u ig_automation/playbook/build_playbook.py --stage playbook
```

`--stage playbook` requires a saved grouping matching the current notes and evidence.
If posts changed or no grouping exists, it stops and asks for `--stage topics` again.
Before starting that stage, `--stage playbook --dry-run` reports the number of saved topics,
comparison calls, cache hits, uncached calls, and prompt sizes without using a model or
writing files. If all comparisons are cached, it also checks the final cleanup prompt.
A topics dry run reports how many sequential grouping batches can currently reuse cache;
the later keys depend on topic names that have not been produced yet. A real playbook run stops
before its first model call if it needs more than 100 comparison calls. This protects
against a topic library that is too fine grained to review or synthesize economically.
Consolidate its assignments first; `--max-playbook-batches N` changes the limit, and
`--max-playbook-batches 0` removes it when the larger run is intentional. A topics
dry run cannot know the final topic count.
Running with `--stage all` (the default) performs both stages in this order without a
review pause. Neither command is attached to the scheduled download pipeline.

Requires Python 3.9+ on Linux and an authenticated, current `codex` CLI supporting
`--ignore-user-config`, `--ephemeral`, and `--output-schema`. Check authentication with
`codex login status`; the builder reuses it without copying credentials. The default
model is `gpt-6-astra` with `xhigh` reasoning. Calls consume the signed-in account's
Codex usage allowance.

### Claude fallback

If a Codex call fails (usage limit, error, timeout, or an answer that fails validation), the
same prompt and schema are sent to the Claude CLI instead (`claude -p --safe-mode --tools ""`,
so no CLAUDE.md, hooks, MCP, or tools are involved). The default is `claude-sonnet-5-5` at the
same effort as the call it replaces; change it with `--fallback-model` and `--fallback-effort`. Requires an
authenticated `claude` CLI (`claude auth status`); it uses that account's usage.

* A usage limit is detected from Codex's output. Once seen, the rest of that run uses Claude
  without trying Codex again. Other failures retry Codex on the next call.
* Results are cached as before, so rerunning the same command resumes where it stopped.
  Each cached result records which model made it (`producer.json`).
* The playbook header and `status.json` say when Claude produced any results
  (`fallback_calls`, `fallback_cost_usd`, `models_used`).
* To redo Claude made results with Codex once its allowance is back, add `--refresh-fallback`.
* `--no-fallback` restores the old behavior: stop on a Codex failure.
* If Claude also fails, the run stops and names both errors. When the cause is a Claude
  usage or session limit, the error says both models are at their limits and that finished
  calls are cached, so rerunning the same command after the reset continues.
* Every switch is logged. `SWITCH: <from> -> <to> (<effort>). Reason: ...` appears on screen,
  in `knowledge_library/build.log`, and in `status.json` under `switch_events`. After the first
  usage limit switch, later calls print a short "Using <fallback> for this call" line.
* Each fallback call logs the Claude spend for this run and the total across runs, kept in
  `knowledge_library/fallback_spend.json`. `--max-fallback-cost` (default 5 USD, 0 means no
  cap) applies to that total, so rerunning does not grant a fresh allowance; a run that starts
  at or over the cap stops before calling Claude. The call that crossed the cap is cached
  first, so a rerun does not pay for it again. `--reset-fallback-spend` starts the total
  again from $0. The figure is the CLI's reported cost.

The model receives supplied text through stdin and runs with a read-only sandbox,
command tools and web search disabled, personal config ignored, and apps disabled.
The Python parent validates results and writes output. Codex runtime databases and
logs are directed into `knowledge_library/.runtime/` using supported per-command
settings; global configuration and authentication files are not changed.

### Cheaper topic grouping

Sorting posts into topics is simpler than choosing the best advice, so grouping uses its
own settings: `--group-effort` (default `medium`), optionally `--group-model` for Codex and
`--group-fallback-model` for Claude (for example `claude-haiku-5-5`). The playbook calls and
the final cleanup keep `--effort` (default `xhigh`). Cache keys include model and effort, so
changing the grouping effort makes earlier grouping results unusable; to reuse results made
at the old setting, pass `--group-effort xhigh` (and `--model-merge` if they came from the
older flow below).

### Shared topic list instead of a merge call

Grouping batches run one after another. Each batch is shown the topics created so far and is
told to reuse an existing topic's exact slug and name when a post fits it. The topic lists are
then joined in plain code (same slug or same normalized name becomes one topic; sources and
use cases are combined), validated, and written. No model call merges them.

* Trade-off: a later batch's cache depends on the batches before it. Changing early batches
  re-runs the ones after. Hash buckets still keep a new post from touching unrelated buckets
  on the first pass, but a changed bucket re-runs everything after it.
* The old model based merge, which could also split overbroad topics, remains available with
  `--model-merge`. That mode uses the older independent batches and its cached results.
* Topic names are only as consistent as the batches make them, so check `Topic index.md` for
  near duplicates before running the playbook stage.

## Output

| File | Purpose |
| --- | --- |
| `Topic index.md` | First-stage topic library; browse this before building the playbook |
| `topics/<slug>/Sources.md` | Topic scope, possible skill use cases, and links to all its sources |
| `topics.json` | The active topic grouping and the input fingerprint for the later playbook stage |
| `groupings/<name>.json` | Every saved grouping (same format), reusable with `--stage playbook --grouping <name>` |
| `fallback_spend.json` | Running total of Claude fallback spend that `--max-fallback-cost` checks |
| `Instagram playbook.md` | One document, grouped by topic, with selected/merged source links and contradictions |
| `Source index.md` | Every reviewed post, its local note, and why it was selected, merged, or excluded |
| `playbook.json` | The validated structured content used to render both notes |
| `status.json` | Current or last run status, completed batches, model, errors, totals, and `switch_events` |
| `build.log` | Timestamped log of calls, cache reuse, model switches, and fallback spend |
| `runs.jsonl` | Appended run history |
| `.cache/` | Content-addressed prompts, model responses, validation results, stdout/stderr logs |
| `.runtime/` | Local Codex runtime state and logs |

The topic library is saved before any playbook call begins. If later synthesis fails,
the topic library remains usable for skill preparation. `--stage topics` returns
`topics_complete` in `status.json`; it never creates or updates a playbook.
The three final playbook outputs appear only after every synthesis result passes validation.
Each file is replaced atomically; the three files are not a single filesystem transaction.
A failed model call leaves the prior successful playbook in place. `status.json` records
the failure and the error gives the relevant log paths. There are no automatic retries.
Press Ctrl+C to stop; the active model process group is terminated.

## How subsequent runs work

1. Scan the saved notes and evidence; no content is silently truncated.
2. Group sources in bounded batches, normalize the topic names across all batches, and
   save the topic library. Stable hash buckets allow unchanged grouping batches to be reused.
3. For the playbook stage, draw inputs from the saved topics. Large topics are divided
   into bounded batches. Source files and raw text are read again as evidence; grouping
   summaries are not substituted for the full inputs.
4. Reuse completed, validated calls whose full input, prompt/schema, and model settings
   match. Changes to topic assignments or evidence invalidate affected synthesis calls.
5. Always finish with a final cleanup that merges overlaps and finds contradictions
   across topics, including runs with just one topic/batch. When the drafts are larger
   than `--cleanup-bytes` (default 200,000), neighbouring drafts are first merged in parts,
   then the parts are merged, until one final call takes them all.
6. Require every source to be accounted for and all citations to refer to known source IDs.
   Reject literal duplicate entries and any result that drops the opposing source sides
   of a previously identified contradiction. These are structural checks; a human review
   is still needed to assess whether the claims and their comparisons are accurate.
7. Update the playbook and source index; append a run-history entry.

The topic stage manages only `Sources.md` inside each topic folder. Other files you
add there are preserved. Old topic folders are retained rather than deleted; the
current `Topic index.md` and `topics.json` identify the active groups.

After grouping, if there are more than `--max-topics` topics (default 60, 0 keeps all),
a grouping-effort call merges fragments and synonyms into broader topics. It names which
earlier topics each new one absorbs, and the sources are joined in code, so no post can be
lost. Each topics run is saved as `groupings/<name>.json` (`--grouping NAME`, default the
date and time) and becomes the active grouping. `--list-groupings` lists them;
`--stage playbook --grouping NAME` builds from an earlier one and makes it active again.
A saved grouping is rejected as stale once the posts or their evidence change.

Run the same command again to resume after an interruption. A completely unchanged run
reuses the final synthesis too. The default per-call timeout is 1,800 seconds. Input
budgets are measured in UTF-8 bytes, not exact model tokens: 240,000 per source batch,
700,000 per synthesis prompt. If a budget is exceeded the build stops with cached work
intact instead of silently dropping evidence. Use `--help` for configurable limits.

"Specific instructions" means usable directions were found in a source; it does not
mean we tested them. Creator-reported outcomes and unsupported claims are labeled.
Source-coverage checks detect missing IDs and invented citations, but they cannot prove
that every paraphrase or merge decision is correct. Review the first generated playbook
before relying on it. The build does not verify current software features, pricing,
health, financial, or legal claims against external sources.

The CLI integration follows the official [non-interactive guide](https://learn.chatgpt.com/docs/non-interactive-mode)
and [configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference).

## Offline checks

```bash
python3 -m unittest discover -s ig_automation/playbook/tests -p test_build_playbook.py -v
```

These exercise source coverage, carousel evidence inclusion, output links, cache reuse
and invalidation (including prompt edits), mandatory final cleanup, contradiction
preservation, duplicate rejection, failure preservation, dry-run behavior, and destination restrictions.
They also verify that grouping precedes synthesis, topics-only runs stop before the
playbook, playbook-only runs reuse saved assignments, and stale/missing topic libraries
are rejected. Topic coverage and safe folder names are checked before publication.
The fake CLI fixture makes no network or model calls.

## First live run: blocked by this session's filesystem permissions

The inventory on 2026-10-15 found 996 notes, 1,795 transcript/OCR files, and one dated
post folder without a note, split into 17 batches. The first live build stopped before
model inference: Codex initialization attempted to open `/home/homepi/.codex/installation_id`
for writing, but this agent session mounts that directory read-only. Redirecting the
supported database/log locations did not remove that installation-file requirement.
No successful model batch or final playbook has been generated yet. No filesystem
permissions were changed. Start the command above in a normal terminal on the Pi;
the live result will still depend on model access and the account's remaining usage.
