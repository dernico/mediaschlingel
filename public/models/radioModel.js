
var radioModel = (function(){
	return function(station){
		var self = this;
		self.id = station.id;
		self.description = station.description;
		self.stream = station.stream;
		self.format = station.format;
        self.image = station.image;
        self.name = station.name;
	};
})();