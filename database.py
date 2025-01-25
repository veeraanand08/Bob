from pymongo import MongoClient

def get_database():
    CONNECTION_STRING = "mongodb+srv://veeraanand08:awesomesauce@cluster0.554d5.mongodb.net/"
    client = MongoClient(CONNECTION_STRING)
    return client['bobData']

if __name__ == "__main__":   
   dbname = get_database()

  