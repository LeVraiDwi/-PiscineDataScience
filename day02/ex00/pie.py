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
    cursor = con.cursor()
    cursor.execute("SELECT unnest(enum_range(NULL::eventtype))::text")
    res = cursor.fetchall()
    cursor.close()
    RowName = []
    for name in res:
        RowName.append(name[0])
    cursor = con.cursor()
    RowCount = []
    for data in RowName:
        cursor.execute("SELECT count(event_type) from customers where event_type = %s", (data, ))
        RowCount.append(cursor.fetchone()[0])
    cursor.close()
    con.close()
    plt.pie(RowCount, labels=RowName, autopct='%0.1f%%')
    plt.show()
    return


if __name__ == "__main__":
    main()