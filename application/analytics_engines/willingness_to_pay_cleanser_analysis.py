from application.database.database import engine
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

with engine.begin() as con:
    df = pd.read_sql(
        sql='select * from willingness_to_pay_tbl',
        con=con
    )

df['willingness_to_pay_booking_fee'] = df['willingness_to_pay_booking_fee'].map({True:'Yes', False:'No'})
df_filtered = df[(df['expected_annual_rent_for_showroom_space_aed'] > 0) &
                 (df['expected_annual_rent_for_showroom_space_aed'] < 10000)
                ]

def scatter_plot_willingness_to_pay(show_plot: bool):
    data_set_1 = df_filtered[['ideal_showroom_size_in_sqm','expected_annual_rent_for_showroom_space_aed']].describe().to_dict()
    correlation_showroom_size_rent = df[['ideal_showroom_size_in_sqm','expected_annual_rent_for_showroom_space_aed']].corr()
    fig, ax = plt.subplots(figsize=(8, 6), dpi=120)
    plt.scatter(df_filtered['ideal_showroom_size_in_sqm'], df_filtered['expected_annual_rent_for_showroom_space_aed'])
    ax.set_xlabel("Size (sqm)")
    ax.set_ylabel("Rent (AED)")
    ax.set_title("Expected Annual Rent For Showroom (in AED) × Ideal Showroom Size (in sqm)")
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:,.0f}"))
    if show_plot:
        plt.tight_layout()
        plt.show()
    return data_set_1, correlation_showroom_size_rent, fig

def box_plot_willingness_to_pay(show_plot: bool):
    data_set_1 = (
        df_filtered
        .groupby('primary_industry')['expected_annual_rent_for_showroom_space_aed']
        .describe()
        .reset_index()
        .to_dict(orient='records')
    )
    fig, ax = plt.subplots(figsize=(8, 6), dpi=120)
    sns.boxplot(x='primary_industry', y='expected_annual_rent_for_showroom_space_aed', data=df_filtered, ax=ax)
    ax.set_xlabel("Primary Industry")
    ax.tick_params(axis='x', labelsize=10, labelrotation=90)
    ax.set_ylabel("Rent (AED)")
    ax.set_title("Expected Annual Rent For Showroom (in AED) on Primary Industry Box Plot")
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:,.0f}"))
    if show_plot:
        plt.tight_layout()
        plt.show()
    return data_set_1, fig
