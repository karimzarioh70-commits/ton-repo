import pandas
import streamlit as st
from dotenv import load_dotenv
from datetime import datetime
import requests
import os
import plotly.express as px

load_dotenv()


# Fonction pour obtenir l'intervalle de dates du mois en cours
def get_date_interval() -> tuple[str, str]:
    """
    Cette fonction renvoie l'intervalle de dates du mois en cours.
    Elle retourne le premier jour du mois ainsi que la date actuelle.
    
    Retourne:
        tuple: Un tuple contenant la date du premier jour du mois et la date actuelle,
               au format "YYYY-MM-DD".
    """
    pass


# Fonction pour récupérer les données depuis l'API OpenAQ
def fetch_data(
    url: str = "https://api.openaq.org/v2/measurements", p=1
) -> pd.DataFrame | str:
    """
    Cette fonction récupère les données de qualité de l'air depuis l'API OpenAQ pour la France,
    en fonction de l'intervalle de dates du mois en cours.

    Paramètres:
        url (str): L'URL de l'API à interroger (par défaut, l'API de OpenAQ).
        p (int): Le numéro de page des résultats à récupérer (par défaut 1).

    Retourne:
        pd.DataFrame: Un DataFrame contenant les données récupérées.
        str: Un message d'erreur si la requête échoue.
    """
    pass


# Fonction pour extraire la date UTC depuis un dictionnaire
def get_utc_from_df(dict_date: dict) -> str:
    """
    Cette fonction extrait la date UTC à partir d'un dictionnaire de données.
    
    Paramètres:
        dict_date (dict): Un dictionnaire contenant une clé 'utc' pour la date UTC.

    Retourne:
        str: La valeur de la clé 'utc' dans le dictionnaire, ou "Unknown" si elle est absente.
    """
    pass


# Partie principale du script Streamlit
if __name__ == "__main__":
    # Titre principal du tableau de bord

    # Section des filtres dans la barre latérale

    # Récupération des données depuis l'API et affichage des graphiques streamlit
