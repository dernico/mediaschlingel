
pages.viewmodel("deezerSearchVM", ["api", "player", function (api, player) {
    var self = this;
    self.api = api;

    self.query = ko.observable();
    self.searchResults = ko.observableArray([]);

    self.searchOnEnter = function(vm, e) {
        if (e.keyCode == 13) {
            self.search();
        }
    };

    self.search = function(){
        var query = self.query();
        api.deezer.search(query, handleSearchResult);
    };

    function handleSearchResult(result){
        self.searchResults(result.tracks);
    }

    self.play = function(item){
        //api.deezer.play(ko.toJSON(item));
        api.deezer.play(item.id, function(){
            alert("play");
        });
    };

}]);