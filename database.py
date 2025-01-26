from pymongo import MongoClient

def get_database():
    CONNECTION_STRING = "YOUR_STRING_HERE"
    client = MongoClient(CONNECTION_STRING)
    return client['bobData']

if __name__ == "__main__":   
   dbname = get_database()

  