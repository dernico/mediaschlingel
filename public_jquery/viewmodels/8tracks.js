//var tracksVM = ["api", "player", function (api, player) {
pages.viewmodel("tracksVM", ["api", "player", function (api, player) {
    var self = this;
    self.api = api;
    self.searchTerm = ko.observable();
    self.tracksResult = ko.observableArray([]);

    self.currentTag = "";
    self.choosenSorting = ko.observable("popular");

    self.sorting = [
        {title: "Popular", value: "popular"},
        {title: "Trending", value: "hot"},
        {title: "Newest", value: "recent"}
    ];

    self.tagCloud = [
        {title: "Popular", tag: "all", name: "popular"},
        {title: "Charts", tag: "tags:charts", name: "charts"},
        {title: "Hip Hop", tag: "tags:hip_hop", name: "hip_hop"},
        {title: "Underground", tag: "tags:underground", name: "underground"},
        {title: "Rap", tag: "tags:rap", name: "rap"},
        {title: "Classic", tag: "tags:classic", name: "classic"},
        {title: "Funk", tag: "tags:funk", name: "funk"},
        {title: "Jazz", tag: "tags:jazz", name: "jazz"},
        {title: "Alternative", tag: "tags:alternative", name: "alternative"},
        {title: "House", tag: "tags:house", name: "house"},
        {title: "Electro", tag: "tags:electro", name: "electro"},
        {title: "Dupstep", tag: "tags:dupstep", name: "dupstep"},
        {title: "Chill", tag: "tags:chill", name: "chill"},
        {title: "2000s", tag: "tags:2000s", name: "2000s"},
        {title: "90s", tag: "tags:90s", name: "90s"},
        {title: "80s", tag: "tags:80s", name: "80s"}
    ];

    self.selectedTags = ko.observableArray();

    self.pageing = ko.observable();


    self.choosenSorting.subscribe(function(newVal){
        //sendTag(self.currentTag);
        explore();
    });

    var handleMixes = function(data, err){
        if(!data || err) return;


        var mixes = data.mixes;
        var pageing = data.pageing;

        self.pageing({
            currentPage: pageing.currentPage,
            nextPage: pageing.nextPage,
            prevPage: pageing.prevPage,
            mixCount: pageing.totalMixes,
            pageCount: pageing.totalPages
        });

        self.tracksResult(mixes);
    };

    var sendTag = function(tag){
        self.currentTag = tag;
        tag += ":" + self.choosenSorting();
        self.api.tracks.tags(tag, handleMixes);
    };

    var explore = function(){
        var exploreTags = [];
        self.selectedTags().forEach(function(tag){
            exploreTags.push(tag.name);
        });
        var tag = "";
        if(exploreTags.length > 0){
            var explorer = exploreTags.join("+");
            tag += "tags:"+explorer;
            tag += ":" + self.choosenSorting();
        }else{
            tag += "all:" + self.choosenSorting();
        }
        self.api.tracks.tags(tag, handleMixes);
    };

    function toUrlParam(param) {
        if (param) {
            return encodeURIComponent(param.replace(/_/g, '__').replace(/\s/g, '_').replace(/\//g, '\\').replace(/\./g, '^'));
        }
    }

    self.pagePrev = function(){
        self.api.tracks.page(self.pageing().prevPage,handleMixes);
    };

    self.pageNext = function(){
        self.api.tracks.page(self.pageing().nextPage, handleMixes);
    };

    self.tagClick = function(tag){
        self.selectedTags.push(tag);
        explore();
    };

    self.removeTag = function(tag){
        self.selectedTags.remove(tag);
        if(self.selectedTags().length === 0){
            self.loadPopular();
        }else{
            explore();
        }
    };

    self.loadPopular = function(){
        var tag = self.tagCloud[0];
        sendTag(tag.tag);
    };

    self.searchOnEnter = function(self, e){
        if(e.which != 13 ) return;
        self.search();
    };

    self.search = function(){
        var searchTerm = toUrlParam(self.searchTerm());
        //var searchTag = "keyword:" + searchTerm;
        var searchTag = "artist:" + searchTerm;
        sendTag(searchTag);
        //self.api.tracks.tags(searchTag, handleMixes);
        //self.api.tracks.search(self.searchTerm(), handleMixes);
    };

    self.play = function(mix){
        //console.log(mix);
        player.playTracks(mix);
    };

    self.activate = function () {
    };

    self.loadPopular();
}]);