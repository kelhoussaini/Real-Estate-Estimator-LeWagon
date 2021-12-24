#FROM real-estate-estimator-lewagon_streamlit_frontend
#FROM real-estate-estimator-lewagon_fastapi_backend 

FROM python:3.8.6-buster

RUN mkdir /streamlit

#COPY api /api
COPY ree_website/requirements.txt streamlit/requirements.txt
#COPY RandomForest.joblib app/RandomForest.joblib
COPY ree_website/reestimator/ streamlit/reestimator
#COPY /home/krystelle/code/Krys28/gcp/wagon-bootcamp-323012-dd58be9af1e1.json /wagon-bootcamp-323012-dd58be9af1e1.json
# COPY /path/to/your/credentials.json /credentials.json !!!!!!!!!!! Complete the path
# to credential file from Jean GCP account cf. README to know how to do it

COPY ree_website/boxplot_appartements_Marseille.png  streamlit/boxplot_appartements_Marseille.png
COPY ree_website/boxplot_maisons_Marseille.png  streamlit/boxplot_maisons_Marseille.png
#above, my updated file


WORKDIR /streamlit

RUN pip install -r streamlit/requirements.txt
RUN pip install --upgrade pip

COPY . /streamlit


#EXPOSE 8501

ENTRYPOINT ["streamlit","run"]
CMD ["app-streamlit-to-heroku.py"]
