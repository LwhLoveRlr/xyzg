import pymongo


def generate_mongo_conn(db="laws_2024"):
    MONGO_HOST = "43.248.98.20:23003"
    MONGO_USER = "farbun"
    passwd = "zFSHLkxrPxJ5gYw2"
    cnn = pymongo.MongoClient('mongodb://localhost:27017/')
    return cnn[db]

