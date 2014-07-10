
var listvm = ["api", "player", function(data, player) {

    var self = this;
    self.api = data;
    self.activated = false;
    self.playinfo = ko.observable();
    self.searchfilter = ko.observable("");


    self.searchTimeoutID = null;
    self.media = ko.observableArray();
    self.count = ko.observable();
    self.from = ko.observable();
    self.to = ko.observable();
    
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
        self.activated = true;
        pageing.load();
    };

    self.searchOnEnter = function(vm,e) {
        if (e.keyCode == 13) {
            pageing.search();
        }
    };

    var pageing = new pageingVM(self.api, "list", function(data){
        self.media([]);
        self.count(pageing.count);
        self.from(pageing.from);
        self.to(pageing.to);
        data.forEach(function(item) {
            self.media.push(new MusicFileModel(item));
        });
    });

    self.pagePrev = pageing.pagePrev;
    self.pageNext = pageing.pageNext;



    self.searchfilter.subscribe(function(oldval,newval){
        if(self.activated){

            if(self.resetPage) self.resetPage();

            
            if(self.searchTimeoutID){
                clearTimeout(self.searchTimeoutID);
            }
            self.searchTimeoutID = setTimeout(function(){

                pageing.searchfilter(self.searchfilter());
                //if(pageing.search) pageing.search();
            }, 1000);
        }
    });

    //ko.computed(function () {
    //});

}];

/*var mediaListItemView = function(model){
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


var listvm = ["api", "player", function(data, player) {
    var self = this;
    self.api = data;
    self.player = player;

    self.media = {};

    self.activate = function() {
        self.searchBox = $("#search");
        self.medialist = $("#medialist");
        self.pageNext = $(".pageNext");
        self.pagePrev = $(".pagePrev");
        self.pageFromText = $(".pageFromText");
        self.pageToText = $(".pageToText");
        self.pageCountText = $(".pageCountText");

        pageing.load();
        addPagingHandler();
        addSearchHandler();
    };


    var pageing = new pageingVM(self.api, "list", function(data){
        var view = "";
        self.media = {};
        data.forEach(function (item) {
            var model = new MusicFileModel(item);
            view += mediaListItemView(model);
            self.media[model.id] = model;
        });
        self.medialist.empty();
        self.medialist.append(view);
        self.pageFromText.text(pageing.from);
        self.pageToText.text(pageing.to);
        self.pageCountText.text(pageing.count);

        appendMediaItemClickHandler();
        appendVoteHandler();
    });

    var addPagingHandler = function() {
        self.pageNext.click(pageing.pageNext);
        self.pagePrev.click(pageing.pagePrev);
    };

    var appendMediaItemClickHandler = function() {
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

    var addSearchHandler = function(){
        self.searchBox.bind("keyup", function(){
            pageing.searchfilter(self.searchBox.val());
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
            pageing.search();
        }
    };
}];
*/