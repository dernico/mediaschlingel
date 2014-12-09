var youtubeModel = (function(){
	return function(yt){
		var self = this;
		self.id = yt.id;
		self.thumbnail = yt.thumbnail;
		self.title = yt.title;
		self.showPlayNext = ko.observable(yt.showPlayNext);
	};
})();