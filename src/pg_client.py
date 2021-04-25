import psycopg2


def get_pg_client(hostname):
    conn = psycopg2.connect(dbname='default', user='root',
                            password='root', host=hostname, port='5432')

    cursor = conn.cursor()

    cursor.execute("""
    create table if not exists waitlist (
        chat_id varchar(15)
    )
    """)

    cursor.close()

    return conn


if __name__ == '__main__':
    cli = get_pg_client()

    cursor = cli.cursor()

    cursor.execute("select * from waitlist")

    print(cursor.fetchall())

    cli.close()
