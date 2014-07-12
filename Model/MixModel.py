# -*- coding: utf-8 -*-

class MixModel(dict):

    @property
    def ID(self):
        return self['id']

    @ID.setter
    def ID(self, value):
        self['id'] = value

    @property
    def Name(self):
        return self['name']

    @Name.setter
    def Name(self, value):
        self['name'] = value

    @property
    def Description(self):
        return self['description']

    @Description.setter
    def Description(self, value):
        self['description'] = value

    @property
    def Tags(self):
        return self['tags']

    @Tags.setter
    def Tags(self, value):
        self['tags'] = value

    @property
    def Likes(self):
        return self['likes']

    @Likes.setter
    def Likes(self, value):
        self['likes'] = value

    @property
    def Cover(self):
        return self['cover']

    @Cover.setter
    def Cover(self, value):
        self['cover'] = value

    @property
    def IsLocal(self):
        return self['islocal']

    @IsLocal.setter
    def IsLocal(self, value):
        self['islocal'] = value

    def __init__(self):
        self.ID = ""
        self.Name = ""
        self.Description = ""
        self.Tags = ""
        self.Likes = ""
        self.Cover = ""
        self.IsLocal = False