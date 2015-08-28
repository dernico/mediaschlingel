pages.viewmodel("tuneinTrendingVM", ["api", "player", function (api, player) {
    var self = this;
    self.results = ko.observableArray([]);
    self.currentRadio = null;
    self.api = api;


    self.playRadio = function(item){
        self.api.tunein.play(ko.toJSON(item), player.setCurrentInfo);
        self.currentRadio = item;
    };

    self.saveRadio = function (item) {
        self.api.tunein.saveRadio(ko.toJSON(item));
    };


    self.activate = function () {
        
        self.results([]);
        self.api.tunein.categories("trending", function(results){
            self.results(results);
        });

    };
}]);