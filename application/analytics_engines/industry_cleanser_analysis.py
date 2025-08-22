from application.database.database import engine
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

with engine.begin() as con:
    df = pd.read_sql(
                sql='select * from industry_cluster_tbl',
                con=con
    )

df['company_sector'] = df['company_sector'].str.strip('{}').str.split(',')
df['product_hs_code'] = df['product_hs_code'].str.strip('{}').str.split(',')
df = df.explode('company_sector')
df = df.explode('product_hs_code')

df_industry_sector = df[['primary_industry', 'company_sector']].drop_duplicates()
df_industry_hs_code = df[['primary_industry', 'product_hs_code']].drop_duplicates()

def cross_tabulation_industry_sector():
    heat = pd.crosstab(df_industry_sector['primary_industry'], df_industry_sector['company_sector'])
    sns.heatmap(heat, cmap='YlGnBu')
    plt.show()
    return heat

cross_tabulation_industry_sector()