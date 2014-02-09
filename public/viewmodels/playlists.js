var playlistsvm = function(api) {
    var self = this;
    self.playlists = ko.observableArray();
    self.playlistItems = ko.observableArray();

    self.selectedPlaylist = ko.observable();
    self.searchfilter = ko.observable();

    ko.computed(function () {
        if(self.selectedPlaylist()){
            self.loadPlaylist();
        }
    });

    self.loadPlaylist = function(){

    };
    
    self.addNewPlaylist = function (item) {
        api.get({
            action: "addplaylist",
            params: "?playlist=" + item,
            success: function(){}
        });
    };

    self.activate = function() {
        paging.load();
    };

    self.searchOnEnter = function(vm,e) {
        if (e.keyCode == 13) {
            self.search();
        }
    };

    var paging = new pageingVM(self, "playlists", self.searchfilter, self.media);
    paging.load();

    self.search = paging.search;

    self.count = paging.count;
    self.from = paging.from;
    self.to = paging.to;
}