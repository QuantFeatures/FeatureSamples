#!/usr/bin/env python3
"""Inspect synthetic sample CSV using only Python standard library."""
import csv, sys
from pathlib import Path
path=Path(sys.argv[1] if len(sys.argv)>1 else 'data/synthetic/feature_preview.csv')
with path.open(newline='',encoding='utf-8') as f:
 rows=list(csv.DictReader(f))
print(f'{len(rows)} rows; columns: {list(rows[0]) if rows else []}')
for row in rows[:3]: print(row['interval_start_utc'],row['instrument'],row.get('trade_count'))
