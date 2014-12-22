pages.viewmodel("categoriesVM", ["api", "player", function (api, player) {
    var self = this;
    self.categories = ko.observableArray([]);
    self.stations = ko.observableArray([]);
    self.currentRadio = null;
    self.api = api;

    self.categoriesVisible = ko.observable(true);

    self.toggleCategories = function(){
        var newState = !self.categoriesVisible();
        self.categoriesVisible(newState);
    };

    self.loadCategories = function(){
        self.api.radio.categories('genre',function(data){
            self.categories(data.categories);
        });
    };

    self.loadByCategorie = function(categorie){
        self.categoriesVisible(false);

        self.api.radio.bycategorie('genre', categorie, function(data){
            self.stations(data);
            //$("img").unveil();
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

    self.loadCategories();
}]);