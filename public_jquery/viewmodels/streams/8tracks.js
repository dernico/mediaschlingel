var tracksVM = ["api", "player", function (api, player) {
    var self = this;
    self.api = api;
    self.searchTerm = ko.observable();
    self.tracksResult = ko.observableArray([]);

    self.tagCloud = [
        {title: "Popular", tag: "all:popular"},
        {title: "Hip Hop", tag: "tags:hip_hop"},
        {title: "Rap", tag: "tags:rap"},
        {title: "Alternative", tag: "tags:alternative"},
        {title: "Electro", tag: "tags:electro"},
        {title: "80s", tag: "tags:80s"}
    ];

    self.selectedTag = ko.observable();

    self.tagClick = function(tag){
        self.selectedTag(tag);
        self.api.tracks.tags(tag.tag, function(data, err){
            if(err){
                console.log(err);
                return;
            }
            data = data.mixes;
            self.tracksResult(data);
        });
    };

    self.loadPopular = function(){
        var tag = self.tagCloud[0];
        self.selectedTag(tag)
        self.api.tracks.tags(tag.tag, function(data, err){
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