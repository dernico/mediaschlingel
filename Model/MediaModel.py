# -*- coding: utf-8 -*-

class MediaModel(dict):

    @property
    def ID(self):
        return self['id']

    @ID.setter
    def ID(self, value):
        self['id'] = value

    @property
    def Title(self):
        return self['title']

    @Title.setter
    def Title(self, value):
        self['title'] = value

    @property
    def Artist(self):
        return self['artist']

    @Artist.setter
    def Artist(self, value):
        self['artist'] = value

    @property
    def Album(self):
        return self['album']

    @Album.setter
    def Album(self, value):
        self['album'] = value

    @property
    def Cover(self):
        return self['cover']

    @Cover.setter
    def Cover(self, value):
        self['cover'] = value

    def __init__(self):
        self.ID = ""
        self.Title = ""
        self.Artist = ""
        self.Album = ""
        self.Cover = ""
        '''
        self.id = id
        self.file = file
        self.dir = path
        self.filepath = os.path.join(path,file)
        self.artist = ""
        self.title = file
        self.album = path
        self.coverdir = coverdir
        self.covername = ""
        self.loadID3()
        '''


    def toDict(self):
        return {
            'id': self.id,
            'artist': self.artist,
            'album': self.album,
            'title': self.title,
            'path': self.filepath,
            'WebPath': '',
            'covername': self.covername
        }