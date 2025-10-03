from networksecurity.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from networksecurity.exception.exception import CustomException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig,DataValidationConfig,TrainingPipelineConfig
from networksecurity.utils.utils import read_yaml_file,write_yaml_file
from networksecurity.constants import SCHEMA_FILE_PATH
import yaml
from scipy.stats import ks_2samp
import pandas as pd
import sys,os

class DataValidation:
    def __init__(self,data_validation_config:DataValidationConfig,
                 data_ingestion_artifact:DataIngestionArtifact):
        try:
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.schema_file_path = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise CustomException(e,sys)
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise CustomException(e,sys)
    
    def validate_number_of_columns(self,dataframe:pd.DataFrame)->bool:
        try:
            number_of_columns = len(self.schema_file_path["columns"])
            logging.info(f"Required number of columns: {number_of_columns}")
            logging.info(f"Dataframe has columns: {dataframe.columns}")
            if len(dataframe.columns) == number_of_columns:
                return True
            return False
        except Exception as e:
            raise CustomException(e,sys)
    def is_numerical_column_exist(self,dataframe:pd.DataFrame)->bool:
        try:
            numerical_columns = self.schema_file_path["numerical_columns"]
            dataframe_columns = dataframe.columns
            numerical_column_present = True
            missing_numerical_columns = []
            for num_column in numerical_columns:
                if num_column not in dataframe_columns:
                    numerical_column_present = False
                    missing_numerical_columns.append(num_column)
            if len(missing_numerical_columns)>0:
                logging.info(f"Missing numerical columns: {missing_numerical_columns}")
            return numerical_column_present
        except Exception as e:
            raise CustomException(e,sys)
    def detect_data_drift(self,base_df:pd.DataFrame,current_df:pd.DataFrame,threshold=0.05)->bool:
        try:
            status = True
            report = {}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                same_distribution = ks_2samp(d1,d2)
                if same_distribution.pvalue > threshold:
                    status = False
                report.update({column:{
                    "p_value":float(same_distribution.pvalue),
                    "same_distribution":status
                }})
            drift_report_file_path = self.data_validation_config.drift_report_file_path
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path,exist_ok=True)
            write_yaml_file(drift_report_file_path,report,replace=status)
            logging.info(f"Data drift report: {report}")
            
            return status
        except Exception as e:
            raise CustomException(e,sys)

    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            ## read the data
            train_df = DataValidation.read_data(train_file_path)
            test_df = DataValidation.read_data(test_file_path)

            status = self.validate_number_of_columns(train_df)
            if not status:
                error_message = f"Train dataframe does not have all columns"
            status = self.validate_number_of_columns(test_df)
            if not status:
                error_message = f"Test dataframe does not have all columns"
            status = self.is_numerical_column_exist(train_df)
            if not status:
                error_message = f"Train dataframe does not have all numerical columns"
            status = self.is_numerical_column_exist(test_df)
            if not status:
                error_message = f"Test dataframe does not have all numerical columns"
            
            status = self.detect_data_drift(base_df=train_df,current_df=test_df)
            # === Make sure validated & invalid dirs exist ===
            os.makedirs(self.data_validation_config.valid_data_dir, exist_ok=True)
            os.makedirs(self.data_validation_config.invalid_data_dir, exist_ok=True)

        # Also ensure drift report parent exists (detect_data_drift already does it, but safe to repeat)
            os.makedirs(os.path.dirname(self.data_validation_config.drift_report_file_path), exist_ok=True)

            train_df.to_csv(self.data_validation_config.valid_train_path,index=False,header=True)
            test_df.to_csv(self.data_validation_config.valid_test_path,index=False,header=True)

            data_validation_artifact = DataValidationArtifact(
                validation_status = status,
                valid_train_file_path = self.data_validation_config.valid_train_path,
                valid_test_file_path = self.data_validation_config.valid_test_path,
                invalid_train_file_path = self.data_validation_config.invalid_train_path,
                invalid_test_file_path = self.data_validation_config.invalid_test_path,
                drift_report_file_path = self.data_validation_config.drift_report_file_path
            )
            return data_validation_artifact

        except Exception as e:
            raise CustomException(e,sys)
    
   