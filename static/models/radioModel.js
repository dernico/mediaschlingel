
var radioModel = (function(){
	return function(station){
		var self = this;
		self.id = station.id;
        self.image = station.pictureBaseURL + station.picture1Name;
        self.name = station.name;
        self.genre = station.genresAndTopics;
        self.rank = station.rank;
	};
})();