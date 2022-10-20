from flask_app.models.spotifyAPI import SpotifyAPI
class Track:
    def search_query(query):
        client_id = "310c337f3b7247a49d84b12c5c1de6ba"
        client_secret = "2d36f1dd9ed54c6f99af70d48e7495bf"
        spotify = SpotifyAPI(client_id, client_secret)
        track_list = spotify.search(query,'track')['tracks']['items']
        track_list_file = []
        for track in track_list:
            track_list_file.append({
                'title' : track['name'],
                'artist' : track['album']['artists'][0]['name'],
                'id' : track['id'],
                'image_url' : track['album']['images'][-1]['url']
            })
        return track_list_file
    
    def get_one_track_by_id(id):
        client_id = "310c337f3b7247a49d84b12c5c1de6ba"
        client_secret = "2d36f1dd9ed54c6f99af70d48e7495bf"
        spotify = SpotifyAPI(client_id,client_secret)
        entire_track = spotify.get_track(id)
        track = {
            'title' : entire_track['name'],
            'artist' : entire_track['album']['artists'][0]['name'],
            'id' : entire_track['id'],
            'image_url' : entire_track['album']['images'][-1]['url']
        }
        return track
