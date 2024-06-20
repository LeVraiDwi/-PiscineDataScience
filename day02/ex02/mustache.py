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
    cursor.execute("SELECT event_time, user_id, price from customer where event_type = 'purchase'")
    res = cursor.fetchall()
    cursor.close()
    data = pd.DataFrame(res, columns=['date', 'user_id','price'])
    
    mean = data['price'].mean()
    count = data['price'].count()
    std = data['price'].std()
    min = data['price'].min()
    quart = data['price'].quantile(0.25)
    mid = data['price'].quantile(0.50)
    tier = data['price'].quantile(0.75)
    max = data['price'].max()

    print(count)
    print(mean)
    print(std)
    print(min)
    print(quart)
    print(mid)
    print(tier)
    print(max)

    #create table
    fig, axs = plt.subplots(1, 3, figsize=(8, 7), layout='constrained')

    #chart creation
    axs[0].boxplot(data['price'], zorder=3, vert=False)
    axs[1].boxplot(data['price'], zorder=3, vert=False, showfliers=False)
   

    #config for all plot
    for ax in axs:
        ax.set_xlabel('Price')
        ax.set_yticks([])
        ax.grid(True, zorder=0)
        ax.spines['boxes'].set_color('#7dba7f')

    #first mustache box
    ax = axs[0]

    #first mustache box
    ax = axs[1]
    ax.set_xlim(-0.75, 12.25 )

    #chart amount of soles per month
    #ax = axs[1]
    #ax.set_xticks(range(0, len(SolesPerMonth)), ['Oct', 'Nov', 'Dec', 'Jan'])
    #ax.set_ylabel('total sales in million of A')
    #ax.grid(axis='y', zorder=0)

    #chart average spend per customer
    #ax = axs[2]
    #ax.grid(True, zorder=0)
    #ax.set_ylabel('average spend/customers in A')

    plt.show()
    return


if __name__ == "__main__":
    main()