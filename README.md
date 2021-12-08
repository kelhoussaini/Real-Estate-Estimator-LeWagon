# Data analysis
- Document here the project: reestimator
- Description: Project Description
- Data Source:
- Type of analysis:

Please document the project the better you can.

# Startup the project

The initial setup.

Create virtualenv and install the project:
```bash
sudo apt-get install virtualenv python-pip python-dev
deactivate; virtualenv ~/venv ; source ~/venv/bin/activate ;\
    pip install pip -U; pip install -r requirements.txt
```

Unittest test:
```bash
make clean install test
```

Check for reestimator in gitlab.com/{group}.
If your project is not set please add it:

- Create a new project on `gitlab.com/{group}/reestimator`
- Then populate it:

```bash
##   e.g. if group is "{group}" and project_name is "reestimator"
git remote add origin git@github.com:{group}/reestimator.git
git push -u origin master
git push -u origin --tags
```

Functionnal test with a script:

```bash
cd
mkdir tmp
cd tmp
reestimator-run
```

# Install

Go to `https://github.com/{group}/reestimator` to see the project, manage issues,
setup you ssh public key, ...

Create a python3 virtualenv and activate it:

```bash
sudo apt-get install virtualenv python-pip python-dev
deactivate; virtualenv -ppython3 ~/venv ; source ~/venv/bin/activate
```

Clone the project and install it:

```bash
git clone git@github.com:{group}/reestimator.git
cd reestimator
pip install -r requirements.txt
make clean install test                # install and test
```
Functionnal test with a script:

```bash
cd
mkdir tmp
cd tmp
reestimator-run
```

# Description colonnes

## Colonnes conservées

nom_de_colonne (numéro de colonne)
description (dtype/conversion)
_modif à faire_

**id_mutation**(0)
id keys (str)

**date_mutation**(1)
date de la mutation (à convertir en datetime)

**nature_mutation**(3)
nature de la mutation : vente, partage, adjucation (str)
_conserver seulement les lignes 'ventes', envoyer les autres dans la table 'non-traité'

**valeur_fonciere**(5)
notre target ! (à convertir en int32)

**adresse_numero**(6)
numéro dans la rue (adresse) (à convertir en int8)

**adresse_suffixe**(7)
suffixe numéro d'adresse : A, B, bis, ter... (str)

**adresse_nom_voie**(8)
nom de la rue (str)

**code_commune**(11)
code de la commune sur le plan cadastral

**code_departement**(12)
(str à cause de la Corse)

**id_parcelle**(15)
agrége code commune / code secteur cadastral / numéro parcelle
_extraire le code secteur cadastral dans autre colonne_

**type_local**(30)
type du local : maison ou appartement (dépendance est encodée dans une nouvelle colonne)

**surface_reelle_bati**(31)
un de nos rares prédicteurs (convertir en int32)

**nombre_pieces_principales**(32)
un de nos rares prédicteurs (convertir en int32)

**surface_terrain**(37)
un de nos rares prédicteurs(convertir en int32)

**longitude**(38)
**latitude**(39)
coordonnées pour la géolocalisation (float 64)
_il y a des communes non vectorisées où la géolocalisation n'est pas dispo_

## Colonnes supprimées

**adresse_code_voie**(9)
code FANTOR pour l'administration

**ancien_code_commune**(13)

**ancien_nom_commune**(14)
utile seulement si on fouille dans le cadastre passé

**ancien_id_parcelle**(16)
utile seulement si on fouille dans le cadastre passé

**numero_volume**(17)
utile seulement si on fouille dans le cadastre passé

**code_type_local**(29)
encodage du type de local. double emploi avec type_local (conservée)

**code_nature_culture**(33)

**nature_culture**(34)

**code_nature_culture_speciale**(35)

**nature_culture_speciale**(36)

pas de corrélation des cols nature avec valeur foncière

**lot1_numero**(18)

**lot1_surface_carrez**(19)

**lot2_numero**(20)

**lot2_surface_carrez**(21)

**lot3_numero**(22)

**lot3_surface_carrez**(23)

**lot4_numero**(24)

**lot4_surface_carrez**(25)

**lot5_numero**(26)

**lot5_surface_carrez** (27)

**nombre_lots**(28)
pas de corr. avec valeur foncière, et pas toujours bien rempli

**numero_disposition**(4)
Numéro d'ordre si ventes simultanées. Pas toujours bien rempli

## Colonnes qui posent question

**code_postal**(10)
code postal, différent du code commune, mais utilisé pour l'adressage

## Colonnes à créer

**Prix au m2**

