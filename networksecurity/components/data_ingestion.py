from networksecurity.exception.exception import CustomException
from networksecurity.logging.logger import logging

from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact
import sys,os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import pymongo
from typing import List
from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise CustomException(e,sys)
    
    def export_collection_as_dataframe(self):
        ## read the data from mongodb and store it in a dataframe
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            self.collection = self.mongo_client[database_name][collection_name]
            df = pd.DataFrame(list(self.collection.find()))
            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"],axis=1)
            df.replace(to_replace="na",value=np.nan,inplace=True)
            return df
        except Exception as e:
            raise CustomException(e,sys)
    
    def export_data_to_feature_store(self,dataframe:pd.DataFrame):
        try:
            feature_store_dir = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_dir)
            os.makedirs(dir_path,exist_ok=True)
            dataframe.to_csv(feature_store_dir,index=False,header=True)
            return dataframe
        except Exception as e:
            raise CustomException(e,sys)
    def split_data_as_train_test(self,dataframe:pd.DataFrame):
        try:
            train_set,test_set = train_test_split(dataframe,test_size=self.data_ingestion_config.test_size,random_state=42)
            logging.info("Performed train test split")
            logging.info(f"Train set length: {len(train_set)}")
            

            os.makedirs(os.path.dirname(self.data_ingestion_config.train_file_path), exist_ok=True)
            os.makedirs(os.path.dirname(self.data_ingestion_config.test_file_path), exist_ok=True)

            train_set.to_csv(self.data_ingestion_config.train_file_path,index=False,header=True)
            test_set.to_csv(self.data_ingestion_config.test_file_path,index=False,header=True)
            logging.info("Ingested data is saved at train and test path")
            

        except Exception as e:
            raise CustomException(e,sys)
    
    def initiate_data_ingestion(self):

        try:
            dataframe = self.export_collection_as_dataframe()
            dataframe = self.export_data_to_feature_store(dataframe)
            self.split_data_as_train_test(dataframe)
            data_ingestion_artifact = DataIngestionArtifact(
                train_file_path = self.data_ingestion_config.train_file_path,
                test_file_path = self.data_ingestion_config.test_file_path
            )
            logging.info(f"Data Ingestion artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            raise CustomException(e,sys)
        