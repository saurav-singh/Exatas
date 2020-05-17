from sklearn.cluster import DBSCAN
from sklearn import preprocessing
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import sqlite3
import numpy as np
import pandas as pd

if __name__ == "__main__":

    # Retrieve data as pandas dataframe
    conn = sqlite3.connect("Database.db")
    query = "select c.title, c.source_1, similarity_1 from cases c where c.source_1 in \
            (select source_1 from cases group by source_1 having count(*) > 1)"
    df = pd.read_sql_query(query, conn)

    # Pre-process Data
    encoder = preprocessing.LabelEncoder()
    df["title"] = encoder.fit_transform(df["title"])
    df["source_1"] = encoder.fit_transform(df["source_1"])
    df["similarity_1"] = pd.to_numeric(df["similarity_1"])
    update = map(lambda x: round(x * 100), df["similarity_1"])
    df["similarity_1"] = list(update)

    # Cluster using DBSCAN
    cluster = DBSCAN(eps=10, min_samples=12)
    cluster.fit(df)
    labels = cluster.labels_

    # Compute Loss
    loss = 0
    for l in labels:
        loss = loss + 1 if l == -1 else loss
    print("Loss (unclustered):", (loss / len(df)) * 100, "%")

    # Plot 3D - Graph of clusters
    X = np.array(df)
    graph = plt.figure()
    ax = graph.add_subplot(111, projection="3d")
    ax.scatter(X[:, 0], X[:, 1], X[:, 2], c=labels, alpha=0.5)
    plt.show()