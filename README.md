# AI Infrastructure Deal Database

A structured database of the power purchase agreements, M&A transactions, and financing structures behind the AI infrastructure buildout. Maintained as independent research; the analytical companion to my essay [The Moat Moved Downstairs](https://toluwalaseayeni.substack.com/p/the-moat-moved-downstairs) and its [interactive deck](https://deal-data-file-creat-u1eu.bolt.host/).

## What this is

Every deal in here is sourced from company press releases, SEC filings, and primary reporting. The database tracks three layers of the market:

- **ppa_deals**: power purchase agreements and generation deals serving hyperscaler demand (grid connected and behind the meter)
- **ma_deals**: corporate M&A consolidating power generation
- **financing_deals**: the JV, lease, and credit structures financing AI campuses

## Data integrity conventions

Every capital cost figure carries a provenance tag, because the difference between a disclosed number and an analyst estimate is the difference between evidence and opinion:

| Tier | Meaning |
|---|---|
| disclosed | Company stated the figure directly |
| computed from disclosed figures | Calculated from company stated inputs (e.g. $27B / 2GW) |
| analyst imputed | Third party estimate; flagged with source and range |
| not disclosed | No reliable figure exists; left blank, never guessed |

## Example queries

**Capex per kW, generation vs data center** (the essay's core chart):

```
name                    asset_class   capex_per_kw   provenance
Hyperion JV             data center   13,500         computed from disclosed figures
Hyperion 5GW expansion  data center   10,000         computed from disclosed figures
Justified Data lease    data center    9,975         analyst imputed
Project Kilby           generation     3,333         analyst imputed
Clearway portfolio      generation     2,051         disclosed
```

**Contracted duration** (how many years of the physical layer are locked up): three deals at 20 years, one at 15, and Hyperion's 4 year lease sitting on a 16 year residual value guarantee.

**M&A buyer mix**: Strategic buyers, 3 deals, $85.6B of equity value. Financial buyers, 2 deals, $13.3B. The utilities and IPPs are consolidating bigger; the infra funds are buying platforms.

**The credit support register**: every financing structure and who stands behind it, from Meta's residual value guarantee to the undisclosed investment grade supporter behind the Anthropic TeraWulf lease.

All five queries are in `queries.sql`.

## Files

- `deals.db`: the SQLite database
- `deal_data.json`: the source data (edit here, rerun the loader)
- `load_database.py`: rebuilds the database from the JSON
- `queries.sql`: the analytical queries

## Watch items

Open questions the database is waiting to record: how the ~$23B Hyperion expansion gets financed; who supports the TeraWulf lease (WULF filings); Meta's 10-K treatment of the JV.

---

*Toluwalase Ayeni | Duke MBA | [Substack](https://toluwalaseayeni.substack.com) | Independent research, not investment advice.*
