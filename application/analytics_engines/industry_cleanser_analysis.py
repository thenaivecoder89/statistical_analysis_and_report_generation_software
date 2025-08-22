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
    df_hs_desc = pd.read_sql(
        sql='select * from hs_codes_db',
        con=con
    )

df['company_sector'] = df['company_sector'].str.strip('{}').str.split(',')
df['product_hs_code'] = df['product_hs_code'].str.strip('{}').str.split(',')
df = df.explode('company_sector')
df = df.explode('product_hs_code')

merged_df = pd.merge(df, df_hs_desc, left_on='product_hs_code', right_on='code', how='inner')

df_industry_sector = merged_df[['primary_industry', 'company_sector']].drop_duplicates()
df_industry_hs_code = merged_df[['primary_industry', 'description']].drop_duplicates()

def cross_tabulation_industry_sector(show_plot: bool):
    heat = pd.crosstab(df_industry_sector['primary_industry'], df_industry_sector['company_sector'])
    if show_plot:
        sns.heatmap(heat, cmap='YlGnBu')
        plt.show()
    return heat

def cross_tabulation_industry_hs_code(show_plot: bool): # REVIEW THIS!!
    heat = pd.pivot_table(
        df_industry_hs_code,
        index='primary_industry',
        columns='description',
        values='code',  # choose a column to aggregate — must be numeric or countable
        aggfunc='nunique')  # or 'count' if 'code' isn't unique
    print(heat)
    if show_plot:
        sns.heatmap(heat, cmap='YlGnBu')
        plt.show()
    return heat

cross_tabulation_industry_hs_code(show_plot=True)