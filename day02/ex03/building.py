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
    cursor.execute("SELECT event_time, user_id, price, user_session from customers where event_type = 'purchase'")
    res = cursor.fetchall()
    cursor.close()
    data = pd.DataFrame(res, columns=['date', 'user_id','price', 'user_session'])

    CustomerFrequency = data.groupby[[data['user_id']]]

    averageBasket = data['price'].groupby([data['user_id'], data['user_session']]).sum()
    averageBasket = averageBasket.groupby(['user_id']).mean()
    #create table
    fig, axs = plt.subplots(1, 3, figsize=(8, 7), layout='constrained')

    #chart creation
    flierprops = dict(marker='o', markerfacecolor='grey', markersize=2,
                  markeredgecolor='grey')
    medianprops = dict(linestyle='-', color='black')
    box = axs[0].boxplot(data['price'], zorder=3, vert=False, medianprops = medianprops, flierprops=flierprops, patch_artist=True)
    for b in box['boxes']:
        b.set_facecolor('darkseagreen')
    box = axs[1].boxplot(data['price'], zorder=3, vert=False, medianprops = medianprops, showfliers=False, patch_artist=True)
    for b in box['boxes']:
        b.set_facecolor('darkseagreen')
    box = axs[2].boxplot(averageBasket.values, zorder=3, vert=False, medianprops = medianprops, flierprops=flierprops, patch_artist=True)
    for b in box['boxes']:
        b.set_facecolor('darkseagreen')

    #config for all plot
    for ax in axs:
        ax.set_xlabel('Price')
        ax.set_yticks([])
        ax.grid(True, zorder=0)

    #first mustache box
    ax = axs[0]

    #second mustache box
    ax = axs[1]
    ax.set_xlim(-0.75, 12.25 )
    ax.set_xticks(range(0, 14, 2))

    #third mustache box
    ax = axs[2]
    ax.set_xlim(-20, 120)

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