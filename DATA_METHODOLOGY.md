# Data methodology

## Time and interval conventions

- All timestamps are UTC.
- Each record covers a half-open interval `[start_time_utc, end_time_utc)`.
- From feature version `2.0.0`, file names and `YYYY/MM/DD` partitions are labelled by the interval **start**. Version `1.0.0` used interval-end labels; the two must not be combined by file name. To map a v2 file to its v1 counterpart, add the interval length to the v2 start time, including any UTC date rollover.
- A label is a storage key, not an availability time: an interval's information is complete only at `end_time_utc`.
- The sample dataset is hourly.

## Stateful replay

The proprietary engine replays sequential event data and carries state across interval boundaries within a replayed day. A monthly sample day is not equivalent to a continuous multi-year replay: long-lookback and cross-day features may be unavailable or less reliable at the start of a sample day.

Unavailable values are published as NaN, never filled; there are no nulls. NaN is not zero, and a missing file or instrument row is not zero activity. Integer counts are always defined: a zero count means no qualifying events were recorded in the interval. When the source feed itself has no records for an interval (an exchange outage, maintenance, or a recording gap), counts are zero and price-type values are NaN; such intervals are listed in the README under "Days with limited or no data".

## Quality checks

Before publication, each release is checked for complete interval coverage per module, market, and sample day; readable, non-empty Parquet; schema consistency with the [Feature Catalog](https://github.com/QuantFeatures/FeatureCatalog); and, for version changes, mapped schema and value comparison against the previous version.

## Source and licensing

Features are derived from licensed historical exchange data for Binance, OKX, Bybit, and Hyperliquid. Raw vendor or exchange data is never published.
