var mediaListItemView = function(model){
    var tmpl = '<div class="tile">' +
        '<div class="tile-content" >' +
            '<div class="media-item" data-itemid="'+ model.id+'">' +
                '<p>' + model.artist + '</p>' +
                '<p>' + model.album + '</p>'+
                '<p>' + model.title + '</p>' +
            '</div>' +

            '<div class="tile-bottom">' +
                '<div class="vote display-'+ model.showVoting +'"'+
                    ' data-itemid="'+ model.id+'">' +
                    '<span>Play it next</span>' +
                '</div>'+
            '</div>'+
        '</div>'+
    '</div>';
    return tmpl;
};


var listvm = (function() {

    return function(data, player) {
        var self = this;
        self.api = data;
        self.player = player;

        self.media = {};
        self._searchfilter = "";
        self.searchfilter = function(filter){
            if(!filter){
                return self._searchfilter;
            }
            else{
                self._searchfilter = filter;
            }
        };


        self.activate = function() {
            self.searchBox = $("#search");
            self.medialist = $("#medialist");
            self.pageNext = $("#pageNext");
            self.pagePrev = $("#pagePrev");

            pageing.load();
            addPagingHandler();
            addSearchHandler();
        };


        var pageing = new pageingVM(self, "list", self.searchfilter, function(data){
            var view = "";
            self.media = {};
            data.forEach(function (item) {
                var model = new MusicFileModel(item);
                view += mediaListItemView(model);
                self.media[model.id] = model;
            });
            self.medialist.empty();
            self.medialist.append(view);
            appendClickHandler();
            appendVoteHandler();
        });

        self.search = pageing.search;
        self.count = pageing.count;
        self.from = pageing.from;
        self.to = pageing.to;

        var appendClickHandler = function() {
            $(".media-item").click(function (event) {
                var id = $(this).data("itemid");
                var playItem = self.media[id];
                self.play(playItem);
            });
        };

        var appendVoteHandler = function(){
            $(".vote").click(function(event){
                var id = $(this).data("itemid");
                self.voteit(id);
            });
        };

        var addPagingHandler = function() {
            self.pageNext.click(pageing.pageNext);
            self.pagePrev.click(pageing.pagePrev);
        };

        var addSearchHandler = function(){
            self.searchBox.bind("keyup", function(){
                self.searchfilter(self.searchBox.val());
                self.search();
            });
        };

        self.play = function (item) {
            self.player.play(item);
        };

        self.voteit = function (id) {
            self.api.get({
                action: "vote",
                params: "?id=" + id,
                success: function(){
                    item.showVoting(false);
                }
            });
        };

        self.searchOnEnter = function(vm,e) {
            if (e.keyCode == 13) {
                self.search();
            }
        };
    };
})();
