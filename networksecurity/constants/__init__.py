# networksecurity/constants/__init__.py
import os
import sys
import numpy as np
import pandas as pd

## defining  common constant variable for training pipeline
TARGET_COLUMN: str = "isPhishing"   
PIPELINE_NAME: str = "network_security"
ARTIFACT_DIR: str = "artifact"
FILE_NAME: str = "phishingData.csv"
TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"    




"""
Data Ingestion related constant start with DATA_INGESTION VAR NAME
"""

DATA_INGESTION_COLLECTION_NAME: str = "phishing_data"
DATA_INGESTION_DATABASE_NAME: str = "network_security"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATION: float = 0.2