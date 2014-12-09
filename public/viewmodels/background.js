//var backgroundVM = [function(){
pages.viewmodel("backgroundVM", ['background',function(backgroundService){
	var self = this;
	self.Cover = backgroundService.Cover;
	backgroundService.setCover();
}]);