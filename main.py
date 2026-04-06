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
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', {'id': 'spotifydaily'})
        
        if not table:
            return pd.DataFrame()

        rows = []
        for tr in table.find_all('tr')[1:]:
            cols = tr.find_all('td')
            if len(cols) < 3: continue
            
            # Extraemos el texto de la columna Artista - Canción
            # Kworb separa el artista de la canción con un " - "
            full_text = cols[2].get_text(separator=" ").strip()
            
            # Lista oficial de nombres a filtrar (Exactos)
            # Agregamos los nombres artísticos oficiales para no mezclar con otros
            bts_members = [
                "BTS", "JUNG KOOK", "JIMIN", " V ", "SUGA", 
                "J-HOPE", "RM", "JIN", "AGUST D", "V"
            ]
            
            # Verificamos si alguno de estos nombres es el ARTISTA principal
            # (Normalmente el artista aparece antes del primer "-")
            artist_part = full_text.split(" - ")[0].upper()
            
            es_bts = any(member.upper() in artist_part for member in bts_members)
            
            if es_bts:
                rows.append({
                    'Puesto': int(cols[0].text.strip()),
                    'Mov': cols[1].text.strip(),
                    'Canción': full_text,
                    'Reproducciones': cols[6].text.strip(),
                    'Evolución': cols[7].text.strip()
                })

        return pd.DataFrame(rows)

    except Exception as e:
        st.error(f"Error al filtrar datos: {e}")
        return pd.DataFrame()

# --- INTERFAZ ---
st.title("💜 Solo BTS: Honduras Daily Chart")
st.write(f"Filtrado exclusivo para ARMY Honduras - {datetime.now().strftime('%d/%m/%Y')}")

df = get_kworb_data()

if not df.empty:
    # Iconos de movimiento
    def icon_mov(val):
        if val == "=": return "➡️ ="
        if "+" in val: return f"🟩 {val}"
        if "-" in val: return f"🟥 {val}"
        if "RE" in val: return "🔵 RE"
        return val

    df['Mov'] = df['Mov'].apply(icon_mov)

    # Ordenar por puesto (del más alto al más bajo)
    df = df.sort_values('Puesto')

    st.dataframe(
        df[['Puesto', 'Mov', 'Canción', 'Reproducciones', 'Evolución']],
        hide_index=True,
        use_container_width=True
    )
    st.success(f"¡Lista lista! Se encontraron {len(df)} canciones de BTS/Solistas.")
else:
    st.warning("No hay canciones de BTS en el Top 200 de Honduras hoy.")

st.caption("Fuente: Kworb.net (Spotify Daily Chart)")
