from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exception import CustomException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig
import sys

if __name__ == "__main__":
    try:
        data_ingestion_config = DataIngestionConfig(TrainingPipelineConfig())
        data_ingestion = DataIngestion(data_ingestion_config)
        dataingestionartifact = data_ingestion.initiate_data_ingestion()
        logging.info("Data ingestion completed successfully")
        print(dataingestionartifact)
    except Exception as e:
        raise CustomException(e,sys)