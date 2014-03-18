from Model.StreamModel import StreamModel

class StreamModelFactory:

    def createFromUrl(self, url):
        model = StreamModel()
        model.Description = ""
        model.Image = "keinbild.jpg"
        model.Format = url
        model.Name = url
        model.Stream = url
        model.Website = ""
        return model

    def createFromJson(self, json):
        model = StreamModel()
        model.Description = json["description"]
        model.Image = json["image"]
        model.Format = json["format"]
        model.Name = json["name"]
        model.Stream = json["stream"]
        model.Website = json["website"]
        return model