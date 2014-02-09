function pageingVM(vm, url, observableFilter, observableData){

    var ScrollTop = function () { window.scrollTo(0, 0) };
    var self = this;
    //Paging stuff
    var pageIndex = ko.observable(0);
    var pageSize = 10;
    self.count = ko.observable();
    self.from = ko.observable();
    self.to = ko.observable();

    /*vm.resetPage = function () {
        pageIndex( 0 );
    };*/

    vm.pageNext = function () {
        if(observableData().length >= pageSize){
            pageIndex(pageIndex() + 1);
            self.load();
            ScrollTop();
        }
    };

    vm.pagePrev = function () {
        if(pageIndex() > 0){
            pageIndex(pageIndex() - 1);
            self.load();
            addStreamcrollTop();
        }
    };

    var getParams = function () {
        var params = "";
        var filter = "";
        if (observableFilter()) {
            filter = observableFilter();
        }
        params = "?filter=" + filter
                + "&top=" + pageSize + "&skip=" + (pageIndex() * pageSize);
        return params;
    };


    self.load = function () {
        api.get({
            action: url,
            params: getParams(),
            success: loadSuccess,
            error: function(){
                alert("Error");
            }
        });
    };

    self.search = function() {
        api.get({
            action: url,
            params: getParams(),
            success: loadSuccess,
            showLoading: false
        });
    };

    var loadSuccess = function (data) {
        observableData([]);
        vm.count(data.count);

        if (data.list) {
            var from = pageIndex() * pageSize;
            var to = data.list.length >= pageSize
                    ? from + pageSize : from + data.list.length;
            vm.from(from);
            vm.to(to);
            data.list.forEach(function(item) {
                //self.addStream(item);
                observableData.push(new MusicFileModel(item));
            });
        }
    };
}
