import os
import pickle
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from sqlalchemy import create_engine

# Importamos las funciones y constantes de los módulos existentes
from src.config import DATASET_ROOT_PATH, get_csv_to_table_mapping, PUBLIC_HOLIDAYS_URL, SQLITE_BD_ABSOLUTE_PATH
from src.extract import extract
from src.load import load
from src.transform import run_queries

# Ruta donde se guardará el archivo temporal con los datos extraídos
DATA_PICKLE = "/tmp/extracted_data.pkl"

# Configuración de los argumentos por defecto del DAG
default_args = {
    'owner': 'tu_usuario',
    'depends_on_past': False,
    'start_date': datetime(2025, 4, 3),  # Ajusta según sea necesario
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def extraer_datos():
    """
    Función para extraer datos:
    - Lee los CSV y obtiene también los días festivos.
    - Persiste el diccionario de DataFrames en un archivo pickle.
    """
    dataframes = extract(DATASET_ROOT_PATH, get_csv_to_table_mapping(), PUBLIC_HOLIDAYS_URL)
    with open(DATA_PICKLE, "wb") as f:
        pickle.dump(dataframes, f)
    print("Extracción completada y datos guardados en", DATA_PICKLE)

def cargar_datos():
    """
    Función para cargar datos:
    - Crea una conexión a la base de datos SQLite.
    - Recupera el diccionario de DataFrames desde el archivo pickle.
    - Llama a la función load para cargar los datos en la BD.
    """
    # Crear conexión a la base de datos usando SQLite
    engine = create_engine(f"sqlite:///{SQLITE_BD_ABSOLUTE_PATH}")
    
    if not os.path.exists(DATA_PICKLE):
        raise FileNotFoundError("Archivo de datos extraídos no encontrado.")
    
    with open(DATA_PICKLE, "rb") as f:
        dataframes = pickle.load(f)
    
    load(dataframes, engine)
    print("Carga completada en la base de datos:", SQLITE_BD_ABSOLUTE_PATH)

def transformar_datos():
    """
    Función para transformar datos:
    - Crea una conexión a la base de datos.
    - Ejecuta las queries definidas en el módulo de transformación.
    - Imprime un resumen de cada resultado.
    """
    engine = create_engine(f"sqlite:///{SQLITE_BD_ABSOLUTE_PATH}")
    query_results = run_queries(engine)
    
    for query_name, df in query_results.items():
        print(f"Resultado de {query_name}: {len(df)} registros.")
    print("Transformación completada.")

# Definición del DAG
with DAG(
    'pipeline_elt',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False
) as dag:

    tarea_extraccion = PythonOperator(
        task_id='extraer_datos',
        python_callable=extraer_datos
    )

    tarea_carga = PythonOperator(
        task_id='cargar_datos',
        python_callable=cargar_datos
    )

    tarea_transformacion = PythonOperator(
        task_id='transformar_datos',
        python_callable=transformar_datos
    )

    # Definir el flujo de tareas: extraer -> cargar -> transformar
    tarea_extraccion >> tarea_carga >> tarea_transformacion
