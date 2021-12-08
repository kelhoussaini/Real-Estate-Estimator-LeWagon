# ----------------------------------
#  PARAMETERS FOR GCP/DOCKER/HEROKU
# ----------------------------------
# GCP PARAMETERS
# ----------------------------------
# path of the file to upload to gcp (the path of the file should be absolute or should match the directory where the make command is run)
# LOCAL_PATH=XXX # exemple: PATH_TO_FILE_train_1k.csv

# project id on GCP
PROJECT_ID='wagon-bootcamp-322821'

# bucket name on GCP
BUCKET_NAME='reestimator'

# # bucket directory in which to store the uploaded file (we choose to name this data as a convention)
# BUCKET_FOLDER=data # convention folder then check that it is the good name in our project

# # name for the uploaded file inside the bucket folder (here we choose to keep the name of the uploaded file)
# # BUCKET_FILE_NAME=another_file_name_if_I_so_desire.csv
# BUCKET_FILE_NAME=$(shell basename ${LOCAL_PATH})

# # will store the packages uploaded to GCP for the training
# BUCKET_TRAINING_FOLDER =XXX # folder name where is the trainer.py

# # selected region to run our GCP
# REGION=europe-west1

# # name of the
# JOB_NAME=taxi_fare_training_pipeline_$(shell date +'%Y%m%d_%H%M%S')

# ----------------------------------
#          INSTALL & TEST
# ----------------------------------
install_requirements:
	@pip install -r requirements.txt

check_code:
	@flake8 scripts/* reestimator/*.py

black:
	@black scripts/* reestimator/*.py

test:
	@coverage run -m pytest tests/*.py
	@coverage report -m --omit="${VIRTUAL_ENV}/lib/python*"

ftest:
	@Write me

clean:
	@rm -f */version.txt
	@rm -f .coverage
	@rm -fr */__pycache__ */*.pyc __pycache__
	@rm -fr build dist
	@rm -fr reestimator-*.dist-info
	@rm -fr reestimator.egg-info

install:
	@pip install . -U

all: clean install test black check_code

count_lines:
	@find ./ -name '*.py' -exec  wc -l {} \; | sort -n| awk \
        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''
	@find ./scripts -name '*-*' -exec  wc -l {} \; | sort -n| awk \
		        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''
	@find ./tests -name '*.py' -exec  wc -l {} \; | sort -n| awk \
        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''

# ----------------------------------
#      UPLOAD PACKAGE TO PYPI
# ----------------------------------
PYPI_USERNAME=<AUTHOR>
build:
	@python setup.py sdist bdist_wheel

pypi_test:
	@twine upload -r testpypi dist/* -u $(PYPI_USERNAME)

pypi:
	@twine upload dist/* -u $(PYPI_USERNAME)


run_locally:
	@python -m ${PACKAGE_NAME}.${FILENAME}

gcp_submit_training:
	gcloud ai-platform jobs submit training ${JOB_NAME} \
		--job-dir gs://${BUCKET_NAME}/${BUCKET_TRAINING_FOLDER} \
		--package-path ${PACKAGE_NAME} \
		--module-name ${PACKAGE_NAME}.${FILENAME} \
		--python-version=${PYTHON_VERSION} \
		--runtime-version=${RUNTIME_VERSION} \
		--region ${REGION} \
		--stream-logs

# ----------------------------------
#         HEROKU COMMANDS
# ----------------------------------

streamlit:
	-@streamlit run # name_project.py

heroku_login:
	-@heroku login

heroku_create_app:
	-@heroku create ${APP_NAME}

deploy_heroku:
	-@git push heroku master
	-@heroku ps:scale web=1##### Prediction API - - - - - - - - - - - - - - - - - - - - - - - - -


# ----------------------------------
#         PREDICT API COMMANDS
# ----------------------------------

run_api:
	uvicorn api.fast:app --reload  # load web server with code autoreload
