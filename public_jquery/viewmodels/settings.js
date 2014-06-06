var settingsvm = (function() {


    return function() {
        var self = this;
        self.shoutdown = function() {
            api.get({ action: "shutdown", params: "" });
        };
        self.crapShoutcast = function() {
            api.get({ action: "grapShoutcast", params: "" });
        };

        self.refresh = function () {
            api.get({ action: "refreshData", params: "" });
        };

        self.discover = function () {
            api.get({ action: "discover", params: "" });
        };

        self.grabcover = function(){
            api.get({action: "grabcover", params: ""});
        };

        self.activate = function(){
            $("#mypivot").pivot();
            $("#myhub").hub();
        };
    };
})();
