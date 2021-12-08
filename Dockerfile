FROM python:3.8.6-buster

COPY api /api
COPY requirements.txt /requirements.txt
COPY RandomForest.joblib /RandomForest.joblib
COPY reestimator /reestimator
COPY /home/krystelle/code/Krys28/gcp/wagon-bootcamp-323012-dd58be9af1e1.json /wagon-bootcamp-323012-dd58be9af1e1.json
# COPY /path/to/your/credentials.json /credentials.json !!!!!!!!!!! Complete the path
# to credential file from Jean GCP account cf. README to know how to do it

RUN pip install --upgrade pip
RUN pip install -r requirements.txt


CMD uvicorn api.fast:app --host 0.0.0.0 --port $PORT
