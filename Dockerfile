FROM kenzael/reestimator_backend
FROM kenzael/reestimator_frontend

RUN mkdir /streamlit_parent

#COPY api /api
COPY ree_website/requirements.txt streamlit_parent/requirements.txt
#COPY RandomForest.joblib app/RandomForest.joblib
COPY ree_website/reestimator/ streamlit_parent/reestimator
#COPY /home/krystelle/code/Krys28/gcp/wagon-bootcamp-323012-dd58be9af1e1.json /wagon-bootcamp-323012-dd58be9af1e1.json
# COPY /path/to/your/credentials.json /credentials.json !!!!!!!!!!! Complete the path
# to credential file from Jean GCP account cf. README to know how to do it

COPY ree_website/boxplot_appartements_Marseille.png  streamlit_parent/boxplot_appartements_Marseille.png
COPY ree_website/boxplot_maisons_Marseille.png  streamlit_parent/boxplot_maisons_Marseille.png
#above, my updated file


WORKDIR /streamlit_parent

#RUN pip install -r /requirements.txt
RUN pip install --upgrade pip

COPY . /streamlit_parent


EXPOSE 8509

ENTRYPOINT ["streamlit","run"]
CMD ["app-streamlit-to-heroku.py"]
