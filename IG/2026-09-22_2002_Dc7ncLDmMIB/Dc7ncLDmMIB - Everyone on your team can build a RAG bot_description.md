---
shortcode: "Dc7ncLDmMIB"
url: "https://instagram.com/p/Dc7ncLDmMIB/"
type: "Carousel"
author: "datasciencebrain"
shared: "Sep 22, 2026, 08:02 PM"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Repairing stale agent memories: a 20-file guide

A carousel promoting a written project guide for a memory agent that tracks when facts were true versus when they were believed, and detects and repairs stale facts. The slides show the guide's cover, table of contents, mental model, architecture diagram, and setup commands.

Written by claude-haiku-5-5.

## What it teaches

1. Store each memory as an interval with a belief attached, keeping valid time (when the fact was true) separate from transaction time (when the system believed it).
2. Never delete a memory. Close its validity window instead.
3. Classify every change as one of four operations: born (opens, no end), replaced (closes where its successor opens), ages (stays open, belief weakens, flagged), or ends (closes, nothing succeeds it).
4. Run two paths into one writer: an arrival path that extracts, classifies and applies policy when the user speaks, and a timed sweep that finds stale facts when nobody has said anything.
5. Make the repair module the only file that changes rows, so every rule and audit entry lives in one place.
6. Detect stale facts with SQL and file reads, so a sweep with no drift makes no model calls.
7. Send low-confidence repairs to a human review inbox instead of applying them automatically.
8. Build bottom-up, with config and clock first, then store, embed and recall, cache and LLM calls, extract, classify, policy and repair, detect, propose and sweep, graph nodes, and finally the demo, CLI and inbox.
9. Verify that the sqlite-vec extension loads before writing a schema around it.
10. Create the project with uv, add the listed dependencies, and put the Groq API key in a .env file as GROQ_API_KEY.
11. Inject a clock object so tests can run with a frozen time.
12. Write the success criterion for an ablation before running it, then measure which mechanisms actually changed answers.

## Source

* How to get it: The full guide PDF is shared only with Instagram subscribers via the subscribe button on the profile (paid membership). Not sent by comment or DM.

## Caption

Everyone on your team can build a RAG bot.

Almost nobody can answer this:

"What happens to that memory in six months?"

That question is the gap between a demo and a system. And it is the one interviewers reach for when they want to find out if you have actually shipped something.

I built the answer as a full project.

→ Two time axes - when a fact was TRUE vs when you BELIEVED it
→ Nothing is ever deleted, only closed
→ Four detectors that find stale facts with zero model calls
→ A human gate for repairs the agent shouldn't make alone
→ An ablation with a criterion written down BEFORE the run

And the honest part most write-ups skip: two of my own mechanisms came back null. Keeping history changed no answer on the present. I published that instead of hiding it.

Free Groq. No credit card. 20 files.

A PDF Version of the complete Guide is shared with our Exclusive Instagram Subscribers 👑. Get access to it with 1000+ other FREE Resources for just Rs.45 per month❗️. Click subscribe button in profile to access it now!

Follow @datasciencebrain for daily AI notes 📝,tips ⚙️ and interview Q&A 🎯

.
.
.
.
.
.
[dataanalytics, artificialintelligence, deeplearning, bigdata, agenticai, aiagents, statistics, dataanalysis, datavisualization, analytics, datascientist, neuralnetworks, 100daysofcode, llms, datasciencebootcamp, ai]

#genai #aiengineer #datascience #pythonforai #aicareers

## On screen text

