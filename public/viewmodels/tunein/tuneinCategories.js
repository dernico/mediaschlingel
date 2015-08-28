pages.viewmodel("tuneinCategoriesVM", ["api", "player", function (api, player) {
    var self = this;
    self.categories = ko.observableArray([]);
    self.results = ko.observableArray([]);
    self.currentRadio = null;
    self.api = api;
    self.player = player;

    
    self.opencategorie = function(item){

        self.api.tunein.stations(item.guide_id, function(results){
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


    self.activate = function () {
        
        self.categories([]);
        self.api.tunein.categories("music", function(results){
            self.categories(results);
        });

    };
}]);