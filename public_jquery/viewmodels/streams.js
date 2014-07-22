//var streams = ["api", "player", function (api, player) {
pages.viewmodel("streams", ["api", "player", function (api, player) {
    var self = this;
    self.activate = function () {
        $("#mypivot").pivot();
    };
}]);

