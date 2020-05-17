import sqlite3
import json
import DBWrapper as db


def retrieveQA(squadData):
    squadData = squadData["data"]
    QA = []

    for data in squadData:
        title = data["title"]

        for _data in data["paragraphs"]:

            for d in _data["qas"]:

                ID = d["id"]
                question = d["question"]
                answer = d["answers"]
                answer = "" if len(answer) == 0 else answer[0]["text"]
                QA.append({
                    "id": ID,
                    "title": title,
                    "question": question,
                    "answer": answer
                })

    return QA


if __name__ == "__main__":
    # Read Questions from json
    with open("selectedSquad.json") as data:
        data = json.load(data)
    QAdata = retrieveQA(data)

    # Database
    database = "CaseDatabase.db"
    conn = db.createConnection(database)
    db.createTable(conn)

    # Write Questions into database
    index = 0
    for qas in QAdata:
        ID = qas["id"]
        I = str(index)
        T = qas["title"].replace("'", "")
        Q = qas["question"].replace("'", "")
        A = qas["answer"].replace("'", "")

        columns = ["_index", "ID", "title", "question", "answer"]
        data = [I, ID, T, Q, A]
        db.insert(conn, columns, data)
        index += 1

    # Store in database and save
    db.save(conn)
    db.closeConnection(conn)
