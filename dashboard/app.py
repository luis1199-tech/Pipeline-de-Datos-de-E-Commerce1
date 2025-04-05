import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import os
import sys

# Aseguramos que se incluya la ruta del proyecto para poder importar módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.config import SQLITE_BD_ABSOLUTE_PATH

# Configuración de la página
st.set_page_config(page_title="Dashboard Olist", layout="wide")
st.title("📊 Dashboard Olist Data")

# Conectar a la base de datos SQLite usando la ruta definida en config.py
conn = sqlite3.connect(SQLITE_BD_ABSOLUTE_PATH)

# Obtener la lista de tablas disponibles en la base de datos
query_tables = "SELECT name FROM sqlite_master WHERE type='table';"
tables = pd.read_sql(query_tables, conn)
table_names = tables['name'].tolist()

# Barra lateral para selección de tabla
st.sidebar.subheader("Selecciona una tabla")
selected_table = st.sidebar.selectbox("Tablas disponibles", table_names)

# Cargar la tabla seleccionada
df = pd.read_sql(f"SELECT * FROM {selected_table}", conn)
conn.close()

# Mostrar la tabla de datos
st.subheader(f"Datos de la tabla: {selected_table}")
st.dataframe(df, use_container_width=True)

# Opciones para graficar si hay columnas numéricas
if not df.empty:
    numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
    if numeric_columns:
        st.sidebar.subheader("Visualización")
        selected_col = st.sidebar.selectbox("Columna numérica", numeric_columns)
        chart_type = st.sidebar.radio("Tipo de gráfico", ["Línea", "Barras"])

        # Crear una fila con dos columnas para mostrar dos gráficos distintos
        col1, col2 = st.columns(2)

        with col1:
            st.subheader(f"Gráfico de {chart_type} para {selected_col}")
            fig, ax = plt.subplots()
            if chart_type == "Línea":
                ax.plot(df[selected_col], marker='o')
            else:
                ax.bar(df.index, df[selected_col], color='orange')
            plt.xticks(rotation=45)
            st.pyplot(fig, use_container_width=True)

        with col2:
            st.subheader("Histograma")
            fig2, ax2 = plt.subplots()
            ax2.hist(df[selected_col], bins=20, color='green', edgecolor='black')
            st.pyplot(fig2, use_container_width=True)
    else:
        st.info("La tabla no contiene columnas numéricas para graficar.")
else:
    st.error("La tabla seleccionada está vacía.")
