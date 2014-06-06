function pageingVM(vm, url, filter, callback){

    var ScrollTop = function () { window.scrollTo(0, 0); };
    var self = this;
    var pageIndex = 0;
    var pageSize = 10;
    var currentDataCount = 0;
    self.count = null;
    self.from = null;
    self.to = null;

    var getParams = function () {
        var params = "";
        var _filter = filter();
        if (_filter === undefined) {
            _filter = "";
        }
        params = "?filter=" + _filter + 
                    "&top=" + pageSize + "&skip=" + (pageIndex * pageSize);
        return params;
    };

    self.pageNext = function () {
        if(currentDataCount >= pageSize){
            pageIndex = pageIndex + 1;
            self.load();
            ScrollTop();
        }
    };

    self.pagePrev = function () {
        if(pageIndex > 0){
            pageIndex = pageIndex - 1;
            self.load();
        }
    };

    self.load = function () {
        api.get({
            action: url,
            params: getParams(),
            success: loadSuccess,
            showLoading: false,
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
        vm.count = data.count;

        if (data.list) {
            currentDataCount = data.list.length;
            var from = pageIndex * pageSize;
            var to = data.list.length >= pageSize ? 
                        from + pageSize : from + data.list.length;
            vm.from = from;
            vm.to = to;
            if(callback){
                callback(data.list);
            }
        }
    };
}
