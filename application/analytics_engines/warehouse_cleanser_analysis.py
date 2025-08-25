from application.database.database import engine
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

with engine.begin() as con:
    df = pd.read_sql(
                sql='select * from warehousing_requirements_tbl',
                con=con
    )

df_warehouse_cbm = df[df['monthly_trade_volumes_units']=='CBM']
df_warehouse_mt = df[df['monthly_trade_volumes_units']=='MT']

def histogram_warehouse_cbm(show_plot: bool):
    data_set_1 = df_warehouse_cbm['monthly_trade_volumes_cbm_or_mt'].describe().to_dict()
    counts, bins = np.histogram(df_warehouse_cbm['monthly_trade_volumes_cbm_or_mt'], bins=50,range=(0, 5000))
    data_set_2 = {
        'bins': bins.tolist(),
        'counts': counts.tolist()
    }
    fig, ax = plt.subplots(figsize=(8, 6), dpi=120)
    df_warehouse_cbm['monthly_trade_volumes_cbm_or_mt'].hist(bins=50,range=(0, 5000), color='blue', ax=ax, edgecolor='grey')
    ax.set_title('Trade Volumes for Warehouse (in cbm) - Histogram')
    ax.set_xlabel('Monthly Trade Volumes (in cbm)')
    ax.set_ylabel('Frequency')
    ax.set_xlim(0, 1000)
    if show_plot:
        plt.show()
    return data_set_1, data_set_2, fig

def histogram_warehouse_mt(show_plot: bool):
    data_set_1 = df_warehouse_mt['monthly_trade_volumes_cbm_or_mt'].describe().to_dict()
    counts, bins = np.histogram(df_warehouse_mt['monthly_trade_volumes_cbm_or_mt'], bins=50,range=(0, 5000))
    data_set_2 = {
        'bins': bins.tolist(),
        'counts': counts.tolist()
    }
    fig, ax = plt.subplots(figsize=(8, 6), dpi=120)
    df_warehouse_mt['monthly_trade_volumes_cbm_or_mt'].hist(bins=50,range=(0, 5000), color='blue', ax=ax, edgecolor='grey')
    ax.set_title('Trade Volumes for Warehouse (in mt) - Histogram')
    ax.set_xlabel('Monthly Trade Volumes (in mt)')
    ax.set_ylabel('Frequency')
    ax.set_xlim(0, 1000)
    if show_plot:
        plt.show()
    return data_set_1, data_set_2, fig

def kde_warehouse_cbm(show_plot: bool):
    x = df_warehouse_cbm['monthly_trade_volumes_cbm_or_mt'].dropna().to_numpy().reshape(1, -1)
    kde = gaussian_kde(x, bw_method='scott')
    grid = np.linspace(0, 5000, 512)
    density = kde(grid)
    bandwidth = kde.factor * x.std(ddof=1)
    data_set_1 = {
        'x': grid.tolist(),
        'density': density,
        'bandwidth': bandwidth
    }
    fig, ax = plt.subplots(figsize=(8, 6), dpi=120)
    sns.kdeplot(df_warehouse_cbm['monthly_trade_volumes_cbm_or_mt'].dropna(), fill=True, ax=ax)
    ax.set_title('Trade Volumes for Warehouse (in cbm) - Kernel Density Estimation')
    ax.set_xlim(0, 5000)
    if show_plot:
        plt.show()
    return data_set_1, fig

def kde_warehouse_mt(show_plot: bool):
    x = df_warehouse_mt['monthly_trade_volumes_cbm_or_mt'].dropna().to_numpy().reshape(1, -1)
    kde = gaussian_kde(x, bw_method='scott')
    grid = np.linspace(0, 10000, 512)
    density = kde(grid)
    bandwidth = kde.factor * x.std(ddof=1)
    data_set_1 = {
        'x': grid.tolist(),
        'density': density,
        'bandwidth': bandwidth
    }
    fig, ax = plt.subplots(figsize=(8, 6), dpi=120)
    sns.kdeplot(df_warehouse_mt['monthly_trade_volumes_cbm_or_mt'].dropna(), fill=True, ax=ax)
    ax.set_title('Trade Volumes for Warehouse (in mt) - Kernel Density Estimation')
    ax.set_xlim(0, 10000)
    if show_plot:
        plt.show()
    return data_set_1, fig