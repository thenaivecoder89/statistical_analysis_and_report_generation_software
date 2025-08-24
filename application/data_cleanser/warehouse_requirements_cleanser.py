from application.database import database as db
import pandas as pd
from sqlalchemy import text

query_string = text("""
            select
            monthly_trade_volumes_cbm_or_mt,
            upper(monthly_trade_volumes_units) as monthly_trade_volumes_units,
            primary_industry
            from
            questionnaire_db
            where
            primary_industry <> 'NA'
            and upper(monthly_trade_volumes_units) <> 'UNITS'
        """)

with db.engine.begin() as con:
    rows = con.execute(query_string)

df = pd.DataFrame(rows)

def warehouse_requirements_cleaning():
    with db.engine.begin() as con:
        df.to_sql(
                    name='warehousing_requirements_tbl',
                    con=con,
                    if_exists='append',
                    index=False
                )

warehouse_requirements_cleaning()