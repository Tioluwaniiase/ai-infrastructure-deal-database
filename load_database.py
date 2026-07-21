"""
Builds deals.db (SQLite) from deal_data.json.

Usage: python load_database.py
Rebuilds the database from scratch on every run: edit deal_data.json, rerun, done.

Provenance taxonomy applied to every capital cost figure:
disclosed / computed from disclosed figures / analyst imputed / not disclosed.
"""
import json
import os
import sqlite3

DB = "deals.db"
SOURCE = "deal_data.json"


def provenance(capex_flag, capex_per_kw):
    flag = (capex_flag or "").lower()
    if flag.startswith("disclosed"):
        return "disclosed"
    if flag.startswith("imputed"):
        return "analyst imputed"
    if flag.startswith("not disclosed"):
        return "not disclosed"
    if capex_per_kw is not None:
        return "computed from disclosed figures"
    return "not disclosed"


def buyer_category(buyer_type):
    t = buyer_type or ""
    if t.startswith("Strategic"):
        return "Strategic"
    if t.startswith("Financial"):
        return "Financial"
    return "Other"


def main():
    with open(SOURCE) as f:
        data = json.load(f)

    if os.path.exists(DB):
        os.remove(DB)

    con = sqlite3.connect(DB)
    cur = con.cursor()

    cur.executescript("""
        CREATE TABLE ppa_deals (
            id INTEGER PRIMARY KEY, name TEXT NOT NULL, parties TEXT, announced TEXT,
            deal_type TEXT, structure TEXT, market TEXT, capacity_gw REAL, capex_b REAL,
            capex_per_kw REAL, capex_flag TEXT, provenance TEXT, term_years INTEGER,
            implied_ppa_price REAL, annual_energy_twh REAL, implied_capacity_factor REAL,
            first_power TEXT, status TEXT, note TEXT
        );
        CREATE TABLE ma_deals (
            id INTEGER PRIMARY KEY, name TEXT NOT NULL, announced TEXT, acquirer TEXT,
            target TEXT, structure TEXT, equity_value_b REAL, enterprise_value_b REAL,
            premium REAL, buyer_type TEXT, buyer_category TEXT, status TEXT,
            expected_close TEXT, rationale TEXT
        );
        CREATE TABLE financing_deals (
            id INTEGER PRIMARY KEY, name TEXT NOT NULL, parties TEXT, announced TEXT,
            tenant TEXT, capital_partners TEXT, structure TEXT, debt_b REAL, equity_b REAL,
            total_b REAL, asset_value_b REAL, contracted_revenue_b REAL,
            rent_per_mw_year_m REAL, capacity_gw REAL, capex_per_kw REAL, capex_flag TEXT,
            provenance TEXT, lease_term_years INTEGER, credit_support TEXT, location TEXT,
            status TEXT, note TEXT
        );
    """)

    for d in data["ppaDeals"]:
        cur.execute(
            "INSERT INTO ppa_deals (name, parties, announced, deal_type, structure,"
            " market, capacity_gw, capex_b, capex_per_kw, capex_flag, provenance,"
            " term_years, implied_ppa_price, annual_energy_twh, implied_capacity_factor,"
            " first_power, status, note) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (
                d["name"], d.get("parties"), d.get("announced"), d.get("type"),
                d.get("structure"), d.get("market"), d.get("capacityGW"), d.get("capexB"),
                d.get("capexPerKW"), d.get("capexFlag"),
                provenance(d.get("capexFlag"), d.get("capexPerKW")),
                d.get("termYears"), d.get("impliedPPAPrice"), d.get("annualEnergyTWh"),
                d.get("impliedCapacityFactor"), d.get("firstPower"), d.get("status"),
                d.get("note"),
            ),
        )

    for d in data["maDeals"]:
        cur.execute(
            "INSERT INTO ma_deals (name, announced, acquirer, target, structure,"
            " equity_value_b, enterprise_value_b, premium, buyer_type, buyer_category,"
            " status, expected_close, rationale) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (
                d["name"], d.get("announced"), d.get("acquirer"), d.get("target"),
                d.get("structure"), d.get("equityValueB"), d.get("enterpriseValueB"),
                d.get("premium"), d.get("buyerType"), buyer_category(d.get("buyerType")),
                d.get("status"), d.get("expectedClose"), d.get("rationale"),
            ),
        )

    for d in data["financingDeals"]:
        cur.execute(
            "INSERT INTO financing_deals (name, parties, announced, tenant,"
            " capital_partners, structure, debt_b, equity_b, total_b, asset_value_b,"
            " contracted_revenue_b, rent_per_mw_year_m, capacity_gw, capex_per_kw,"
            " capex_flag, provenance, lease_term_years, credit_support, location,"
            " status, note) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (
                d["name"], d.get("parties"), d.get("announced"), d.get("tenant"),
                d.get("capitalPartners"), d.get("structure"), d.get("debtB"),
                d.get("equityB"), d.get("totalB"), d.get("assetValueB"),
                d.get("contractedRevenueB"), d.get("rentPerMWYearM"), d.get("capacityGW"),
                d.get("capexPerKW"), d.get("capexFlag"),
                provenance(d.get("capexFlag"), d.get("capexPerKW")),
                d.get("leaseTermYears"), d.get("creditSupport"), d.get("location"),
                d.get("status"), d.get("note"),
            ),
        )

    con.commit()
    for t in ["ppa_deals", "ma_deals", "financing_deals"]:
        n = cur.execute("SELECT COUNT(*) FROM " + t).fetchone()[0]
        print(t + ": " + str(n) + " rows")
    con.close()
    print("deals.db rebuilt")


if __name__ == "__main__":
    main()
