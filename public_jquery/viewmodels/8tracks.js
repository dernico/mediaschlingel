var tracksVM = ["api", "player", function (api, player) {
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
        {title: "Popular", tag: "all"},
        {title: "Charts", tag: "tags:charts"},
        {title: "Hip Hop", tag: "tags:hip_hop"},
        {title: "Alternative", tag: "tags:alternative"},
        {title: "House", tag: "tags:house"},
        {title: "2000s", tag: "tags:2000s"},
        {title: "90s", tag: "tags:90s"},
        {title: "80s", tag: "tags:80s"}
    ];

    self.selectedTag = ko.observable();

    self.pageing = ko.observable();


    self.choosenSorting.subscribe(function(newVal){
        sendTag(self.currentTag);
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

    self.pagePrev = function(){
        self.api.tracks.page(self.pageing().prevPage,handleMixes);
    };

    self.pageNext = function(){
        self.api.tracks.page(self.pageing().nextPage, handleMixes);
    };

    self.tagClick = function(tag){
        self.selectedTag(tag);
        sendTag(tag.tag);
    };

    self.loadPopular = function(){
        var tag = self.tagCloud[0];
        self.selectedTag(tag);
        self.tagClick(tag);
    };

    self.searchOnEnter = function(self, e){
        if(e.which != 13 ) return;
        self.search();
    };

    self.search = function(){
        //var searchTag = "keyword:" + self.searchTerm();
        var searchTag = "artist:" + self.searchTerm();
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
}];