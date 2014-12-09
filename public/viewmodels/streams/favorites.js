//var favoritesVM = ["api", "player", function (api, player) {
pages.viewmodel("favoritesVM", ["api", "player", function (api, player) {
    var self = this;
    self.activated = false;
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

    
    self.removeRadio = function (item) {
        api.post("removeStream", "id=" + item.id, function () {
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
            showLoading: false,
            success: self.insertStreams });
    };

    self.activate = function (scope) {
        if(!self.activated){
            self.init();
        }
        //ko.applyBindings(self, scope);
    };
}]);