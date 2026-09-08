"""SQLite queries and direct standardization of merchant risk."""

import sqlite3

import pandas as pd


def run(d, root):
    with sqlite3.connect(":memory:") as con:
        d.to_sql("transactions", con, index=False)
        cohorts = pd.read_sql_query(
            (root / "sql/cohorts.sql").read_text(),
            con,
            params={"as_of": 210, "horizon": 42},
        )
        recognized = pd.read_sql_query(
            (root / "sql/recognition.sql").read_text(), con, params={"as_of": 210}
        )
    return cohorts.merge(recognized, on="week")


def merchant_comparison(d):
    """Standardize pre-routing geography/CNP mix; route remains a mechanism."""
    recent = d[d.recent == 1]
    weights = recent.groupby(["cross_border", "cnp"]).size() / len(recent)
    rows = []
    for merchant, g in recent.groupby("merchant"):
        rates = g.groupby(["cross_border", "cnp"]).fraud.mean()
        if not weights.index.isin(rates.index).all():
            raise ValueError("Common-support cell missing")
        rows.append(
            dict(
                merchant=merchant,
                raw=g.fraud.mean(),
                standardized=(weights * rates).sum(),
                n=len(g),
            )
        )
    out = pd.DataFrame(rows)
    peer = out[out.merchant == "Peer"].iloc[0]
    out["raw_relative"] = out.raw / peer.raw
    out["standardized_relative"] = out.standardized / peer.standardized
    return out


def payment_type_cohorts(d, root):
    """Payment-type incidence and fixed-window loss from complete denominators."""
    with sqlite3.connect(":memory:") as con:
        d.to_sql("transactions", con, index=False)
        return pd.read_sql_query(
            (root / "sql/cnp_cohorts.sql").read_text(),
            con,
            params={"as_of": 210, "horizon": 42},
        )


def routing_diagnostics(d):
    """Descriptive route and missingness cells, before/after the routing shift."""
    result = (
        d.groupby(["merchant", "recent", "route", "missing"])
        .agg(
            transactions=("transaction_id", "size"),
            fraud_count=("fraud", "sum"),
            attempted_settled_value=("amount", "sum"),
            net_loss=("net", "sum"),
        )
        .reset_index()
    )
    result["fraud_incidence"] = result.fraud_count / result.transactions
    result["net_loss_rate"] = result.net_loss / result.attempted_settled_value
    return result
