import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

st.set_page_config(page_title="BTS Charts Honduras", page_icon="💜")

def get_kworb_data():
    url = "https://kworb.net/spotify/country/hn_daily.html"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(url, headers=headers)
        # Forzamos la codificación correcta para evitar caracteres raros
        response.encoding = 'utf-8'
        
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', {'id': 'spotifydaily'})
        
        if not table:
            st.error("No se pudo encontrar la tabla en Kworb.")
            return pd.DataFrame()

        # Extraemos las filas manualmente para mayor precisión
        rows = []
        for tr in table.find_all('tr')[1:]: # Saltamos el encabezado
            cols = tr.find_all('td')
            if len(cols) < 3: continue
            
            # Limpiamos el texto de la columna de Artista y Canción
            raw_text = cols[2].get_text(separator=" ").strip()
            
            rows.append({
                'Puesto': cols[0].text.strip(),
                'Mov': cols[1].text.strip(),
                'Contenido': raw_text,
                'Streams': cols[6].text.strip(),
                'Evolución': cols[7].text.strip()
            })

        df = pd.DataFrame(rows)

        # Filtro de búsqueda mejorado (BTS y solistas)
        # Agregué variantes para asegurar que no se escape nada
        terminos = ["BTS", "JUNG KOOK", "JIMIN", " V ", "SUGA", "J-HOPE", "RM", "JIN", "AGUST D"]
        pattern = '|'.join(terminos)
        
        # Buscamos en el contenido limpio
        df_bts = df[df['Contenido'].str.contains(pattern, case=False, na=False)].copy()
        
        return df_bts

    except Exception as e:
        st.error(f"Error técnico: {e}")
        return pd.DataFrame()

# --- INTERFAZ ---
st.title("💜 BTS & Solistas: Honduras Daily")

if st.button('🔄 Forzar Actualización'):
    st.cache_data.clear()

df = get_kworb_data()

if not df.empty:
    # Formato visual para los movimientos
    def icon_mov(val):
        if val == "=": return "➡️ ="
        if "+" in val: return f"🟩 {val}"
        if "-" in val: return f"🟥 {val}"
        return f"🔵 {val}"

    df['Mov'] = df['Mov'].apply(icon_mov)

    st.dataframe(
        df[['Puesto', 'Mov', 'Contenido', 'Streams', 'Evolución']],
        hide_index=True,
        use_container_width=True
    )
    st.success(f"¡Éxito! Se encontraron {len(df)} entradas de BTS en el Top 200 de Honduras.")
else:
    st.warning("No se encontraron coincidencias. Revisa si los nombres en Kworb han cambiado.")

st.caption("Fuente: Kworb.net")
