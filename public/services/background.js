//var backgroundVM = [function(){
pages.service("background", function(){
	var self = this;
	self.Cover = ko.observable();

	self.setCover = function(cover){

		if(cover){
			if(cover.indexOf("http") != -1){
				self.Cover(getCoverUrl(cover));
			}
			else{
				self.Cover(getCoverUrl('Cover/' + cover));
			}
		}else{
			self.Cover(getCoverUrl("/schlingel.jpg"));
		}
	};

	var getCoverUrl = function(cover){
		return "url(" + cover + ")"
	};

});