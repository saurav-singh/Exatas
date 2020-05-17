import sqlite3
import os


def createConnection(DBName):
    # Overwrite database
    if os.path.exists(DBName):
        os.remove(DBName)

    # Create SQLite connection
    try:
        conn = sqlite3.connect(DBName)
        return conn
    except Exception as e:
        print("Error", e)
        return None


def closeConnection(conn):
    conn.close()


def createTable(conn):
    query = """CREATE TABLE cases (
            _index            text,
            ID                text,
            title             text,
            question          text,
            answer            text,

            title_1           text,
            abstract_1        text,
            author_1          text,
            source_1          text,
            sourceURL_1       text,

            title_2           text,
            abstract_2        text,
            author_2          text,
            source_2          text,
            sourceURL_2       text,

            title_3           text,
            abstract_3        text,
            author_3          text,
            source_3          text,
            sourceURL_3       text,

            title_4           text,
            abstract_4        text,
            author_4          text,
            source_4          text,
            sourceURL_4       text,

            title_5           text,
            abstract_5        text,
            author_5          text,
            source_5          text,
            sourceURL_5       text
            )"""
    conn.cursor().execute(query)


def insert(conn, columnList, valueList):
    column = "CASES  ("
    for col in columnList:
        column += "'" + col + "' ,"
    column = column[:-1] + ")"

    values = " VALUES ("
    for val in valueList:
        values += "'" + val + "' ,"
    values = values[:-1] + ")"

    query = "INSERT INTO " + column + values
    conn.cursor().execute(query)


def fetch(conn, columnName, tableName="cases"):
    query = "SELECT " + columnName + " FROM " + tableName + ";"
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    return data


def fetchRow(conn, i, tableName="cases"):
    query = "SELECT * FROM " + tableName
    query += " WHERE _index = " + str(i) + ";"
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    return data


def updateRow(conn, i, columnList, valueList, tableName="cases"):
    updateValues = ""
    for j in range(len(columnList)):
        col = columnList[j]
        val = valueList[j]
        updateValues += col + "='" + val + "' ,"
    updateValues = updateValues[:-1]

    query = "UPDATE " + tableName
    query += " SET " + updateValues
    query += "WHERE _index = " + str(i) + ";"

    conn.cursor().execute(query)


def count(conn, tableName="cases"):
    query = "SELECT COUNT(*) FROM " + tableName + ";"
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    return data


def save(conn):
    conn.commit()
