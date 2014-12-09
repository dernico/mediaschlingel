pages.service("player", ["api", "background", function(api, background) {

    var self = this;

    self.showPlaying = ko.observable(false);
    self.randomOff = ko.observable(true);
    self.PlayingFile = ko.observable(null);


    self.currentData = {
        Album: ko.observable(),
        Name: ko.observable(),
        Volumn: ko.observable(),
        Cover: ko.observable()
    };


    self.setCurrentInfo = function (data) {
        
        //background.setCover(data.cover);

        var album = data.album ? data.album : "-";
        var title = data.title ? data.title : "-";
        
        self.currentData.Album(album);
        self.currentData.Name(title);
        self.currentData.Volumn(data.Volume);
        self.currentData.Cover(data.cover);

        self.showPlaying(!data.IsPlaying);
        self.randomOff(!data.IsRandom);
    };

    self.LoadCurrentInfo = function () {
        api.get({
            action: "info",
            params: "",
            success: self.setCurrentInfo
        }); //gets CurrentMediaFile
    };



    self.toggleRandom = function () {
        if (self.randomOff()) {
            self.randomOff(false);
        } else {
            self.randomOff(true);
        }
        api.post("toggleRandom", { }, self.setCurrentInfo);
    };

    self.fullscreen = function () {
        api.post("fullScreen", {}, self.setCurrentInfo);
    };
    self.reload = function () {
        api.post("dummy", {}, self.setCurrentInfo);
    }; //Operate the player
    self.playpause = function (item) {
        if (self.showPlaying()) {
            api.post("play", {}, self.setCurrentInfo);
            self.showPlaying(false);
        } else {
            api.post("pause", {}, self.setCurrentInfo);
            self.showPlaying(true);
        }
    };

    self.play = function(item) {
        api.get({
            action: "play",
            params: "?id=" + item.id,
            success: self.setCurrentInfo
        });
    };

    self.playStream = function(item) {
        api.get({
            action: "playStream",
            params: "?stream=" + item.stream,
            success: self.setCurrentInfo
        });
    };

    self.playRadio = function(item){
        api.post("playRadio", "id=" + item.id, self.setCurrentInfo);
    };

    self.playTracks = function(mix){
        api.tracks.play(mix, self.setCurrentInfo);
    };
    
    self.playYouTube = function(track, done){
        api.youtube.play(track, function(data){
            self.setCurrentInfo(data);
            if(done) done(data);
        });
    };

    self.next = function () {
        api.post("next",{ }, self.setCurrentInfo);
    };
    self.prev = function () {
        api.post("prev", {}, self.setCurrentInfo);
    };
    self.volUp = function () {
        api.post("volumeUp", {}, self.setCurrentInfo);
    };
    self.volDown = function () {
        api.post("volumeDown", {}, self.setCurrentInfo);
    };

    self.activate = function(){
        self.LoadCurrentInfo();
    };
}]);