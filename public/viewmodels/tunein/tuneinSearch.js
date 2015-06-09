pages.viewmodel("tuneinSearchVM", ["api", "player", function (api, player) {
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
        self.api.tunein.search(self.searchterm(), function(results){
            self.results(results);
        });
    };
    

    self.playRadio = function(item){
        self.api.tunein.play(ko.toJSON(item), player.setCurrentInfo);
        self.currentRadio = item;
    };

    self.saveRadio = function (item) {
        self.api.tunein.saveRadio(ko.toJSON(item));
    };


    self.loadRecommendations = function(){
        self.api.radio.recommendations(function(data){
            console.log("recommendations success");
        });
    };

    self.activate = function () {
        
    };
}]);