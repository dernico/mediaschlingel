pages.viewmodel('youtube.searchVM', ['api', 'player', function(api, player){
	var self = this;
	self.searchTerm = ko.observable();
	self.results = ko.observableArray();

	self.searchOnEnter = function(vm, e){
		if(e.which == 13){
			self.search();
		}
	};

	self.search = function(){
		api.youtube.search(self.searchTerm(), function(result){
			self.results(result);
		});
	};

	self.play = function(track){
		player.playYouTube(track);
	};

}]);