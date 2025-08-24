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
                sql='select * from showroom_specific_requirements_tbl',
                con=con
    )

def histogram_showroom(show_plot: bool):
    data_set_1 = df['ideal_showroom_size_in_sqm'].describe().to_dict()
    counts, bins = np.histogram(df['ideal_showroom_size_in_sqm'], bins=50,range=(0, 5000))
    data_set_2 = {
        'bins': bins.tolist(),
        'counts': counts.tolist()
    }
    fig, ax = plt.subplots(figsize=(8, 6), dpi=120)
    df['ideal_showroom_size_in_sqm'].hist(bins=50,range=(0, 5000), color='blue', ax=ax, edgecolor='grey')
    ax.set_title('Showroom Size (in sqm) - Histogram')
    ax.set_xlabel('Showroom Size (in sqm)')
    ax.set_ylabel('Frequency')
    ax.set_xlim(0, 1000)
    if show_plot:
        plt.show()
    return data_set_1, data_set_2, fig

def kde_showroom(show_plot: bool):
    x = df['ideal_showroom_size_in_sqm'].dropna().to_numpy().reshape(1, -1)
    kde = gaussian_kde(x, bw_method='scott')
    grid = np.linspace(0, 2000, 512)
    density = kde(grid)
    bandwidth = kde.factor * x.std(ddof=1)
    data_set_1 = {
        'x': grid.tolist(),
        'density': density,
        'bandwidth': bandwidth
    }
    fig, ax = plt.subplots(figsize=(8, 6), dpi=120)
    sns.kdeplot(df['ideal_showroom_size_in_sqm'].dropna(), fill=True, ax=ax)
    ax.set_title('Showroom Size (in sqm) - Kernel Density Estimation')
    ax.set_xlim(0, 2000)
    if show_plot:
        plt.show()
    return data_set_1, fig