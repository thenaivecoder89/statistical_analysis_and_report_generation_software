from application.database import database as db
import pandas as pd
from sqlalchemy import text

query_string = text("""
            select 
            primary_industry, 
            ideal_showroom_size_in_sqm 
            from 
            questionnaire_db 
            where 
            ideal_showroom_size_in_sqm is not null 
            and primary_industry <> 'NA'
        """)

with db.engine.begin() as con:
    rows = con.execute(query_string)

df = pd.DataFrame(rows)

def showroom_specific_requirements_cleaning():
    with db.engine.begin() as con:
        df.to_sql(
                    name='showroom_specific_requirements_tbl',
                    con=con,
                    if_exists='append',
                    index=False
                )

showroom_specific_requirements_cleaning()