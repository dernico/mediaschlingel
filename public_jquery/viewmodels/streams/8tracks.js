var tracksVM = ["api", "player", function (api, player) {
    var self = this;
    self.api = api;
    self.searchTerm = ko.observable();
    self.tracksResult = ko.observableArray([]);

    self.tagCloud = [
        {title: "Popular", tag: "all:popular"},
        {title: "Hip Hop", tag: "tags:hip_hop"},
        {title: "Alternative", tag: "tags:alternative"},
        {title: "Electro", tag: "tags:electro"},
        {title: "80s", tag: "tags:80s"}
    ];

    self.selectedTag = ko.observable();

    self.pageing = ko.observable();


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

    self.pagePrev = function(){
        self.api.tracks.page(self.pageing().prevPage,handleMixes);
    };

    self.pageNext = function(){
        self.api.tracks.page(self.pageing().nextPage, handleMixes);
    };

    self.tagClick = function(tag){
        self.selectedTag(tag);
        self.api.tracks.tags(tag.tag, handleMixes);
    };

    self.loadPopular = function(){
        var tag = self.tagCloud[0];
        self.selectedTag(tag)
        self.tagClick(tag);
    };

    self.searchOnEnter = function(self, e){
        if(e.which != 13 ) return;
        self.search();
    };

    self.search = function(){
        self.api.tracks.search(self.searchTerm(), handleMixes);
    };

    self.play = function(mix){
        //console.log(mix);
        player.playTracks(mix);
    };

    self.activate = function () {
    };

    self.loadPopular();
}];