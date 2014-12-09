pages.viewmodel('youtube.playlistVM', ['api', 'player', function(api, player){
	var self = this;
	self.results = ko.observableArray();

	self.searchOnEnter = function(vm, e){
		if(e.which == 13){
			self.search();
		}
	};

	self.play = function(track){
		player.playYouTube(track, function(){
			api.youtube.related(track, self.activate);
		});
	};

	var handleResult = function(result){
		self.results(result.playlist);
	};


	self.activate = function(){
		api.youtube.getPlaylist(handleResult);
	};

}]);