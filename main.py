import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import streamlit as st
import os
from datetime import datetime

# 1. Configuración de conexión con Streamlit Secrets
# Esto lee las llaves que pegaste en el menú "Settings > Secrets" de Streamlit
try:
    client_id = st.secrets["SPOTIPY_CLIENT_ID"]
    client_secret = st.secrets["SPOTIPY_CLIENT_SECRET"]
except:
    st.error("Error: No se encontraron los Secrets en Streamlit. Configura SPOTIPY_CLIENT_ID y SPOTIPY_CLIENT_SECRET.")
    st.stop()

auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

def get_bts_charts():
    # ID de la playlist Top 50 Honduras (es la más estable para el ranking diario)
    playlist_id = '37i9dQZEVXbJp9wj9p9v7f' 
    
    # Obtenemos los datos de la playlist
    results = sp.playlist_items(playlist_id)
    tracks = results['items']
    
    bts_songs = []
    
    for i, item in enumerate(tracks):
        track = item['track']
        # Buscamos "BTS" en la lista de artistas (mayúsculas para evitar errores)
        artists_names = [a['name'].upper() for a in track['artists']]
        
        if 'BTS' in artists_names:
            bts_songs.append({
                'Rank': i + 1,
                'Canción': track['name'],
                'Artistas': ", ".join([a['name'] for a in track['artists']]),
                'id': track['id']
            })
    
    return pd.DataFrame(bts_songs)

# --- INTERFAZ DE LA PÁGINA ---
st.set_page_config(page_title="BTS Charts Honduras", page_icon="💜")

st.title("💜 BTS Spotify Charts: Honduras")
st.write(f"Actualizado el: {datetime.now().strftime('%d/%m/%Y')}")

# Ejecutar la función
df_new = get_bts_charts()

if not df_new.empty:
    # Lógica de comparación simple (puedes mejorarla luego con archivos CSV)
    st.subheader("Top Diario de Canciones")
    
    # Mostramos la tabla bonita
    # Usamos una columna de "Movimiento" fija por ahora mientras generas historial
    df_new['Movimiento'] = "NEW" 
    
    st.dataframe(
        df_new[['Rank', 'Canción', 'Artistas', 'Movimiento']],
        hide_index=True,
        use_container_width=True
    )
    
    st.success(f"¡Se encontraron {len(df_new)} canciones de BTS en el Top de Honduras!")
else:
    st.warning("Hoy no se detectaron canciones de BTS en el Top 50 principal de Honduras. ¡A seguir haciendo stream!")

st.divider()
st.caption("Datos obtenidos directamente de la API de Spotify.")
