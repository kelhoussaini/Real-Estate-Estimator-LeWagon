# backend/Dockerfile

FROM python:3.8.6-buster

COPY requirements.txt app/requirements.txt
COPY RandomForest.joblib app/RandomForest.joblib
COPY XGBoost.joblib app/XGBoost.joblib
COPY robustscaler.joblib app/robustscaler.joblib





WORKDIR /app

RUN pip install -r requirements.txt
RUN pip install --upgrade pip

COPY . /app

EXPOSE 8000

CMD ["uvicorn", "fast:app", "--host", "0.0.0.0", "--port", "8000" , "--reload"]


#COPY /home/krystelle/code/Krys28/gcp/wagon-bootcamp-323012-dd58be9af1e1.json /wagon-bootcamp-323012-dd58be9af1e1.json
# COPY /path/to/your/credentials.json /credentials.json !!!!!!!!!!! Complete the path
# to credential file from Jean GCP account cf. README to know how to do it