GDATASCIENCEBRAIN
SWIPETO KNOW MORE
Memories
reated by@datasciencebrain
MESSA
slen decy
INBO
on 3.12, Windows.
2.13.5.Pyth
How to read this guide
projects
ssumes this one worked.
holding up.
ue y then youwnot need
s commentary be
eca
Table of Contents
. What you're building
2. The mental model
3. Architecture
4.Setup
.conisyeverynb noneplace
.clockpyhecockcomesfirt
store.py - two time axes
the one place rows change
18.inbox.py -the review UI
19.Run it end to en
o.rovingheep ea pac
rors and fixes
22.What to build next
1.What you're building
ork inMarch stays anwera
changed,wndows that closed
andseparatelaiis sys
believed for a str
Picture one fact ona timeline:
Feb
now
valid time
was true Feb-Jun
hat happens
the interval
tillretrieved?
example
live in Pune
pens, no end
yes
born
cosesoxay where  suceso
no  the successor
l moved to Bengaluru
replaced
opens
nobodymentoned he carin eight
yes, flagged
stays open, belief weakens
ages
months
closes,nothing succeeds it
he dentist eppoinenthappened
ends
Look closer.Replaced and
The two paths
o.sorce chandwndow c
3.Architecture
one place to enf
hicr
ea
ns
nweepaable onareeti
Build order, and why
you can...
layer
move time by hand
5-6
config, clock
store
retrieve i with ts age atached
embed, recall
cal amodel without ever raising
cache, lm
10-12
detect propose, Swep
ind rot nobodyreported
13-14
park adecision for a human
15-16
nodes, graph, turn
arive n alfroacandabrwser
17-18
Seed, main, inbox
v t nenryedicyhon.
cd memory-medic
ntics=2.13.4
anggrephcheckpointsqu
GRoo APKEY-gk yourkey here
m main.py
touch src/init_.py
eryouhvewnchea aoun
fetchone()
.conyveynobinene place
If-lives, rate limits.S
changing
Inputs:
import annotations
future
from
import os
import sys
from pathuib import Path
rom dotenv mpor lad otenv
resolve parent parent
ROT_DIR=Path(file
DATA DIRROOTDIR
data"
SOUREDIATADROU
OUTUTDIRROTDIROUEPUE
# On Windows uv run
Load dotenv ROoIR/nv
Maostou survivemodoutut.
for stream in (s
(ysstdout,Sysstderr
I harenecnfoure
force_utff_console(
OUPUR. Tre
des emit typographic p
ctuatior
hatever line happenec
a bug in your display code.
Naethefies the proectwrites.
Paths
heckpoints.db"
OUTPUT_DIR/
cache.sglite"
CACHE_PATH
OUTPUTDIR
ledger.sqlite"
LEADERBOARD_PATH
UTUTDIReaderboardmd
Models
chema
son
EXTRACTMODEL
nai/gpt-
openai/gpt-oss-2ob)
n equally and can
doubles what a day affords.
Generation
TEMPERATURE
REASONINGEFFORTLOW
en eson bee c
ds complet
gp
# JSoN. Starved, it
returns
400
schema bug and
s not one
AX COLEOOEN
256
TOKENSPERMINUTEO00
REQUESTS_PERMINUTE
REQUESTSPERDAY O0O
publishes
TPD_PER_MODELTrUe
MAX_CONCURRENCY
REOUEST_SPACING_ 1.0
MAXRETRIES4
OPENEND 253402300799
DIMS
RECALL_K8
SOLITE_TIMEOUT0.0
iS nOIS NULL.
they drift apart.
civeachkindctheli.
hidde
#slow:
people cha
thre
roughly he
fast:
d by valid to, not by age.
HALFLIFE_DAYS
"stable"
fast:30}
365
time.0.5 is
utofdate"
resh
may
read
lowthi
ner
urabl
rompt and the swec n open
everythingis a
FRESH_FLOOR0.
0.60
ostof
AUTOAFLYMINCONIDEE.
QUALIFYMIN CONIDENCE
CONFIRMMIN CONFIDENCE
# A contradiction
extraction err
STABLE ALWAYS PARKS
async
hat
never pair.
# share few words
SCOPE SIM_THRESHOLD
9
EVIDENCEMAXCHARS1500
MAX REVISIONS
ddingit
Behaviour Switches
bitemporal")
GATE_ENABLED
SgtenVGATEENABLED
SWEEP_ENABLED
o ateeptyyen coc
os .getenv
CLOCK_AT
PROMPT_VERSION
EXTRACT SCHENAVERSIONVI
RELATION SCHEMA_VERSION
v1
JUDGE PROMPT_VERSION
ku-vl
STORE_VERSION
Faepuywneky sg.
dereultspathodelstr
>Path:
Per-model
turn OUTPUT_DIR
.json"
de requireepikeyOstri
strip
if not key:
raise SystemExit(
GROQ APIKEY=gsk
eturn key
.cocyhe clockcoert
six months.How
injecting a clock
cost
future_import annotations
mport time
rom typing import Protocol
de toepochiotint
00:00
text
if len(text)
else:
if parsed.tzinfo is
arsed
date only:
True
boo
Epoch seconds
S
X
nnt
etuonnt eofot
The baredatebranchaters e
Meaurianchday scon
def daysbetween later:
int, earler int loat:
"Fractional days from
earlier
heets a live cloci
class Clock(Protocol):
hat can say what now
is, in epoch seconds.
def now(self) > int:
def today(self str:
class Systemclock:
frozen  False
def now(selfs int:
return int(time.time)
return to_iso(self.now
ive he cleracock hey canmove.
class Frozenclock:
lock he cer oves by hand
watch  fastmoving act go
in June
advance(days
5180
frozen  True
self._epoch
def now(self)> int:
etu
def today(self)s str
return to_isoself._epoch
ion
None:
int0
fuses to go backwards
bitemporal
tiedaysday
f delta
n
self._epoch += delta
->Clock:
make_clockat:
def
eturn FrozenClock(at)
t.srie sytencock
an intervalwith negative
uv run pythonc
print('start
.today(
vance(days=180)
print('gap
7.store.py -two time axes
romuturempor otations
import json
import sqlite3
import sqlite_vec
from sre import config
OPENENDCOn1g.OPENEND
STATE
SCHEMA
INTEER PRINARY KEY AUTOINCRENENT
user_id
NOT NULL
NOT NULL DEFAULT
scope
NULL
value
rolatility
scheduled',
confidence
REAL
INTEGER NOT NULL,
alid_from
NTECERNOT LL DEAULTOPEEND
validto
INTEGERNOT NULL
recorded_at
expired_at
INERREEENES O
Superseded_by
rdonveon
NULLCHECK
NOT
ur
human'
Source_ref
source_hash
ast_verified_at I
INTEGER NOT
JUL
status
superseded','expired
REATEINDE INOEXITS EY
column
axis
means
vatid_fromvaid_to
hen the tacwas true in thoword
recorded_at expered_et
last_verified_ar
neithe
separately?
backwards.
cope wrong caused three se
Ad provennceand the auditlog.
RETABLENTEXISSU
TEXT PRIMARY KEY
ource_ref
sha256
TEXT NOT NULL
content
INTEGER NOT NULL
fetched_at
LekeNERNNULL
REETABLE NIS
NTEGR PRIMARY KEV AUTNCREET
id
topic
TEXTN
NULLDEFAULT
p
detector
radiction
policy
NTEGER
new_id
before_json
after_jsor
NULL DEFAULT
evidence
eason
fidence
conf
DEFAULT0.
routed
ided_by
dedby
parked','applied
tat
thread_id
Propoedt INTEERNOT NULL.
INTEGER
decided_at
CREATE
XISTS
NDEX
proposed_at;
pairs
ON repairs(old_id)
INDEX
leted and th
cide
parked toapplied
CREATE TABLEIF NOT EXISTS
TEXT PRIMARY KEY,
VaLUe TEXT NOT NULL
REATEVEN ITS
proposeda
VEC_SCHEMA
INTEGER PRIMARY KE
memory_id
embedding
TEXT PARTITION KEY
INTEGER,
valid_to_epoch
Threedesignchoices in six ines:
SI
reirdneny sae
e vector
sqlite.Connection:
def connect(path-None)
conn= sqlite3.connect(
isolation_level-None,
conn.rowactory sute Row
tensionTrue
sqlite_vec.load(conn
enable_oad_xtension(False
conn.
Sy_timeout=30000
exeeRArtoney
onn
conn.xecutescriptSEA
eturn conn
connection
we arwetoboth tabes atonc.
dict  None:
onuped ao anut ro
eturn dict(row)
row is not None else None
ie
int:
its vector.
rt on
columns
superseded_by",
valid from'
valid to
recordedat"
last verified at"
source_kind",
"status
placeholders
join? for
in columns)
conn.execute
enoryd intur latrowid
epoch, validto_epoch)
VALUES...7.,,
fields[user_id"]
return memory_id
O
if not changes:
changes values
nemori
retur
ow
.fetchone
id)
Physically ren
Only the
memory_id,
the recommended path cals it.
at: int
forever
Stays retrievable
ctive
needs_verification'
istAnyueid,topie
params
if window:
params +=[at, at
Sq.ppendANDscope
Want Complete Version?
Note areshared asPDFwith
Exusivontar subsribe
With tooo+ other Resourcos.
How to get them
nurxusivesrerche
Followi..
Message
Subscribe
@DATASCIENCEBRAIN
