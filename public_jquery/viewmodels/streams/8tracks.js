var tracksVM = ["api", "player", function (api, player) {
    var self = this;
    self.api = api;
    
    self.tracksResult = ko.observableArray([]);


    self.loadPopular = function(){
        self.api.tracks.popular(function(err, data){
            if(err){
                console.log(err);
                return;
            }
            data = data.mix_set.mixes;
            self.tracksResult(data);
        });
    };

    self.play = function(mix){
        //console.log(mix);
        self.api.tracks.play(mix.id);
    };

    self.activate = function () {
        self.loadPopular();
    };
}];