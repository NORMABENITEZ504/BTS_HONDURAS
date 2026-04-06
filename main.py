import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime

st.set_page_config(page_title="BTS Honduras", page_icon="💜")

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
        # Lista de artistas permitidos (en mayúsculas para comparar)
        solo_bts = ["BTS", "JUNG KOOK", "JIMIN", "V", "SUGA", "J-HOPE", "RM", "JIN", "AGUST D"]

        for tr in table.find_all('tr')[1:]:
            cols = tr.find_all('td')
            if len(cols) < 3: continue
            
            # Kworb tiene el formato "Artista - Canción"
            # Extraemos el texto y lo dividimos por el guion " - "
            full_text = cols[2].get_text(separator=" ").strip()
            
            # Separamos el artista de la canción
            parts = full_text.split(" - ")
            artist_name = parts[0].strip().upper() # El artista siempre es lo primero
            
            # REGLA DE ORO: Solo si el artista está en nuestra lista de BTS
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

# --- INTERFAZ ---
st.title("💜 Solo BTS: Honduras Daily Chart")
st.write(f"Filtrado estricto para ARMY - {datetime.now().strftime('%d/%m/%Y')}")

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
else:
    st.info("No hay canciones de BTS o solistas en el Top 200 de Honduras hoy.")

st.caption("Fuente: Kworb.net")
