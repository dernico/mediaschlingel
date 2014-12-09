//var radioVM = ["api", "player", function (api, player) {
pages.viewmodel("mostWantedVM", ["api", "player", function (api, player) {
    var self = this;
    self.results = ko.observableArray([]);
    self.currentRadio = null;
    self.api = api;

    self.loadMostWanted = function(){
        self.api.radio.mostWanted(function(data){
            self.results(data);
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

    self.activate = function () {
    };

    self.loadMostWanted();
}]);