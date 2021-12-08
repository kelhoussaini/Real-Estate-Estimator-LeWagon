-------------------------------------
# VISUALISATION - CARTES & PREDICTION
-------------------------------------
Etapes pour la mise en place de notre application web pour présenter notre travail:
  - la carte de la France avec les prix par mètre carré par département
  - la carte de la France avec le nombre de transaction par département
  - les cartes individuelles pour Paris, Lyon, Marseille
  - la description des statistiques à l'aide d'un graphique de boxplot pour illustrer les fluctuation de prix par mètre carré en fonction de chaque arrondissement de Marseille
  - le résultat de notre modèle prédictif en fonction de l'input de l'utilisateur

_________________________________________________________
## CARTOGRAPHIE NATIONALE
_________________________________________________________
1) Réaliser un choropleth pour afficher une carte de la France en fonction des paramètres suivants (choix laissés à l'utilisateur):
    - les nombres de transactions ou les prix moyens par département
    - les types de vente : Maison ou Appartement
2) Réaliser un choropleth avec les mêmes paramètres pour afficher une carte plus précise en fonction des arrondissements pour les villes: Marseille, Paris, Lyon

_________________________________________________________
## PARTIE VISUALISATION STATISTIQUES DESCRIPTIVES
_________________________________________________________
4) Réaliser le graphique de boxplot pour illustrer les fluctuations de prix au mètre carré pour chaque arrondissement de Marseille

_________________________________________________________
## PARTIE PREDICTIVE SUR LA VILLE DE MARSEILLE
_________________________________________________________
#### 1) "ENTRER LES DONNEES VOULUES PAR L'UTILISATEUR"
_________________________________________________________
5) Principaux paramètres nécessaires pour faire tourner notre predict API en fonction des choix de l'utilisateur
??? Paramètres à revoir et à préciser quand le modèle prédictif final sera disponible ???
-- Type de local : Maison ou Appartement
-- Surface du bien à évaluer
-- Code postal de la commune concernée
6) Décider "Comment l'utilisateur pourra renseigner ces derniers paramètres

_________________________________________________________
#### 2) AFFICHAGE DU RESULTAT EN FONCTION DE L'API DE PREDICTION
_________________________________________________________
7) Compléter la partie request json pour appeler la API de prédiction
6) Créer un bouton pour renvoyer le prix/m² pour la surface renseignée par l'utilisateur
8) Afficher le prix au m² calculé par la
prédiction
