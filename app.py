import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# Configuración de la página
st.set_page_config(page_title="DB Automotriz - Taller", layout="wide")

# Función para conectar a la base de datos
def conectar_db():
    conn = sqlite3.connect('taller_datos.db', check_same_thread=False)
    return conn

conn = conectar_db()
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS registros 
             (id INTEGER PRIMARY KEY AUTOINCREMENT, fecha TEXT, vehiculo TEXT, 
              motor TEXT, categoria TEXT, valor TEXT, nota TEXT)''')
conn.commit()

# --- INTERFAZ ---
st.title("🚗 Mi Base de Datos Automotriz")

menu = ["🔍 Buscar Información", "➕ Registrar Nuevo Dato"]
choice = st.sidebar.selectbox("Menú", menu)

if choice == "➕ Registrar Nuevo Dato":
    st.subheader("🔐 Acceso Restringido")
    
    # --- SISTEMA DE CONTRASEÑA ---
    password = st.text_input("Introduce la clave para registrar datos", type="password")
    
    # AQUÍ PUEDES CAMBIAR LA CONTRASEÑA (Ahora es 'taller2026')
    if password == "taller2026": 
        st.success("Acceso concedido")
        with st.form("form_registro", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                vehiculo = st.text_input("Vehículo (Marca/Modelo/Año)")
                motor = st.text_input("Código de Motor")
            with col2:
                cat = st.selectbox("Categoría", ["Presión", "Voltaje", "Oscilograma", "Tip/Truco", "Otro"])
                valor = st.text_input("Medición / Valor")
            
            nota = st.text_area("Notas técnicas")
            submit = st.form_submit_button("Guardar en la Base de Datos")

            if submit:
                fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
                c.execute("INSERT INTO registros (fecha, vehiculo, motor, categoria, valor, nota) VALUES (?,?,?,?,?,?)",
                          (fecha, vehiculo, motor, cat, valor, nota))
                conn.commit()
                st.success(f"¡Dato de {vehiculo} guardado!")
    elif password == "":
        st.info("Por favor, ingresa la contraseña para habilitar el formulario.")
    else:
        st.error("Contraseña incorrecta")

else:
    st.subheader("🔍 Buscador Rápido (Abierto)")
    busqueda = st.text_input("Escribe el vehículo o motor que buscas...")
    
    df = pd.read_sql_query("SELECT * FROM registros ORDER BY id DESC", conn)
    
    if busqueda:
        df = df[df['vehiculo'].str.contains(busqueda, case=False) | 
                df['motor'].str.contains(busqueda, case=False)]

    if not df.empty:
        for index, row in df.iterrows():
            with st.expander(f"{row['vehiculo']} - {row['motor']} ({row['categoria']})"):
                st.write(f"**Fecha:** {row['fecha']}")
                st.write(f"**Valor:** {row['valor']}")
                st.info(f"**Nota Técnica:** {row['nota']}")
    else:
        st.warning("No hay datos que coincidan.")
