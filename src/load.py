from typing import Dict

from pandas import DataFrame
from sqlalchemy.engine.base import Engine



def load(data_frames: Dict[str, DataFrame], database: Engine):
    """Load the dataframes into the sqlite database.

    Args:
        data_frames (Dict[str, DataFrame]): A dictionary with keys as the table names
        and values as the dataframes.
    """
    try:
        for table_name, df in data_frames.items():
            df.to_sql(name=table_name, con=database, if_exists="replace", index=False)
            print(f"Tabla {table_name} cargado correctamente en la base de datos")
    except Exception as e:
        print(f"Error al cargar los dataframes en la base de datos: {e}")
        False
