from Model.StreamModel import StreamModel

class StreamModelFactory:

    def createFromUrl(self, url):
        model = StreamModel()
        model.Description = ""
        model.Image = ""
        model.Format = url
        model.Name = url
        model.Stream = url
        model.Website = ""
        return model