var tracksVM = ["api", "player", function (api, player) {
    var self = this;
    self.api = api;
    self.searchTerm = ko.observable();
    self.tracksResult = ko.observableArray([]);


    self.loadPopular = function(){
        self.api.tracks.popular(function(data, err){
            if(err){
                console.log(err);
                return;
            }
            data = data.mixes;
            self.tracksResult(data);
        });
    };

    self.searchOnEnter = function(self, e){
        if(e.which != 13 ) return;
        self.search();
    };

    self.search = function(){
        self.api.tracks.search(self.searchTerm(), function(results, err){
            if(!results) return;

            self.tracksResult(results.mixes);
        });
    };

    self.play = function(mix){
        //console.log(mix);
        player.playTracks(mix);
    };

    self.activate = function () {
        self.loadPopular();
    };
}];