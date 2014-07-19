var settingsvm = [function() {

    var self = this;
    self.shoutdown = function() {
        api.get({ action: "shutdown", params: "" });
    };
    self.crapShoutcast = function() {
        api.get({ action: "grapShoutcast", params: "" });
    };

    self.restart = function () {
        setTimeout(function(){
            window.location = window.location.origin;
        }, 800);
        api.restartSchlingel();
    };

    self.discover = function () {
        api.get({ action: "discover", params: "" });
    };

    self.grabcover = function(){
        api.get({action: "grabcover", params: ""});
    };

    self.activate = function(){
        //$("#mypivot").pivot();
        //$("#myhub").hub();
    };
}];
