var player = [function() {

    var self = this;

    self.showPlaying = ko.observable(false);
    self.randomOff = ko.observable(true);
    self.PlayingFile = ko.observable(null);

    self.hasCover = ko.observable();
    self.Cover = ko.observable();
    self.Album = ko.observable();
    self.Name = ko.observable();
    self.Volumn = ko.observable();


    self.setCurrentInfo = function (data) {
        self.hasCover(data.cover === "" ? false : true);
        if(data.cover && data.cover.indexOf("http") != -1){
            self.Cover(data.cover);
        }
        else{
            self.Cover('Cover/' + data.cover);
        }
        var album = data.album ? data.album : "-";
        var title = data.title ? data.title : "-";
        self.Album(album);
        self.Name(title);
        self.Volumn(data.Volume);
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


    return self;
}];