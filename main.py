import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="BTS Charts Honduras", page_icon="💜")

def get_kworb_data():
    url = "https://kworb.net/spotify/country/hn_daily.html"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', {'id': 'spotifydaily'})
        
        if not table:
            return pd.DataFrame()

        rows = []
        # LISTA OFICIAL (Solo estos artistas pueden aparecer)
        solo_bts = ["BTS", "JUNG KOOK", "JIMIN", "V", "SUGA", "J-HOPE", "RM", "JIN", "AGUST D"]

        for tr in table.find_all('tr')[1:]:
            cols = tr.find_all('td')
            if len(cols) < 3: continue
            
            # Extraemos el texto de la columna "Artist and Title"
            full_text = cols[2].get_text(separator=" ").strip()
            
            # Dividimos para obtener el nombre del artista (lo que está antes del guion)
            # Ejemplo: "BTS - SWIM" -> Artista: "BTS"
            parts = full_text.split(" - ")
            artist_name = parts[0].strip().upper() 
            
            # FILTRO ESTRICTO: El artista debe ser exactamente uno de nuestra lista
            if any(member == artist_name for member in solo_bts):
                rows.append({
                    'Puesto': int(cols[0].text.strip()),
                    'Mov': cols[1].text.strip(),
                    'Canción': full_text,
                    'Reproducciones': cols[6].text.strip(),
                    'Evolución': cols[7].text.strip()
                })

        return pd.DataFrame(rows)

    except Exception as e:
        st.error(f"Error: {e}")
        return pd.DataFrame()

# --- INTERFAZ (TÍTULO NUEVO) ---
st.title("BTS Charts Honduras")
st.write(f"Actualizado el: {datetime.now().strftime('%d/%m/%Y')}")

df = get_kworb_data()

if not df.empty:
    def icon_mov(val):
        if val == "=": return "➡️ ="
        if "+" in val: return f"🟩 {val}"
        if "-" in val: return f"🟥 {val}"
        return f"🔵 {val}"

    df['Mov'] = df['Mov'].apply(icon_mov)
    df = df.sort_values('Puesto')

    st.dataframe(
        df[['Puesto', 'Mov', 'Canción', 'Reproducciones', 'Evolución']],
        hide_index=True,
        use_container_width=True
    )
    st.success(f"Se encontraron {len(df)} canciones en el ranking.")
else:
    st.info("No hay canciones de BTS o solistas en el Top 200 de Honduras hoy.")

st.caption("Fuente de datos: Kworb.net")
