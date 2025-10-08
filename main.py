from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer
from networksecurity.exception.exception import CustomException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig,DataValidationConfig,DataTransformationConfig,ModelTrainerConfig
import sys

if __name__ == "__main__":
    try:
        data_ingestion_config = DataIngestionConfig(TrainingPipelineConfig())
        data_ingestion = DataIngestion(data_ingestion_config)
        logging.info("Starting data ingestion")
        dataingestionartifact = data_ingestion.initiate_data_ingestion()
        logging.info("Data ingestion completed successfully")
        logging.info("Starting data validation")
        print(dataingestionartifact)
        data_validation_config = DataValidationConfig(TrainingPipelineConfig())
        data_validation = DataValidation(data_validation_config,dataingestionartifact)
        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info("Data validation completed successfully")
        print(data_validation_artifact)
        logging.info("Starting data transformation")
        data_transformation_config = DataTransformationConfig(TrainingPipelineConfig())
        data_transformation = DataTransformation(data_validation_artifact,data_transformation_config)
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        logging.info("Data transformation completed successfully")
        print(data_transformation_artifact)
        logging.info("Starting model training")
        model_trainer_config = ModelTrainerConfig(TrainingPipelineConfig())
        model_trainer = ModelTrainer(model_trainer_config,data_transformation_artifact)
        model_trainer_artifact = model_trainer.initiate_model_trainer()
        logging.info("Model training completed successfully")
        print(model_trainer_artifact)
    except Exception as e:
        raise CustomException(e,sys)