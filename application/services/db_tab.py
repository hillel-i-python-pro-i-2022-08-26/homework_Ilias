from application.services.dbconnection import DbConnection


def table():
    with DbConnection() as connection:
        with connection:
            connection.execute("""
            CREATE TABLE IF NOT EXISTS phones(
            phoneID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            contactName VARCHAR NOT NULL,
            phoneNumber INTEGER NOT NULL
            )""")
