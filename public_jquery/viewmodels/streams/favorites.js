var favoritesVM = function (api, player) {
    var self = this;
    self.streams = ko.observableArray([]);
    self.api = api;

    self.play = function (item) {
        player.playStream(item);
    };

    self.deleteStream = function (item) {
        self.api.post("deleteStream", "item=" + ko.toJSON(item), function () {
            self.streams.remove(item);
        });
    };

    self.insertStreams = function (data) {
        if (data && data.streams) {
            self.streams([]);
            $.each(data.streams, function (i, item) {
                self.streams.push(item);
            });
        }
    };

    self.init = function () {
        self.api.get({ action: "streams", 
            params: "", 
            success: self.insertStreams });
    };

    self.activate = function () {
        self.init();
    };
};

