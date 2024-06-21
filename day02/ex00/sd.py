import sqlite3 as sq
import matplotlib.pyplot as plt
import matplotlib.scale as scl
import pandas as pd
import psycopg


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
    cur = con.cursor()

    print("Executing query 1/4...")
    cur.execute('SELECT COUNT(*) FROM customers WHERE "event_type" = \'remove_from_cart\'')
    rfc = cur.fetchone()[0]
    print("Executing query 2/4...")
    cur.execute('SELECT COUNT(*) FROM customers WHERE "event_type" = \'cart\'')
    cart = cur.fetchone()[0]
    print("Executing query 3/4...")
    cur.execute('SELECT COUNT(*) FROM customers WHERE "event_type" = \'purchase\'')
    purchase = cur.fetchone()[0]
    print("Executing query 4/4...")
    cur.execute('SELECT COUNT(*) FROM customers WHERE "event_type" = \'view\'')
    view = cur.fetchone()[0]

    labels = ['view', 'cart', 'remove_form_cart', 'purchase']
    values = [view, cart, rfc, purchase]

    fig, ax = plt.subplots()

    ax.pie(values, labels=labels, autopct='%1.1f%%', wedgeprops = {"edgecolor" : "white", 'linewidth': 0.5})
    print(rfc, cart, purchase, view)

    plt.show()

    cur.close()
    con.close()

if __name__ == "__main__":
    main()