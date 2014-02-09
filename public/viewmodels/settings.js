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

        self.grabcover = function(){
            api.get({action: "grabcover", params: ""});
        };

        self.pages = [
            {
                route: '#/settings/page1',
                vm: null,
                args: [],
                view: 'views/upload.html'
            },
            {
                route: '#/settings/page2',
                vm: null,
                args: [],
                view: 'views/test2.html'
            }
        ];
    };
})();
