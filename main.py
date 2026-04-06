import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import os
from datetime import datetime

# Credenciales que proporcionaste
CLIENT_ID = 'f693630ca5df44fa8f10bbcd5fbc6830'
CLIENT_SECRET = '5ebbe4d9a3b94065a9c7f321d471937c'

auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

def update_charts():
    # ID de la playlist "Top 200 Honduras" (Chart oficial de Spotify)
    # Nota: Spotify usa playlists específicas para los charts regionales
    playlist_id = '37i9dQZEVXbJp9wj9p9v7f' 
    
    results = sp.playlist_items(playlist_id)
    tracks = results['items']
    
    bts_data = []
    
    for i, item in enumerate(tracks):
        track = item['track']
        artists = [a['name'].upper() for a in track['artists']]
        
        # Filtramos si BTS está en la lista de artistas
        if 'BTS' in artists:
            bts_data.append({
                'Rank': i + 1,
                'Song': track['name'],
                'Artists': ", ".join([a['name'] for a in track['artists']]),
                'ID': track['id'],
                'Image': track['album']['images'][2]['url'] if track['album']['images'] else ''
            })

    df_new = pd.DataFrame(bts_data)

    # Lógica de comparación con el día anterior
    history_file = 'data/history_hn.csv'
    if os.path.exists(history_file):
        df_old = pd.read_csv(history_file)
        
        def get_status(row):
            if row['ID'] not in df_old['ID'].values:
                return '<span class="badge bg-info">NEW</span>'
            
            old_rank = df_old.loc[df_old['ID'] == row['ID'], 'Rank'].values[0]
            diff = old_rank - row['Rank']
            
            if diff > 0: return f'<span class="text-success">▲ {diff}</span>'
            if diff < 0: return f'<span class="text-danger">▼ {abs(diff)}</span>'
            return '<span class="text-muted">=</span>'
        
        df_new['Status'] = df_new.apply(get_status, axis=1)
    else:
        df_new['Status'] = '<span class="badge bg-info">NEW</span>'

    # Guardar historial para la próxima ejecución
    os.makedirs('data', exist_ok=True)
    df_new[['ID', 'Rank']].to_csv(history_file, index=False)

    # Crear el HTML con estilo
    html_content = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>BTS Charts Honduras</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {{ background-color: #121212; color: white; font-family: sans-serif; }}
            .table {{ background-color: #1e1e1e; color: white; border-radius: 10px; overflow: hidden; }}
            .img-album {{ width: 40px; border-radius: 4px; margin-right: 10px; }}
            h1 {{ color: #bb86fc; font-weight: bold; }}
        </style>
    </head>
    <body class="container py-5">
        <h1 class="text-center mb-4">BTS Spotify Charts Honduras</h1>
        <p class="text-center text-muted">Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
        <div class="table-responsive">
            <table class="table table-dark table-hover">
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Canción</th>
                        <th>Movimiento</th>
                    </tr>
                </thead>
                <tbody>
    """
    
    for _, row in df_new.iterrows():
        html_content += f"""
                    <tr>
                        <td>{row['Rank']}</td>
                        <td>
                            <img src="{row['Image']}" class="img-album">
                            <strong>{row['Song']}</strong><br>
                            <small class="text-muted">{row['Artists']}</small>
                        </td>
                        <td>{row['Status']}</td>
                    </tr>
        """
    
    html_content += """
                </tbody>
            </table>
        </div>
    </body>
    </html>
    """
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

if __name__ == "__main__":
    update_charts()
