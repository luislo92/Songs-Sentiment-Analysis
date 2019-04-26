#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 20:36:16 2019

@author: luislosada
"""
def createdf(song):
##Pulling from the API
    import spotipy
    import spotipy.util as util
    from spotipy.oauth2 import SpotifyClientCredentials
    import spotipy.oauth2 as oauth2         
##Dealing with JSON
    import json
    import pandas as pd
    from pandas.io.json import json_normalize

##This includes most markets, feel free to add more if you know the abbreviation
    market = [ "AD", "AR", "AT", "AU", "BE", "BG", "BO", "BR", "CA", "CH", "CL", "CO", "CR", "CY", 
          "CZ", "DE", "DK", "DO", "EC", "EE", "ES", "FI", "FR", "GB", "GR", "GT", "HK", "HN", "HU", 
          "ID", "IE", "IS", "IT", "JP", "LI", "LT", "LU", "LV", "MC", "MT", "MX", "MY", "NI", "NL", 
          "NO", "NZ", "PA", "PE", "PH", "PL", "PT", "PY", "SE", "SG", "SK", "SV", "TH", "TR", "TW", 
          "US", "UY", "VN" ]
##Set up your client ID and Client Secret    
    CLIENT_ID = "33a602d7e56540d3af86373bcba237af"
    CLIENT_SECRET = "6d36561d42694d8c8747079b156e15cb"
    
    credentials = oauth2.SpotifyClientCredentials(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET)
    
    token = credentials.get_access_token()
    spotify = spotipy.Spotify(auth=token)
    global df
    result = []
##Declare what parameters you want extracted from the JSON File
    parameters = ['id','artists','name','album','duration_ms','popularity']
    df = pd.DataFrame(columns = parameters,index = range(len(song)))
    for j in range(len(song)):
        track = song[j]
##Decide what you want to search for by declaring type, in this case we are using track
        res = spotify.search(track, type="track", market=market, limit=1)
        for i in range(len(parameters)):
            try:
                try:
                    if isinstance(json_normalize(res['tracks']['items'])
                    [parameters[i]][0],str) or isinstance(json_normalize(res['tracks']['items'])
                    [parameters[i]][0],np.int64) == True:
                        result.append(json_normalize(res['tracks']['items'])[parameters[i]][0])
                    else:
                        result.append(json_normalize(res['tracks']['items'][0]
                        [parameters[i]])['name'][0])      
                except KeyError or TypeError:
                    result.append(json_normalize(res['tracks']['items'][0][parameters[i]])['name'][0])
            except IndexError:
                result.append("NA")
        df.loc[j] = result
        result = []
    print("A Data Frame Called df has been created with the output:")
    return(df)

##Test It Out
import os
os.chdir('/Users/luislosada/Columbia Drive/Frameworks II/Group Assignment')    
spotify  = pd.read_csv('cleandata.csv')

popularity = createdf(song = list(spotify['song_title']))
popularity.to_csv(r'/Users/luislosada/Columbia Drive/Frameworks II/Group Assignment/popularity.csv',index=False)