**Présence dépendance**


# Description fonctions

## Preprocessing

### get_data.py

Methods (class dloading) to get datas (DataFrame) from the database Housing_France

class dloading:
  load_data_chunk(table_name,chunksize)
  _Loads a dataframe by chunks of size chunksize from table database_

  get_random_rows(table_name, numrows)
  _Loads a dataframe of size numrows from random lines of the table database_

  get_all_rows(table_name)
  _Loads a dataframe from an entire database table_

  get_num_rows(table_name, rownums)
  _Loads a dataframe of size rownums  from database table_

  show_tables()
  _show all the tables in the database Housing_France_

  data_to_sql(df, tablename, if_exists)
  _Export Data to Sql, if exists takes one of the two strings :  ['replace','append']_

### exploration.py

Methods (class Explration_data) to explore data

class Exploration_data:

  get_float_columns(self):
  _Get float columns_

  get_int_columns(self):
  _Get integer columns_

  get_object_columns(self):
  _Get object columns_

  get_count_of_missing_values(self):
  _Get count of missing values in DataFrame_

  get_columns_with_missing_values(self):  #df dataframe
  _Get columns with missing values_

  get_columns_without_missing_values(self):  #df dataframe
  _Get columns with out missing values_

  get_count_missing_vals_in_1column(self, col_name):  #df dataframe & col_name : name of column
  _Get the count of missing values in one column_

  visualize_feature_types(self):
  _Visualize a plot bar with the different types of features_

  visualize_type_local(self):
  _Visualize a plot bar with the number of each different types of local_

  visualize_lot_surface_columns(self):
  _Visualize a plot bar with the surface of lot for columns "lot number1-5"_

  visualize_lot_numero_columns(self):
  _Visualize a plot bar with  the number of lot for columns "lot number1-5"_



### preprocessing.py

Methods (class Preprocessing_data) to preprocess data

class Preprocessing_data:

  def conv_int(col):
  _Convert a column 'col' dtype (str, float, int) to the smallest type integer according to data_

  def conv_downcast(df):
  _Downcast numeric dtypes in dataframe df to save memory_

  def conv_date(col):
  _Convert a datestr column 'col' to datetime format YYYY-MM-DD_

  def drop_rows_of_specific_column(df, col_name):
  _Drop rows of specific columns with Nan_

  def remplacement_mutation(df):
  _Remplace Sale by 1 and Others type of mutation data by 0_

  def cadastral_sector(df):
  _Get secteur_cadastral from id_parcelle and add a column to df_


### Docker steps to GCP

There are 2 remaining steps in order to enable the developers from anywhere around the world to play with it:

- Push the Docker image to Google Container Registry
- Deploy the image on Google Cloud Run so that it gets instantiated into a Docker container

## 1) Push our prediction API image to Google Container Registry

1) make sure to enable Google Container Registry API for your project in GCP:
      https://console.cloud.google.com/flows/enableapi?apiid=containerregistry.googleapis.com&redirect=https://cloud.google.com/container-registry/docs/quickstart
2) If your account is not listed then you have to authenticate:
      gcloud auth login

3) let’s configure the gcloud command for the usage of Docker:
      gcloud auth configure-docker

4) verify your config. You should see your GCP account and default project:
      gcloud config list

5) define an environment variable for the name of your project:
      export PROJECT_ID=wagon-bootcamp-323012
      echo $PROJECT_ID
      gcloud config set project $PROJECT_ID

6) define an environment variable for the name of your docker image:
      export DOCKER_IMAGE_NAME=reestimator_docker
      echo $DOCKER_IMAGE_NAME

7) Now we are going to build our image =to have container:
      docker build -t eu.gcr.io/$PROJECT_ID/$DOCKER_IMAGE_NAME .

8) let’s make sure that our image runs correctly:
      docker run -e PORT=8000 -p 8000:8000 eu.gcr.io/$PROJECT_ID/$DOCKER_IMAGE_NAME

9) We can now push our image to Google Container Registry:
      docker push eu.gcr.io/$PROJECT_ID/$DOCKER_IMAGE_NAME

10) check the image in Google Container Registry
      https://console.cloud.google.com/gcr/images/wagon-bootcamp-323012?project=wagon-bootcamp-323012


## 2) Deploy the Container Registry image to Google Cloud Run

We have pushed the Docker image for our Prediction API to Google Container Registry. The image is now available for deployment by Google services such as Cloud Run.
We are going to deploy our image to production using Google Cloud Run.Cloud Run will instantiate the image into a container and run the CMD instruction inside of the Dockerfile of the image. This last step will start the uvicorn server serving our Prediction API to the world 🌍

