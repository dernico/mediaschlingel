from Model.MixModel import MixModel

def create_mix_from_tracks(json):
    mix = MixModel()
    mix.ID = json["id"]
    mix.Name = json["name"]
    mix.Description = json["description"]
    mix.Tags = json["tag_list_cache"]
    mix.Likes = json["likes_count"]
    mix.Cover = json["cover_urls"]["original"]
    return mix

def create_mix_from_post(json):
    mix = MixModel()
    mix.ID = str(json["id"])
    mix.Name = json["name"]
    mix.Description = json["description"]
    mix.Tags = json["tags"]
    mix.Likes = json["likes"]
    mix.Cover = json["cover"]
    return mix