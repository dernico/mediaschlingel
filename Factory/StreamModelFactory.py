from Model.StreamModel import StreamModel

class StreamModelFactory:

    def createFromUrl(self, id, url):
        model = StreamModel()
        model.Id = id
        model.Description = ""
        model.Image = "keinbild.jpg"
        model.Format = url
        model.Name = url
        model.Stream = url
        model.Website = ""
        model.Type = ""
        return model

    def createFromJson(self, id, json):
        model = StreamModel()
        model.Id = id
        model.Description = json["description"]
        model.Image = json["image"]
        model.Format = json["format"]
        model.Name = json["name"]
        model.Stream = json["stream"]
        model.Website = json["website"]
        #model.Type = json["type"]
        return model

    '''
    {
        "picture6Name": "t44.png", 
        "family": [], 
        "rating": 4.7, 
        "topics": [], 
        "rank": 1119, 
        "advertiser": ["international"], 
        "streamContentFormat": "MP3", 
        "picture1Name": "t100.png", 
        "shortDescription": "Webstream f\u00fcr HipHop-Musiker und Rap-K\u00fcnstler.",
        "id": 6564, 
        "picture6TransName": "t44.png", 
        "picture5TransName": "", 
        "city": "", 
        "genres": ["Hip-Hop", "Rap", "Urban"], 
        "picture4TransName": "t175.png", 
        "recentTitles": ["Snoop Dogg Pres Doggys Angels - Keep Ya Head Up", "RZA - Slow Grind African", "Lil Wayne - Prom Queen", "Killah Priest - From Then Till Now", "Digital Underground - Underwater Rimes (Remix)", "AZ f/ Raekwon - Doe Or Die Rza Remix", "wu tang clan - severe punishment", "Eminem - Turn Me Loose", "Kool Keith - Lovely Lady (Android Remix)", "Outlawz - Let It Burn (Feat Chair Crazy)", "eight ball and mjg - boom boom", "2 PAC - Changes", "Eminem - Amityville (Feat. Bizarre from D-12)", "Killarmy - Wu-Renegades", "RZA ft. Fev - Mesmerize (wtw rmx)", "Black Eyed Peas  Justin Timbe - Where Is The Love", "Capone-N-Noreaga - Y'all Don't Wanna", "\u00cd\u00e5\u00f3\u00ec\u00ee\u00eb\u00ea\u00e0\u00e5\u00ec\u00fb\u00e5 - \u00d1\u00e2\u00e5\u00f2", "Da Bomb - \u00c5\u00f1\u00eb\u00e8 \u00cd\u00e5\u00eb\u00fc\u00e7\u00ff, \u00cd\u00ee \u00ce\u00f7\u00e5\u00ed\u00fc \u00d5\u00ee\u00f7\u00e5\u00f2\u00f1\u00ff", "Suga Bang Bang - Don't Test - Wu Stallion", "Snoop Dogg Pres Doggys Angels - Gangsta In Me", "Blac Haze - Smoke Tonight (Ft. Bibkross, B", "Kool Keith - Lovely Lady (Android Remix Ins", "017 SNOOP DOGG - SUITED AND BOOTED"], 
        "subdomain": "radiohip-hop", 
        "picture5Name": "", 
        "streamURL": "http://listen.radiogora.ru:10400/", 
        "description": "Webstream f\u00fcr HipHop-Musiker und Rap-K\u00fcnstler.", 
        "needMoreClientMetaData": false, 
        "currentTrack": "Snoop Dogg Pres Doggys Angels - Keep Ya Head Up", 
        "link": "http://www.radiogora.ru/", 
        "streamUrls": [{"metaDataUrl": "http://listen.radiogora.ru:10400/", "streamUrl": "http://listen.radiogora.ru:10400/", "metaDataType": "", "contentType": "audio/mpeg", "bitRate": 128, "streamStatus": "VALID", "playingMode": "STEREO", "streamFormat": "SHOUTCAST", "streamContentFormat": "MP3", "metaDataAvailable": true, "sampleRate": 44100, "type": "STREAM", "id": 5616, "idBroadcast": 6564}, {"metaDataUrl": "http://listen.radiogora.ru:10400/;stream/1", "streamUrl": "http://listen.radiogora.ru:10400/;stream/1", "metaDataType": "", "contentType": "audio/mpeg", "bitRate": 128, "streamStatus": "VALID", "playingMode": "STEREO", "streamFormat": "SHOUTCAST", "streamContentFormat": "MP3", "metaDataAvailable": true, "sampleRate": 44100, "type": "STREAM", "id": 29637, "idBroadcast": 6564}, {"metaDataUrl": "http://listen.radiogora.ru:10400", "streamUrl": "http://listen.radiogora.ru:10400", "metaDataType": "", "contentType": "audio/mpeg", "bitRate": 128, "streamStatus": "VALID", "playingMode": "STEREO", "streamFormat": "SHOUTCAST", "streamContentFormat": "MP3", "metaDataAvailable": true, "sampleRate": 44100, "type": "STREAM", "id": 29638, "idBroadcast": 6564}], 
        "adParams": {"station_country": ["Russland"], "genres": ["Hip-Hop", "Rap", "Urban"], "family": [], "station_city": [], "topics": [], "station_continent": ["Europa"], "domain": ["radio.de"], "languages": ["Russisch"], "station": ["radiohip-hop"], "station_region": [], "userAgent": [""], "type": ["radio station "]}, "podcastUrls": [], "picture1TransName": "t100.png", "bitrate": 128, "picture4Name": "t175.png", "name": "Radio Hip-Hop", "language": ["Russisch"], 
        "oneGenre": "Hip-Hop", 
        "picture2Name": "", 
        "picture3Name": "", 
        "pictureBaseURL": "http://static.radio.de/images/broadcasts/ee/6e/6564/", 
        "country": "Russland", "playable": "FREE", "broadcastType": 1}
    }
    '''
    def createFromRadio(self, id, json):
        streamURL = ""
        streams = json["streamUrls"]
        if len(streams) > 0:
            streamURL = streams[0]["streamUrl"]
        else:
            raise Exception("Keine Streams enthalten: " + str(json))
        model = StreamModel()
        model.Id = id
        model.Description = json["description"]
        model.Image = json["pictureBaseURL"] + json["picture1Name"]
        model.Format = json["streamContentFormat"]
        model.Name = json["name"]
        model.Stream = streamURL
        model.Website = json["link"]
        model.Type = "radio"
        return model