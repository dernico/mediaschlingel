var listvm = (function() {

    return function(api, player) {
        var self = this;
        self.playinfo = ko.observable();
        self.searchfilter = ko.observable();

        ko.computed(function () {
            if(self.resetPage) self.resetPage();
            var filter = self.searchfilter();
            if(self.search) self.search();
        });

        self.media = ko.observableArray();
        
        self.play = function (item) {
            player.play(item);
        };

        self.voteit = function (item) {
            api.get({
                action: "vote",
                params: "?id=" + item.id,
                success: function(){
                    item.showVoting(false);
                }
            });
            /*api.post("voteit", "id=" + ko.toJSON(item),function(data) {
                var mf = new MusicFileModel(data);
                item.votes(mf.votes());
            });*/
        };

        self.setplayinfo = function(data) {
            var playinfo = {
                artist: unescape(data.artist),
                title: unescape(data.title),
                duration: data.duration,
                elapsed: data.elapsed
            };
            self.playinfo(playinfo);
        };


        self.canActivate = function() {
            return true;
        };

        self.activate = function() {
            paging.load();
        };

        self.searchOnEnter = function(vm,e) {
            if (e.keyCode == 13) {
                self.search();
            }
        };

        var paging = new pageingVM(self, "list", self.searchfilter, self.media);
        paging.load();

        self.search = paging.search;

        self.count = paging.count;
        self.from = paging.from;
        self.to = paging.to;
    };
})();
