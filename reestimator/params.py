"""
IMPORT PARAMETERS FOR DOCKER COUNTAINER
"""
# ----------------------------------
#      GCP PARAMETERS (check which parameters to keep)
# ----------------------------------
PROJECT_ID = 'wagon-bootcamp-323012'  # Name of the project in GCP account ex: 'wagon-bootcamp-323012'
BUCKET_NAME = 'wagon-662-reestimator'  # Name of the bucker in GCP account ex: 'wagon-data-662-gilard'
# EXPERIMENT_NAME = 'XXX'# Name of your experiment in the Le Wagon MLFlow server
# BUCKET_FOLDER = 'Bucket folder'  # bucket directory in which to store the uploaded file
# BUCKET_TRAIN_DATA_PATH='<BUCKET_TRAIN_DATA_PATH>'
DOCKER_IMAGE_NAME = 'reestimator_docker_image'
# REGION='europe-west1'
# PYTHON_VERSION=3.7
# FRAMEWORK='scikit-learn'
# RUNTIME_VERSION=1.15
# PACKAGE_NAME='reestimator'
# FILENAME='<FILENAME>'

# ----------------------------------
#      DOCKER PARAMETERS (check which parameters to keep)
# ----------------------------------
# EXPERIMENT_NAME: name of your experiment in the Le Wagon MLFlow server GCP or HEroku
# ???????????????????????????????? What is the experiment name and what is its utility?

# ----------------------------------
#      HEROKU PARAMETERS (check which parameters to keep)
# ----------------------------------


# ----------------------------------
#      PREDICT PARAMETERS (check which parameters to keep)
# ----------------------------------
STORAGE_LOCATION = 'path location to model.joblib file'

# ----------------------------------
#      PACKAGE PARAMETERS (check which parameters to keep)
# ----------------------------------

PACKAGE_NAME=reestimator
FILENAME=trainerFinal
