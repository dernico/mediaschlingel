var playervm = (function() {

    return function() {
        var self = this;
        self.randomOff = true;
        self.showPlaying = false;

        self.cover = $(".cover");
        self.coverImage = $(".cover-img");
        self.album = $("#album");
        self.title = $("#title");
        self.playpause = $("#playpause");
        self.playpauseIcon = $(".icon-pause");
        self.next = $("#next");
        self.prev = $("#prev");
        self.toggleRandom = $("#toggleRandom");
        self.toggleRandomIcon = $(".icon-random");
        self.volUp = $("#volUp");
        self.volDown = $("#volDown");

        self.setCurrentInfo = function (data) {
            
            self.cover.css("visible",data.cover === "" ? false : true);
            var cover = "";
            if(data.cover && data.cover.indexOf("http") != -1){
                cover = data.cover;
            }
            else{
                cover = 'Cover/' + data.cover;
            }
            self.coverImage.attr("src", cover);
            var album = data.album ? data.album : "-";
            var title = data.title ? data.title : "-";
            
            self.album.text(album);
            self.title.text(title);
            
            //self.Volumn(data.Volume);
            self.showPlaying = !data.IsPlaying;
            self.randomOff = !data.IsRandom;

            if(self.showPlaying){
                self.playpauseIcon.addClass('icon-play');
            }
            else{
                self.playpauseIcon.removeClass('icon-play');    
            }

            if(self.randomOff){
                self.toggleRandomIcon.addClass("randomOff");
            }else{
                self.toggleRandomIcon.removeClass("randomOff");
            }
        };

        self.LoadCurrentInfo = function () {
            api.get({
                action: "info",
                params: "",
                success: self.setCurrentInfo
            });
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

        self.toggleRandom.click(function (event) {
            if (self.randomOff) {
                self.randomOff = false;
            } else {
                self.randomOff = true;
            }
            api.post("toggleRandom", { }, self.setCurrentInfo);
        });

        self.playpause.click(function (event) {
            if (self.showPlaying) {
                api.post("play", {}, self.setCurrentInfo);
                self.showPlaying = false;
            } else {
                api.post("pause", {}, self.setCurrentInfo);
                self.showPlaying = true;
            }
        });

        self.next.click(function () {
            api.post("next",{ }, self.setCurrentInfo);
        });

        self.prev.click(function () {
            api.post("prev", {}, self.setCurrentInfo);
        });

        self.volUp.click(function () {
            api.post("volumeUp", {}, self.setCurrentInfo);
        });

        self.volDown.click(function () {
            api.post("volumeDown", {}, self.setCurrentInfo);
        });

        self.LoadCurrentInfo();
    };
})();
