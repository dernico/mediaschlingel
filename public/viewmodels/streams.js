var streams = (function () {
    return function (api, player) {
        var self = this;
        self.streams = ko.observableArray([]);
        self.listenPls = ko.observable();
        self.searchterm = ko.observable();
        self.results = ko.observableArray([]);
        self.currentRadio = null;

        self.searchRadioOnEnter = function(vm, e) {
            if (e.keyCode == 13) {
                self.searchRadio();
            }
        };

        self.searchRadio = function(){
            self.results([]);
            api.get({
                action: "radio/search",
                params: "?search=" + self.searchterm(),
                success: function(data) {
                    if (data.result) {
                        data.result.forEach(function(item){
                            self.results.push(new radioModel(item));
                        });
                    }
                }
            });
        };
        
        self.search2 = function() {
            self.results([]);
            api.laut.search(self.searchterm(), function(data) {
                if (data.results) {
                    $.each(data.results, function(i, cat) {
                        $.each(cat.items, function(j, item) {
                            self.results.push(new stationModel(item.station));
                        });

                    });
                }
            });
        };

        self.playRadio = function(item){
            player.playRadio(item);
            self.currentRadio = item;
        };

        self.play = function (item) {
            player.playStream(item);
        };

        self.saveRadio = function () {
            api.post("saveRadio", "item=" + ko.toJSON(self.currentRadio), 
                function () {
                    self.init();
            });
        };

        self.save = function (item) {
            api.post("addNew", "item=" + ko.toJSON(item), function () {
                self.init();
            });
        };

        self.addListenPlsOnEnter = function (vm, e) {
            if (e.keyCode == 13) {
                self.addListenPls();
            }
        };

        self.addListenPls = function () {
            var path = self.listenPls();
            api.post("addListenPls", "item=" + path, function () {
                self.init();
            });
        };
        self.saveStream = function (item) {
            api.post("saveStream", "item=" + ko.toJSON(item), function () {
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
            api.get({ action: "streams", 
                params: "", 
                success: self.insertStreams });
        };

        self.activate = function () {
            self.init();
        };
        //setTimeout(self.init, 800);
        self.init();
    };
})();
