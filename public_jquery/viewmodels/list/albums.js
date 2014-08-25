
pages.viewmodel("albumsVM", ["api", "player", function(data, player) {

    var self = this;
    self.api = data;
    self.albums = ko.observableArray([]);

    self.playAlbum = function(album){
        if(album.tracks.length > 0){
            var track = album.tracks[0];
            player.play(track);
        }
    };

    self.playTrack = function(track){
        player.play(track);
    };

    self.loadAlbums = function(){
        self.api.loadAlbums(function(data){

            self.albums(data);
        });
    };

    self.activate = function() {
        self.loadAlbums();
    };

}]);
