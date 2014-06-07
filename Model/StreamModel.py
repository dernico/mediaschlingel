# -*- coding: utf-8 -*-

class StreamModel(dict):

    @property
    def Id(self):
        return self['id']

    @Id.setter
    def Id(self, value):
        self['id'] = value

    @property
    def Description(self):
        return self['description']

    @Description.setter
    def Description(self, value):
        self['description'] = value

    @property
    def Image(self):
        return self['image']

    @Image.setter
    def Image(self, value):
        self['image'] = value

    @property
    def Format(self):
        return self['format']

    @Format.setter
    def Format(self, value):
        self['format'] = value

    @property
    def Name(self):
        return self['name']

    @Name.setter
    def Name(self, value):
        self['name'] = value

    @property
    def Stream(self):
        return self['stream']

    @Stream.setter
    def Stream(self, value):
        self['stream'] = value

    @property
    def Website(self):
        return self['website']

    @Website.setter
    def Website(self, value):
        self['website'] = value

    @property
    def Type(self):
        return self['type']

    @Type.setter
    def Type(self, value):
        self['type'] = value

    def __init__(self):
        self.Description = ""
        self.Image = ""
        self.Format = ""
        self.Name = ""
        self.Stream = ""
        self.Website = ""
        self.Type = ""
