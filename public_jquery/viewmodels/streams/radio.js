//var radioVM = ["api", "player", function (api, player) {
pages.viewmodel("radioVM", ["api", "player", function (api, player) {
    var self = this;
    self.listenPls = ko.observable();
    self.searchterm = ko.observable();
    self.results = ko.observableArray([]);
    self.currentRadio = null;
    self.api = api;

    self.searchRadioOnEnter = function(vm, e) {
        if (e.keyCode == 13) {
            self.searchRadio();
        }
    };

    self.searchRadio = function(){
        self.results([]);
        self.api.get({
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
        self.api.laut.search(self.searchterm(), function(data) {
            if (data.results) {
                $.each(data.results, function(i, cat) {
                    $.each(cat.items, function(j, item) {
                        self.results.push(new stationModel(item.station));
                    });

                });
            }
        });
    };

    self.loadRecommendations = function(){
        self.api.raio.recommendations(function(data){
            console.log("recommendations success");
        });
    };

    self.playRadio = function(item){
        player.playRadio(item);
        self.currentRadio = item;
    };

    self.saveRadio = function () {
        self.api.post("saveRadio", "item=" + ko.toJSON(self.currentRadio), 
            function () {
                self.init();
        });
    };

    self.save = function (item) {
        self.api.post("addNew", "item=" + ko.toJSON(item), function () {
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
        self.api.post("addListenPls", "item=" + path, function () {
            self.init();
        });
    };
    self.saveStream = function (item) {
        self.api.post("saveStream", "item=" + ko.toJSON(item), function () {
        });
    };
    self.deleteStream = function (item) {
        self.api.post("deleteStream", "item=" + ko.toJSON(item), function () {
            self.streams.remove(item);
        });
    };

    self.activate = function () {
        
    };
}]);