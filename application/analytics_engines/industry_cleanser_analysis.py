from application.database.database import engine
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency, f_oneway
from scipy.cluster.hierarchy import linkage, dendrogram

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
df_hs_desc['description'] = df_hs_desc['description'].str.split(';')
df_hs_desc['description'] = df_hs_desc['description'].str[0]

df = df.explode('company_sector')
df = df.explode('product_hs_code')
df_hs_desc = df_hs_desc.explode('description')

merged_df = pd.merge(df, df_hs_desc, left_on='product_hs_code', right_on='code', how='inner')

df_industry_sector = merged_df[['primary_industry', 'company_sector']].drop_duplicates()
df_industry_hs_code = merged_df[['primary_industry', 'description']]

def cross_tabulation_industry_sector(show_plot: bool):
    heat = pd.crosstab(df_industry_sector['primary_industry'], df_industry_sector['company_sector'])
    # Chi-squared test to determine statistical significance between industry and sector.
    ct = pd.crosstab(df['primary_industry'], df['company_sector'])
    chi2, p, dof, exp = chi2_contingency(ct)
    fig, ax = plt.subplots(figsize=(8, 6), dpi=120)
    sns.heatmap(heat, cmap='YlGnBu', ax=ax)
    ax.set_title("Industry × Sector (count)")
    if show_plot:
        plt.show()
    return heat, p, fig

def cross_tabulation_industry_hs_code(show_plot: bool): # REVIEW THIS!!
    heat = pd.crosstab(df_industry_hs_code['primary_industry'], df_industry_hs_code['description'])
    # Chi-squared test to determine statistical significance between industry and product.
    ct = pd.crosstab(df_industry_hs_code['primary_industry'], df_industry_hs_code['description'])
    chi2, p, dof, exp = chi2_contingency(ct)
    fig, ax = plt.subplots(figsize=(8, 6), dpi=120)
    sns.heatmap(heat, cmap='YlGnBu', ax=ax)
    ax.set_title("Industry × Product (count)")
    if show_plot:
        plt.show()
    return heat, p, fig

def dendogram_industry_sector(show_plot: bool):
    heat = pd.crosstab(df_industry_sector['primary_industry'], df_industry_sector['company_sector'])
    Z = linkage(heat, method='ward')
    z_df = pd.DataFrame(Z, columns=["cluster_1", "cluster_2", "distance", "cluster_size"])
    # Chi-squared test to determine statistical significance between industry and sector.
    ct = pd.crosstab(df_industry_sector['primary_industry'], df_industry_sector['company_sector'])
    chi2, p, dof, exp = chi2_contingency(ct)
    fig, ax = plt.subplots(figsize=(10, 6), dpi=120)
    dendrogram(Z, labels=heat.index, leaf_rotation=90, ax=ax)
    ax.set_title("Industry × Sector Dendrogram")
    if show_plot:
        plt.show()
    return z_df, p, fig

def dendogram_industry_product(show_plot: bool):
    heat = pd.crosstab(df_industry_hs_code['primary_industry'], df_industry_hs_code['description'])
    Z = linkage(heat, method='ward')
    z_df = pd.DataFrame(Z, columns=["cluster_1", "cluster_2", "distance", "cluster_size"])
    # Chi-squared test to determine statistical significance between industry and sector.
    ct = pd.crosstab(df_industry_hs_code['primary_industry'], df_industry_hs_code['description'])
    chi2, p, dof, exp = chi2_contingency(ct)
    fig, ax = plt.subplots(figsize=(10, 6), dpi=120)
    dendrogram(Z, labels=heat.index, leaf_rotation=90, ax=ax)
    ax.set_title("Industry × Product Dendrogram")
    if show_plot:
        plt.show()
    return z_df, p, fig