11) Let’s run one last command:
      gcloud run deploy --image eu.gcr.io/$PROJECT_ID/$DOCKER_IMAGE_NAME --platform managed --region europe-west1


12) Any developer in the world 🌍 is now able to browse to the deployed url and make a prediction using the API
ATTENTION!!!!!!!!!!!!!!!!!!  Keep in mind that you pay for the service as long as it is up 💸

**1er test**
RESULTS : https://reestimatordockerimage-jw6jz6q2fq-ew.a.run.app
Service name (reestimatordockerimage):  reestimatordockerimage
API [run.googleapis.com] not enabled on project [607412583234].

**2eme test**
Service name (reestimatordocker):  reestimatordocker
Allow unauthenticated invocations to [reestimatordocker] (y/N)?  y

Deploying container to Cloud Run service [reestimatordocker] in project [wagon-bootcamp-323012] region [europe-west1]
✓ Deploying new service... Done.
  ✓ Creating Revision...
  ✓ Routing traffic...
  ✓ Setting IAM Policy...
Done.
Service [reestimatordocker] revision [reestimatordocker-00001-six] has been deployed and is serving 100 percent of traffic.
Service URL: https://reestimatordocker-jw6jz6q2fq-ew.a.run.app

**3eme test**

➜  reestimator git:(krys_urldockerGCP) ✗ gcloud run deploy \
    --image eu.gcr.io/$PROJECT_ID/$DOCKER_IMAGE_NAME \
    --platform managed \
    --region europe-west1 \
    --set-env-vars "GOOGLE_APPLICATION_CREDENTIALS=/credentials.json"
Service name (reestimatordocker):  reestimatordocker
Deploying container to Cloud Run service [reestimatordocker] in project [wagon-bootcamp-323012] region [europe-west1]
✓ Deploying... Done.
  ✓ Creating Revision...
  ✓ Routing traffic...
Done.
Service [reestimatordocker] revision [reestimatordocker-00002-for] has been deployed and is serving 100 percent of traffic.
Service URL: https://reestimatordocker-jw6jz6q2fq-ew.a.run.app

## 3) Writing to Google Cloud Storage from Google Cloud Run

13)  add your credentials to your image so that your code is allowed to push data to your bucket:
      1) check the path to the Google Cloud Plaform credentials you created during setup day
            echo $GOOGLE_APPLICATION_CREDENTIALS
      2) update your Dockerfile with the correct path to your credentials file:
            COPY /path/to/your/credentials.json /credentials.json

14) And deploy the new image that is able to write to GCS:
      gcloud run deploy \
        --image eu.gcr.io/$PROJECT_ID/$DOCKER_IMAGE_NAME \
        --platform managed \
        --region europe-west1 \
        --set-env-vars "GOOGLE_APPLICATION_CREDENTIALS=/credentials.json"

###OTHER CHOICE FOR A CONTINUOU+S DEPLOYMENT
## 4) Create and configure a Cloud Run service for Continuous Deployment

1) Go to Cloud Run.
    https://console.cloud.google.com/run?project=wagon-bootcamp-322821&folder=&organizationId=

2) Click on the Create Service button:
    -Enter a name for your service
    -Select a region on which to run the container of the project (for example europe-west1 for Belgium)
    -Click Next

3) Select Continuously deploy new revisions from a source repository:
    -Click on Set up with Cloud Build

4) Connect your GitHub account:
    -Select GitHub as a repository provider
    -Click on Authenticate to connect to your GitHub account

5) Install the Google Cloud Build app on the project repository:
    -Click Install Google Cloud Build
    -If asked to, select the your GitHub account
    -Check Only selected repositories
    -Select the repository of your project (🚨 Container Registry will only work correctly with repositories having a name following the kebab-case naming convention: my-repo-name)
    link to understand kebab-case: https://betterprogramming.pub/string-case-styles-camel-pascal-snake-and-kebab-case-981407998841

6) Select the source repository:
    -Select the configured repository
    -Read and check I understand …
    -Click Next

7) Configure your project:
    -Select the branch of your repository on which new commits will trigger the CD (for example ^master$)
    -Select the Dockerfile build type and enter the path to the Dockerfile in your project if required
    -Click Save

8) Select the parameters for the service:
    -Allow all traffic
    -Allow all unauthenticated invocations
    -Click Create

9) Get the production URL from the interface, it should look something like:
    Exemple: https://lw-docker-test-xi54eseqrq-ew.a.run.app/

10) Once your application is in production, as usual you will see the built image stored in Container Registry.
