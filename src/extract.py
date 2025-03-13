from typing import Dict

import requests
from pandas import DataFrame, read_csv, read_json, to_datetime


def temp() -> DataFrame:
    """Get the temperature data.
    Returns:
        DataFrame: A dataframe with the temperature data.
    """
    return read_csv("data/temperature.csv")


def get_public_holidays(public_holidays_url: str, year: str) -> DataFrame:
    """
    Obtiene los días festivos públicos desde la API.

    Args:
        public_holidays_url (str): URL base de la API de días festivos.
        year (str): Año para el cual se desean obtener los festivos.
        countryCode (str, optional): Código del país. Por defecto "BR".

    Returns:
        DataFrame: Un DataFrame con los días festivos públicos.
    """
    url = f"{public_holidays_url}/{year}/BR"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Lanza error si la solicitud falla
        
        data = response.json()
        df = DataFrame(data)
        
        # Eliminar columnas innecesarias
        df.drop(columns=["types", "counties"], errors="ignore", inplace=True)
        
        # Convertir la columna 'date' a datetime
        df["date"] = to_datetime(df["date"])
        
        return df
    
    except requests.RequestException as e:
        print(f"Error al obtener los días festivos: {e}")
        raise SystemExit(e)


def extract(
    csv_folder: str, csv_table_mapping: Dict[str, str], public_holidays_url: str
) -> Dict[str, DataFrame]:
    """Extract the data from the csv files and load them into the dataframes.
    Args:
        csv_folder (str): The path to the csv's folder.
        csv_table_mapping (Dict[str, str]): The mapping of the csv file names to the
        table names.
        public_holidays_url (str): The url to the public holidays.
    Returns:
        Dict[str, DataFrame]: A dictionary with keys as the table names and values as
        the dataframes.
    """
    dataframes = {
        table_name: read_csv(f"{csv_folder}/{csv_file}")
        for csv_file, table_name in csv_table_mapping.items()
    }

    # Se obtienen los días festivos para el año 2018
    holidays = get_public_holidays(public_holidays_url, "2018")

    dataframes["public_holidays"] = holidays

    return dataframes
