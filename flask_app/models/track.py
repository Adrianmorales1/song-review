from spotifyAPI import SpotifyAPI
class Track:
    def __init(self,track_id):
        self.id = track_id
        self.client_id = "310c337f3b7247a49d84b12c5c1de6ba"
        self.client_secret = "2d36f1dd9ed54c6f99af70d48e7495bf"
    
    def search_query(self, query):
        spotify = SpotifyAPI(self.client_id,self.client_secret)
        track_list = spotify.search(query,'track')['tracks']['items']
        track_list_file = []
        for track in track_list:
            track_list_file.append({
                'title' : track['name'],
                'artist' : track['album']['artists'][0]['name'],
                'id' : track['id'],
                'image_url' : track['album']['images'][-2]['url']
            })
        return track_list_file
    
    def get_one_track_by_id(self,id):
        spotify = SpotifyAPI(self.client_id,self.client_secret)
        entire_track = spotify.get_track(id)
        track = [{
            'title' : track['name'],
            'artist' : track['album']['artists'][0]['name'],
            'id' : track['id'],
            'image_url' : track['album']['images'][-2]['url']
        }]
        return track
