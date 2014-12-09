//var settingsvm = [function() {
pages.viewmodel("settingsvm",["api", function(api) {
    var self = this;
    self.shoutdown = function() {
        api.get({ action: "shutdown", params: "" });
    };
    self.crapShoutcast = function() {
        api.get({ action: "grapShoutcast", params: "" });
    };

    self.restart = function () {
        api.showLoading();
        setTimeout(function(){
            //window.location = window.location.origin;
            api.removeLoading();
        }, 4000);
        api.restartSchlingel();
    };

    self.discover = function () {
        api.get({ action: "discover", params: "" });
    };

    self.grabcover = function(){
        api.get({action: "grabcover", params: ""});
    };

    self.activate = function(){
    };
}]);
