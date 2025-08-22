from application.database import database as db
from sqlalchemy import create_engine, text
import pandas as pd


query_string = text("""
                        select 
                        primary_industry,
                        company_sector,
                        product_hs_code
                        from
                        questionnaire_db
                        where
                        primary_industry <> 'NA'
                        and company_sector <> 'NA'
                        and product_hs_code <> 'NA' or product_hs_code is not null
                    """)

with db.engine.begin() as con:
    rows = con.execute(query_string)

df = pd.DataFrame(rows)

def industry_cluster_cleaning():
    with db.engine.begin() as con:
        df.to_sql(
            name='industry_cluster_tbl',
            con=con,
            if_exists='append',
            index=False
        )

industry_cluster_cleaning()