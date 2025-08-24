from application.database import database as db
import pandas as pd
from sqlalchemy import text

query_string = text("""
            select
            expected_annual_rent_for_showroom_space_aed,
            willingness_to_pay_booking_fee,
            primary_industry,
            ideal_showroom_size_in_sqm
            from
            questionnaire_db
            where
            primary_industry <> 'NA'
        """)

with db.engine.begin() as con:
    rows = con.execute(query_string)

df = pd.DataFrame(rows)

def willingness_to_pay_cleaning():
    with db.engine.begin() as con:
        df.to_sql(
                    name='willingness_to_pay_tbl',
                    con=con,
                    if_exists='append',
                    index=False
                )

willingness_to_pay_cleaning()