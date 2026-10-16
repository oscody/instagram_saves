# Saved Instagram knowledge playbook

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
python3 ig_automation/build_playbook.py --dry-run
python3 -u ig_automation/build_playbook.py --stage topics
```

Review `knowledge_library/Topic index.md` and its linked topic notes. Then build the
playbook from that saved grouping:

```bash
python3 -u ig_automation/build_playbook.py --stage playbook
```

`--stage playbook` requires a saved grouping matching the current notes and evidence.
If posts changed or no grouping exists, it stops and asks for `--stage topics` again.
Running with `--stage all` (the default) performs both stages in this order without a
review pause. Neither command is attached to the scheduled download pipeline.

Requires Python 3.9+ on Linux and an authenticated, current `codex` CLI supporting
`--ignore-user-config`, `--ephemeral`, and `--output-schema`. Check authentication with
`codex login status`; the builder reuses it without copying credentials. The default
model is `gpt-6-astra` with `xhigh` reasoning. Calls consume the signed-in account's
Codex usage allowance. It does not fall back to another model automatically.

The model receives supplied text through stdin and runs with a read-only sandbox,
command tools and web search disabled, personal config ignored, and apps disabled.
The Python parent validates results and writes output. Codex runtime databases and
logs are directed into `knowledge_library/.runtime/` using supported per-command
settings; global configuration and authentication files are not changed.

## Output

| File | Purpose |
| --- | --- |
| `Topic index.md` | First-stage topic library; browse this before building the playbook |
| `topics/<slug>/Sources.md` | Topic scope, possible skill use cases, and links to all its sources |
| `topics.json` | Canonical topic assignments and the input fingerprint for the later playbook stage |
| `Instagram playbook.md` | One document, grouped by topic, with selected/merged source links and contradictions |
| `Source index.md` | Every reviewed post, its local note, and why it was selected, merged, or excluded |
| `playbook.json` | The validated structured content used to render both notes |
| `status.json` | Current or last run status, completed batches, model, errors, and totals |
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
5. Always compare all topic drafts together in a final cleanup to merge overlaps and
   find contradictions across topics, including runs with just one topic/batch.
6. Require every source to be accounted for and all citations to refer to known source IDs.
   Reject literal duplicate entries and any result that drops the opposing source sides
   of a previously identified contradiction. These are structural checks; a human review
   is still needed to assess whether the claims and their comparisons are accurate.
7. Update the playbook and source index; append a run-history entry.

The topic stage manages only `Sources.md` inside each topic folder. Other files you
add there are preserved. Old topic folders are retained rather than deleted; the
current `Topic index.md` and `topics.json` identify the active groups.

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
python3 -m unittest discover -s ig_automation/tests -p test_build_playbook.py -v
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
