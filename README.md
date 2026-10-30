# QuantFeatures Sample Dataset

**Research-ready, interval-based features derived from licensed historical crypto market data. These samples are hourly; datasets are delivered at the interval you choose, from 1 minute to 3 hours.**

This repository distributes a sample of the QuantFeatures dataset: interval-based indicators and summary features computed from trade, top-of-book, funding, open-interest, and liquidation feeds on Binance, OKX, Bybit, and Hyperliquid. The feature engine itself is proprietary and is not included.

## What is included

| Venue | Markets | Instruments | Modules | Sample days |
| --- | --- | --- | --- | --- |
| Binance | Spot and perpetual | BCH, BNB, BTC, ETH, XRP against USDT | 19 | 2019-12-01 to 2026-10-01 |
| OKX | Perpetual (USDT-margined) | BCH, BNB, BTC, ETH, HYPE, XRP | 17 | 2020-01-01 to 2026-10-01 |
| Bybit | Perpetual (USDT-margined) | BCH, BNB, BTC, ETH, HYPE, XRP | 17 | 2020-06-01 to 2026-10-01 |
| Hyperliquid | Perpetual (USDC-settled) | BCH, BNB, BTC, ETH, HYPE, XRP | 15 | 2024-11-01 to 2026-10-01 |

| Attribute | Sample dataset |
| --- | --- |
| Sample days | First UTC day of each month within each venue's range |
| Modules | See the [Feature Catalog](https://github.com/QuantFeatures/FeatureCatalog). `QuoteGradient` and `TradeRank` are Binance only; `LiqFlow` and `LiqStats` are not published for Hyperliquid. Funding, open-interest, and liquidation modules cover perpetuals only. |
| Interval | 1 hour for the samples, 24 files per module, market, and sample day (delivered datasets: 1 minute to 3 hours) |
| Feature version | `3.0.0` (files labelled by interval start; module names are the module ids, and OKX quantities are in coins) |
| Format | Parquet, gzip-compressed as `.pqt.gz` |

Each file holds one row per instrument for one interval. An instrument appears from its first sample day on its venue: OKX BNB from 2023-01-01 and HYPE from 2025-03-01; Bybit ETH from 2020-11-01, BCH from 2021-01-01, XRP from 2021-06-01, BNB from 2021-07-01, and HYPE from 2025-01-01; Hyperliquid HYPE from 2025-01-01.

## Layout

```text
data/features/<module>/eod/3.0.0/<exchange>/<spot|perp>/usdt/1h/YYYY/MM/DD/<module>-<exchange>-<spot|perp>-usdt.YYYYMMDD.HHMMSS.pqt.gz
```

`<module>` is the module name, for example `TradeFlow`. `<exchange>` is `binance`, `okx`, `bybit`, or `hyperliquid`. Every venue uses the same schema for a given module. For Hyperliquid, the `usdt` path segment and the `quote` column are a fixed label: Hyperliquid perpetuals settle in USDC.

`YYYY/MM/DD` and `YYYYMMDD.HHMMSS` are the UTC **start** of the interval. For example, `TradeFlow-binance-perp-usdt.20261001.230000.pqt.gz` covers `[2026-10-01 23:00, 2026-10-02 00:00)` UTC. Its information is complete only at the interval end (`end_time_utc`); use that column to avoid look-ahead bias.

## Quick start

```bash
pip install pyarrow pandas
python examples/read_pqt_gz.py data/features/TradeFlow/eod/3.0.0/binance/perp/usdt/1h/2026/10/01/TradeFlow-binance-perp-usdt.20261001.230000.pqt.gz
```

Or directly in Python:

```python
import gzip, io
import pyarrow.parquet as pq

with gzip.open(path, "rb") as f:
    table = pq.read_table(io.BytesIO(f.read()))
df = table.to_pandas()
```

`data/synthetic/feature_preview.csv` is a small fabricated preview kept for documentation; it is not market data. Inspect it with `python examples/inspect_csv.py`.

## Days with limited or no data

Exchanges and data recorders have outages, maintenance windows, and late listings, so some sample intervals have little or no source data. In these intervals price-type values are NaN and counts are zero, as described in [DATA_METHODOLOGY.md](DATA_METHODOLOGY.md).

| Venue | Modules | Day(s) | Instruments | Intervals without source data (UTC hour starts) |
| --- | --- | --- | --- | --- |
| Binance | `OpenIntBasic`, `OpenIntPlus`, `OpenIntGradient` | 2019-12-01 to 2020-05-01 | All | All: the source carries no open-interest values before 2020-06-01 |
| Hyperliquid | `FundingRate`, `OpenIntBasic`, `OpenIntPlus`, `OpenIntGradient` | 2024-11-01 | All | All except 00 and 21 |
| Hyperliquid | same | 2024-12-01 | All | All except 00, 02, 06, 15, 21 |
| Hyperliquid | same | 2025-01-01 | All | All except 00, 04, 13 |
| Hyperliquid | same | 2025-02-01 | All | All except 00 |
| OKX | Trade modules and `QuoteBasic` | 2020-01-01 | BCH | 21 |
| OKX | `LiqFlow`, `LiqStats` | 2020-01-01 to 2020-12-01 | All | All: no liquidation records exist for these days, so zero counts here mean no data, not no liquidations |
| Bybit | `LiqFlow`, `LiqStats` | 2020-06-01 to 2020-10-01, and 2020-12-01 | All | All: no liquidation records exist for these days |

## Documentation

The [Feature Catalog](https://github.com/QuantFeatures/FeatureCatalog) is the canonical reference for definitions and schema semantics:

- [Data dictionary](https://github.com/QuantFeatures/FeatureCatalog/blob/main/docs/DATA_DICTIONARY.md)
- [Data specification](https://github.com/QuantFeatures/FeatureCatalog/blob/main/docs/DATA_SPECIFICATION.md)
- [Coverage](https://github.com/QuantFeatures/FeatureCatalog/blob/main/docs/COVERAGE.md)
- [Methodology](https://github.com/QuantFeatures/FeatureCatalog/blob/main/docs/METHODOLOGY.md)
- [Module definitions](https://github.com/QuantFeatures/FeatureCatalog/tree/main/docs/modules)

See also [DATA_METHODOLOGY.md](DATA_METHODOLOGY.md), the record schema in `schemas/`, and the release manifest template in `manifests/`.

## Related repositories

- [Feature catalog](https://github.com/QuantFeatures/FeatureCatalog)
- [Organization profile](https://github.com/QuantFeatures/.github)

## Partnership opportunities

Data vendors: co-branded historical feature datasets and customer-hosted live integration; quantitative teams: evaluate indicator families and request coverage. Contact [QuantFeatures@gmail.com](mailto:QuantFeatures@gmail.com).

## Rights and disclaimer

The published files are derived hourly features; no raw vendor or exchange data is included, and nothing here grants rights to underlying market data. See [LICENSE.md](LICENSE.md) for usage terms. Not investment advice.
