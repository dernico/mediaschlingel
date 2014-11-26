pages.viewmodel('youtube.searchVM', ['api', 'player', function(api, player){
	var self = this;
	self.searchTerm = ko.observable();
	self.results = ko.observableArray();
	self.nextPageToken = null;
	self.prevPageToken = null;
	self.showPaging = ko.observable(false);

	self.searchOnEnter = function(vm, e){
		if(e.which == 13){
			self.search();
		}
	};

	var handleResult = function(result){
		if(result.nextPageToken){
			self.nextPageToken = result.nextPageToken;
		}
		if(result.prevPageToken){
			self.prevPageToken = result.prevPageToken;
		}
		self.results(result.tracks);
	};

	self.search = function(){
		var data = {search: self.searchTerm()};
		api.youtube.search(data, handleResult);
		self.showPaging(true);
	};

	self.play = function(track){
		player.playYouTube(track, function(){
			api.youtube.related(track, handleResult);
			self.showPaging(false);
		});
	};

	self.playNext = function(track){
		api.youtube.addPlaylist(track, function(){
			track.showPlayNext(false);
		});
	};

	self.pagePrev = function(){
		var data = {
			search: self.searchTerm()
		};
		if(self.prevPageToken){
			data.pageToken = self.prevPageToken;
		}
		api.youtube.search(data, handleResult);
	};

	self.pageNext = function(){
		var data = {search: self.searchTerm()};
		if(self.nextPageToken){
			data.pageToken = self.nextPageToken;
		}
		api.youtube.search(data, handleResult);
	};

}]);