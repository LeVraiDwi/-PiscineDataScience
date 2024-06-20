import sqlite3 as sq
import matplotlib.pyplot as plt
import matplotlib.scale as scl
import pandas as pd
import matplotlib.dates as mdates
import psycopg
import datetime


def connectDb() -> psycopg.connection:
    try:
        connection = psycopg.connect(
            dbname="piscineds",
            user="tcosse",
            password="mysecretpassword",
            host="localhost",
            port="5432"
        )
        return connection
    except Exception as msg:
        print(msg)


def main():

    con: psycopg.connection = connectDb()
    cursor = con.cursor()
    cursor.execute("SELECT event_time, user_id, price from customer where event_type = 'purchase' and event_time BETWEEN '2022-10-01' AND '2023-01-31'")
    res = cursor.fetchall()
    cursor.close()
    data = pd.DataFrame(res, columns=['date', 'user_id','price'])
    
    #table customer per month
    customerPerMonth = data.groupby([data['date'].dt.date.rename('timeAt')])['user_id'].nunique()

    #table amount of soles per month
    SolesPerMonth = data['price'].groupby([data['date'].dt.month.rename('month'), data['date'].dt.year.rename('year')]).sum()
    SolesPerMonth = SolesPerMonth.sort_index(level=['year', 'month'])

    #table average spend per customer
    AverageSpendPerCusto = data['price'].groupby([data['date'].dt.date.rename('At'), data['user_id'].rename('user')]).sum()
    AverageSpendPerCusto = AverageSpendPerCusto.groupby('At').mean()

    #create table
    fig, axs = plt.subplots(1, 3, figsize=(8, 7), layout='constrained')

    #chart creation
    axs[0].plot(customerPerMonth.index.tolist(), customerPerMonth.values.tolist(), zorder=3)
    axs[1].bar(range(0, len(SolesPerMonth)), SolesPerMonth.values.tolist(), zorder=3)
    axs[2].stackplot(AverageSpendPerCusto.index.tolist(), AverageSpendPerCusto.values.tolist(), zorder=3)

    #config for all plot
    for ax in axs:
        ax.margins(x=0)
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))

    #chart customer per month custom
    ax = axs[0]
    ax.grid(True, zorder=0)
    ax.set_yticks([500, 1000, 1500, 2000], ['500', '1000', '1500', '2000'])
    ax.set_ylabel('Number of Customer')

    #chart amount of soles per month
    ax = axs[1]
    ax.set_xticks(range(0, len(SolesPerMonth)), ['Oct', 'Nov', 'Dec', 'Jan'])
    ax.set_ylabel('total sales in million of A')
    ax.grid(axis='y', zorder=0)

    #chart average spend per customer
    ax = axs[2]
    ax.grid(True, zorder=0)
    ax.set_ylabel('average spend/customers in A')

    plt.show()
    return


if __name__ == "__main__":
    main()