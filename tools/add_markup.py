"""Add the markup strokes from a GitHub issue to markups.json.

Run by .github/workflows/markups.yml when an issue titled "[markup] ..." is opened.
Reads the issue body (BODY), author (USER) and number (NUM) from the environment,
takes the first ```json block, checks it, appends it as a batch and writes a reply
to .markup_reply.txt for the workflow to post. Exit code is always 0 so the
workflow can reply either way; "nothing changed" replies leave markups.json alone.
"""
import datetime
import json
import math
import os
import re
import sys

LIMIT = 200_000  # bytes. Past this every earlier batch is erased and the store starts again with the new one.
WALLS = {'B2', 'B2_bulkhead', 'B3', 'Wall1', 'M4', 'B4', 'M7', 'M8', 'East', 'BoxEnd', 'Box', 'M6',
         'WFR', 'WFR_north', 'WFR_south'}
MAX_STROKES, MAX_POINTS = 400, 1500

body = os.environ.get('BODY', '')
user = os.environ.get('USER', 'someone')
num = os.environ.get('NUM', '0')


def done(msg):
    with open('.markup_reply.txt', 'w', encoding='utf-8') as f:
        f.write(msg + '\n')
    print(msg)
    sys.exit(0)


m = re.search(r'```json\s*(\{.*?\})\s*```', body, re.S)
if not m:
    done('No markup data found in this issue. The body needs the ```json block the walkthrough gives you '
         '(the Save button puts it on your clipboard). Nothing was changed.')
try:
    data = json.loads(m.group(1))
except Exception as e:  # noqa: BLE001
    done(f'The markup data is not valid JSON ({e}). Nothing was changed.')

clean = []
for s in (data.get('strokes') or [])[:MAX_STROKES]:
    try:
        wall = str(s['wall'])
        if wall not in WALLS:
            continue
        z = float(s.get('z', 0))
        w = min(1.5, max(0.02, float(s['w'])))
        c = str(s['c'])
        if not re.fullmatch(r'#[0-9a-fA-F]{6}', c):
            continue
        p = [[round(float(a), 2), round(float(b), 2)] for a, b in s['p'][:MAX_POINTS]]
        if not p or any(not (math.isfinite(a) and math.isfinite(b)) or abs(a) > 400 or abs(b) > 40 for a, b in p):
            continue
        if not math.isfinite(z) or abs(z) > 5:
            continue
        clean.append({'wall': wall, 'z': round(z, 2), 'w': round(w, 3), 'c': c.lower(), 'p': p})
    except Exception:  # noqa: BLE001
        continue
if not clean:
    done('No usable strokes in the data. Nothing was changed.')

try:
    with open('markups.json', encoding='utf-8') as f:
        store = json.load(f)
    if not isinstance(store, dict):
        store = {}
except Exception:  # noqa: BLE001
    store = {}
batches = store.get('batches') if isinstance(store.get('batches'), list) else []
batch = {'by': user, 'at': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%MZ'),
         'issue': int(num) if str(num).isdigit() else 0, 'strokes': clean}
batches.append(batch)
store = {'v': 1, 'limit': LIMIT, 'batches': batches}
out = json.dumps(store, separators=(',', ':'))
note = ''
if len(out) > LIMIT:
    store['batches'] = [batch]
    out = json.dumps(store, separators=(',', ':'))
    note = (f' The store had reached its {LIMIT // 1000} KB limit, so every earlier markup was erased and the '
            f'site starts again with just these.')
    if len(out) > LIMIT:
        done('This batch alone is bigger than the whole store limit. Nothing was changed.')
with open('markups.json', 'w', encoding='utf-8') as f:
    f.write(out + '\n')
done(f'Added {len(clean)} stroke(s) by @{user} to markups.json.{note} '
     'The site shows them about a minute after this issue closes; reload the walkthrough.')
