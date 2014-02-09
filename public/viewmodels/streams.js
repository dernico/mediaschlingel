var streams = (function () {
    return function (api, player) {
        var self = this;
        self.streams = ko.observableArray([]);
        self.listenPls = ko.observable();
        self.searchterm = ko.observable();
        self.results = ko.observableArray([]);


        self.searchOnEnter = function(vm, e) {
            if (e.keyCode == 13) {
                self.search();
            }
        };

        self.search = function() {
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

        self.play = function (item) {
            player.playStream(item);
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
                //self.streams.remove(item);
            });
        };
        self.deleteStream = function (item) {
            api.post("deleteStream", "item=" + ko.toJSON(item), function () {
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

        //Paging stuff
        self.pageIndex = 0;
        self.pageSize = 200;

        self.resetPage = function () {
            self.pageIndex = 0;
        };

        self.getURL = function () {
            var url = "";
            if (self.searchterm()) {
                url = "?filter=" + self.searchterm() + "&top=" + self.pageSize + "&skip=" + (self.pageIndex * self.pageSize);
            } else {
                url = "?top=" + self.pageSize + "&skip=" + (self.pageIndex * self.pageSize);
            }

            return url;
        };

        self.pageNext = function () {
            if (self.Localfiles.length >= 200) {
                self.pageIndex += self.pageSize;
                self.gogo();
            }
        };

        self.pagePrev = function () {
            if (self.pageIndex > 0) {
                self.pageIndex -= self.pageSize;
                self.gogo();
            }
        };


        self.init = function () {
            api.get({ action: "streams", params: self.getURL(), success: self.insertStreams });
        };

        self.activate = function () {
            self.init();
        };
        //setTimeout(self.init, 800);
        self.init();
    };
})();
