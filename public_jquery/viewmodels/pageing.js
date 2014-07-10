function pageingVM(api, url, callback){

    var ScrollTop = function () { window.scrollTo(0, 0); };
    var self = this;
    var pageIndex = 0;
    var pageSize = 10;
    var currentDataCount = 0;
    self.api = api;
    self._searchfilter = "";
    self.searchfilter = function(filter){
        if(!filter){
            return self._searchfilter;
        }
        else{
            self._searchfilter = filter;
            self.search();
        }
    };
    self.count = null;
    self.from = null;
    self.to = null;

    var getParams = function () {
        var params = "";
        params = "?filter=" + self.searchfilter() + 
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
        self.api.get({
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
        self.api.get({
            action: url,
            params: getParams(),
            success: loadSuccess,
            showLoading: false
        });
    };

    var loadSuccess = function (data) {
        if (data.list) {
            self.count = data.count;
            currentDataCount = data.list.length;
            var from = pageIndex * pageSize;
            var to = data.list.length >= pageSize ? 
                        from + pageSize : from + data.list.length;
            self.from = from;
            self.to = to;
            if(callback){
                callback(data.list);
            }
        }
    };
}
