from datetime import datetime
import pymongo
import SportingLife
import Evo

client = pymongo.MongoClient(
    "YOUR MANGODB URL (CONNECTION STRING)")
db = client["SkiItems"]


def main():
    dateCollection = db["DateUpdated"]
    dateCollection.delete_many({})
    current_date = datetime.now().date()
    formatted_date = current_date.strftime("%Y-%m-%d")
    dateCollection.insert_one({"TimeUpdated": formatted_date})

    SportingLife.run()
    Evo.run()


if __name__ == "__main__":
    main()
