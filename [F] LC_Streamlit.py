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
    today = datetime.today()
    first_day_month = today.replace(day=1)
    return first_day_month.strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d")


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
    debut, fin = get_date_interval()

    # Paramètres de la requête à l'API
    params_query = {
        "country": "FR",  # Pays : France
        "date_from": debut,  # Date de début
        "date_to": fin,  # Date de fin
        "limit": 10000,  # Limite de résultats
        "page": p,  # Page de résultats
        "parameter": ["pm10", "pm25", "o3", "co", "no2", "so2"],  # Paramètres à récupérer
    }

    # En-têtes pour l'authentification à l'API
    header = {
        "X-API-KEY": os.getenv("API_KEY"),  # Utilisation de la clé API depuis les variables d'environnement
    }

    # Requête HTTP GET à l'API
    response = requests.get(url, params=params_query, headers=header)

    # Si la réponse est réussie (code 200), on retourne les données sous forme de DataFrame
    if response.status_code == 200:
        return pd.DataFrame(response.json()["results"])
    else:
        # Si la requête échoue, on retourne un message d'erreur avec le code de statut
        return f"Error {response.status_code}: {response.json().get('message', 'Unknown error')}"


# Fonction pour extraire la date UTC depuis un dictionnaire
def get_utc_from_df(dict_date: dict) -> str:
    """
    Cette fonction extrait la date UTC à partir d'un dictionnaire de données.
    
    Paramètres:
        dict_date (dict): Un dictionnaire contenant une clé 'utc' pour la date UTC.

    Retourne:
        str: La valeur de la clé 'utc' dans le dictionnaire, ou "Unknown" si elle est absente.
    """
    return dict_date.get("utc", "Unknown")


# Partie principale du script Streamlit
if __name__ == "__main__":
    # Titre principal du tableau de bord
    st.title("Air Quality in France")

    # Section des filtres dans la barre latérale
    st.sidebar.header("Filters")
    parameters = st.sidebar.multiselect(
        "Select the parameters", ["pm10", "pm25", "o3", "co", "no2", "so2"], ["pm10"]
    )

    # Récupération des données depuis l'API
    data = fetch_data()
    if isinstance(data, str):
        st.error(data)
    else:
        if not data.empty:
            # Conversion de la colonne 'date' en datetime
            data["datetimestamp"] = pd.to_datetime(data["date"].map(get_utc_from_df))
            # Filtrage des données en fonction des paramètres sélectionnés
            filtered_data = data[data["parameter"].isin(parameters)]

            # Affichage du tableau de données filtrées
            st.header("Filtered Data Table")
            st.dataframe(filtered_data)

            # **1. Box Plot** (Distribution des valeurs de qualité de l'air par paramètre)
            st.header("Air Quality Distribution (Box Plot)")
            fig = px.box(
                filtered_data,
                x="parameter",
                y="value",
                color="parameter",
                title="Air Quality Parameters Distribution",
                labels={"value": "Concentration", "parameter": "Air Quality Parameter"},
            )
            st.plotly_chart(fig, use_container_width=True)

            # **2. Heatmap** (Densité des mesures au fil du temps)
            st.header("Air Quality Density Heatmap")
            fig = px.density_heatmap(
                filtered_data,
                x="datetimestamp",
                y="parameter",
                z="value",
                color_continuous_scale="Viridis",
                title="Air Quality Density Heatmap",
                labels={
                    "datetimestamp": "Date/Time",
                    "parameter": "Air Quality Parameter",
                    "value": "Concentration",
                },
            )
            st.plotly_chart(fig, use_container_width=True)

            # **3. Bar Plot** (Concentration moyenne par paramètre par jour)
            st.header("Average Air Quality Parameters per Day")
            aggregated_data = (
                filtered_data.groupby(
                    [filtered_data["datetimestamp"].dt.date, "parameter"]
                )["value"]
                .mean()
                .reset_index()
            )
            fig = px.bar(
                aggregated_data,
                x="datetimestamp",
                y="value",
                color="parameter",
                barmode="group",
                title="Average Air Quality Concentrations Per Day",
                labels={
                    "datetimestamp": "Date",
                    "value": "Average Concentration",
                    "parameter": "Air Quality Parameter",
                },
            )
            st.plotly_chart(fig, use_container_width=True)

            # **4. Violin Plot** (Distribution des valeurs de qualité de l'air avec densité de noyau)
            st.header("Air Quality Distribution (Violin Plot)")
            fig = px.violin(
                filtered_data,
                x="parameter",
                y="value",
                color="parameter",
                box=True,
                points="all",
                title="Air Quality Parameters Distribution (Violin Plot)",
                labels={"value": "Concentration", "parameter": "Air Quality Parameter"},
            )
            st.plotly_chart(fig, use_container_width=True)

        else:
            st.warning("No data available")
