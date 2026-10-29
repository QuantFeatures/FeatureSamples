#!/usr/bin/env python3
"""Read a sample .pqt.gz feature file and print its shape, schema, and first rows.

Usage: python examples/read_pqt_gz.py <file.pqt.gz> [more files ...]
Requires: pyarrow (and pandas for the row preview).
"""
import gzip
import io
import sys

import pyarrow as pa
import pyarrow.parquet as pq


def read_pqt_gz(path: str) -> pa.Table:
    with gzip.open(path, "rb") as f:
        return pq.read_table(io.BytesIO(f.read()))


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    table = pa.concat_tables(read_pqt_gz(p) for p in sys.argv[1:])
    print(f"{table.num_rows} rows x {table.num_columns} columns")
    print(table.schema)
    print(table.slice(0, 5).to_pandas().to_string())


if __name__ == "__main__":
    main()
