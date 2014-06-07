var stationModel = (function() {

    return function(station) {
        var self = this;
        self.stream = station.stream_url;
        self.image = station.images.station_80x80;
        self.format = station.format;
        self.name = station.name;
        self.website = station.website;
        self.description = station.description;
    };

})();

var radioModel = (function(){
	return function(station){
		var self = this;
		self.id = station.id;
        self.image = station.pictureBaseURL + station.picture1Name;
        self.name = station.name;
        self.genre = station.genresAndTopics;
	};
})();

