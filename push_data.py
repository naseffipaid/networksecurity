import os
import sys
import json
import pandas as pd
import numpy as np
import pymongo
from networksecurity.exception.exception import CustomException
from networksecurity.logging.logger import logging

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")
import certifi
ca = certifi.where()



class NetworkDataExtract:
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise CustomException(e, sys)
        
    def cv_to_json(self, file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records =  list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise CustomException(e, sys)
    def insert_data_to_mongodb(self,records,database,collections):
        try:
            self.records = records
            self.collections = collections
            self.database = database

            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL,tls=True,tlsCAFile=ca)
            self.db = self.mongo_client[self.database]
            self.collection = self.db[self.collections]
            self.collection.insert_many(self.records)
            logging.info("Data inserted successfully")
            return len(self.records)
        except Exception as e:
            raise CustomException(e, sys)
        
if __name__ == "__main__":
    file_path = "network_data/phisingData.csv"
    database = "network_security"
    collections = "phishing_data"
    network = NetworkDataExtract()
    records = network.cv_to_json(file_path)
    no_of_records = network.insert_data_to_mongodb(records=records,database=database,collections=collections)
    print(f"Total number of records inserted: {no_of_records}")



