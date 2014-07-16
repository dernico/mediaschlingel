var backgroundVM = [function(){

	var self = this;
	self.Cover = ko.observable();

	self.setCover = function(cover){

		if(cover){
			if(cover.indexOf("http") != -1){
				self.Cover(cover);
			}
			else{
				self.Cover('Cover/' + cover);
			}
		}else{
			self.Cover("/schlingel.jpg");
		}
	};

}];