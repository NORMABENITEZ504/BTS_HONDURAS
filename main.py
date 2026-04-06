import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime

st.set_page_config(page_title="BTS Charts Honduras", page_icon="💜")

def get_kworb_data():
    url = "https://kworb.net/spotify/country/hn_daily.html"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(url, headers=headers)
        # Usamos BeautifulSoup para procesar el HTML que me pasaste
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', {'id': 'spotifydaily'})
        
        # Leer la tabla con Pandas
        df = pd.read_html(str(table))[0]
        
        # Filtramos por BTS y solistas
        solistas = ["BTS", "JUNG KOOK", "JIMIN", "V ", "SUGA", "J-HOPE", "RM", "JIN"]
        pattern = '|'.join(solistas)
        
        # Filtramos la columna 'Artist and Title'
        df_bts = df[df['Artist and Title'].str.contains(pattern, case=False, na=False)].copy()
        
        # Renombrar para que se vea bien
        df_bts = df_bts.rename(columns={
            'Pos': 'Puesto',
            'P+': 'Mov',
            'Artist and Title': 'Canción',
            'Streams': 'Daily Streams',
            'Streams+': 'Evolución'
        })
        
        return df_bts
    except Exception as e:
        st.error(f"Error al procesar Kworb: {e}")
        return pd.DataFrame()

# --- INTERFAZ ---
st.title("💜 BTS Charts Honduras")
st.write(f"Datos oficiales de Kworb - {datetime.now().strftime('%d/%m/%Y')}")

df = get_kworb_data()

if not df.empty:
    # Función para poner iconos a los movimientos
    def format_mov(val):
        val = str(val)
        if '=' in val: return "➡️ ="
        if '+' in val: return f"🟩 {val}"
        if '-' in val: return f"🟥 {val}"
        if 'RE' in val: return "🔵 RE"
        if 'NEW' in val: return "✨ NEW"
        return val

    df['Mov'] = df['Mov'].apply(format_mov)

    # Mostrar la tabla
    st.dataframe(
        df[['Puesto', 'Mov', 'Canción', 'Daily Streams', 'Evolución']],
        hide_index=True,
        use_container_width=True
    )
    
    st.success(f"¡Se encontraron {len(df)} canciones en el Top 200!")
else:
    st.info("No se encontraron canciones de BTS en el ranking de hoy.")

st.caption("Fuente: Kworb.net (Spotify Daily Chart Honduras)")
