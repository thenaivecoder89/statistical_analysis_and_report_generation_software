from application.database import database as db
import pandas as pd
from sqlalchemy import text

query_string = text("""
            select
            product_hs_code,
            types_of_goods_for_storage_and_distribution,
            export_countries,
            priority_gcc_me_cis_countries_for_export
            from
            questionnaire_db
            where
            product_hs_code <> 'NA'
            and types_of_goods_for_storage_and_distribution <> 'NA'
            and types_of_goods_for_storage_and_distribution <> '/'
            and export_countries <> 'NA'
            and priority_gcc_me_cis_countries_for_export <> 'NA'
        """)

with db.engine.begin() as con:
    rows = con.execute(query_string)

df = pd.DataFrame(rows)

def product_type_cleaning():
    with db.engine.begin() as con:
        df.to_sql(
                    name='product_type_tbl',
                    con=con,
                    if_exists='append',
                    index=False
                )

product_type_cleaning()