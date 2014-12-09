
pages.viewmodel("albumsVM", ["api", "player", function(data, player) {

    var self = this;
    self.api = data;
    self.albums = ko.observableArray([]);
    self.albumSearch = ko.observable("");
    self.albumPage = ko.observable(1);
    self.albumCount = 10;

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
        self.api.loadAlbums(self.albumSearch(), self.albumPage(), self.albumCount, 
        function(data){
            self.albums(data);
        });
    };

    self.pageNext = function(){
        if(self.albums().length == self.albumCount){
            self.albumPage(self.albumPage() + 1);
            self.loadAlbums();
        }
    };

    self.pagePrev = function(){
        if(self.albumPage() > 1){
            self.albumPage(self.albumPage() - 1);
            self.loadAlbums();
        }
    };

    self.albumSearchChange = function(self, e){
        if(e.which == 13){
            self.loadAlbums();
        }
    };

    self.activate = function() {
        self.loadAlbums();
    };

}]);
