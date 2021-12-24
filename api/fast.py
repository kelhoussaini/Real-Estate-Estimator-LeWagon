from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import joblib
import pandas as pd
import numpy as np

app = FastAPI()

"""
CORS or "Cross-Origin Resource Sharing" refers to the situations
when a frontend running in a browser has JavaScript code
that communicates with a backend, and the backend is in a different "origin"
than the frontend.
"""

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


# Define a root '/' endpoint
@app.get("/")
def index():
    return {"greeting": "Hello world"}


@app.get("/predict")
def predict(surface, pieces, arrondissement,
            type_local):  # add parameters to execute the function
    """Enter the parameters used to execute the predict API,
    to return the price per squared meter"""
    
    dependancy = 0
    surface_terrain = 0
    arrondissements = np.zeros(16, 'int')
    index = int(arrondissement) + 7 % 16 - 1
    arrondissements[index] = 1  #vector of appartement presence concatenated

    if type_local == 'Maison':
        local = np.array([0, 1])
    else:
        local = np.array([1, 0])

    data_to_predict = np.concatenate((np.array([surface]), np.array([pieces]), np.array([surface_terrain]),
        np.array([dependancy]), arrondissements, local))


    X_pred = pd.DataFrame(data_to_predict).T
    
    model = joblib.load('XGBoost.joblib')
    test_scal = joblib.load('robustscaler.joblib')
    X_scaled = test_scal.transform(X_pred)
    y_pred = model.predict(X_scaled)
 
    return {"prediction":int(y_pred[0])} 

if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8000, debug=True)
    # y_pred = predict(50, 2, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    #                  0, 0, 1)
    #y_pred = predict(50, 2, 3,'Maison')
   
    
#Arrondissement 3
#http://localhost:8000/predict?surface=50&pieces=3&arrondissement=3&type_local=Appartement
        
#Arrondissement 5
# http://localhost:8000/predict?surface=50&pieces=3&arrondissement=5&type_local=Appartement

# either : uvicorn fast:app --reload  such as : pwd --> ..../api
# either docker-compose build, then docker compose up
