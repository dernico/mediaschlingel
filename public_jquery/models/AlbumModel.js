function AlbumModel(album) {
    var self = this;
    self.name = album.album ? album.album : "";
    self.cover = album.cover ? album.cover : "";
    self.tracks = [];
    self.showTracks = ko.observable(false);
    self.toggleTracks = function(){
        self.showTracks(!self.showTracks());
    };

    if(album.tracks){
        album.tracks.forEach(function(track){
            self.tracks.push(new MusicFileModel(track));
        });
    }
}
