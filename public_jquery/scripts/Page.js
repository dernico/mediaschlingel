
var Path = { version: "0.8.4", map: function (a) { if (Path.routes.defined.hasOwnProperty(a)) { return Path.routes.defined[a] } else { return new Path.core.route(a) } }, root: function (a) { Path.routes.root = a }, rescue: function (a) { Path.routes.rescue = a }, history: { initial: {}, pushState: function (a, b, c) { if (Path.history.supported) { if (Path.dispatch(c)) { history.pushState(a, b, c) } } else { if (Path.history.fallback) { window.location.hash = "#" + c } } }, popState: function (a) { var b = !Path.history.initial.popped && location.href == Path.history.initial.URL; Path.history.initial.popped = true; if (b) return; Path.dispatch(document.location.pathname) }, listen: function (a) { Path.history.supported = !!(window.history && window.history.pushState); Path.history.fallback = a; if (Path.history.supported) { Path.history.initial.popped = "state" in window.history, Path.history.initial.URL = location.href; window.onpopstate = Path.history.popState } else { if (Path.history.fallback) { for (route in Path.routes.defined) { if (route.charAt(0) != "#") { Path.routes.defined["#" + route] = Path.routes.defined[route]; Path.routes.defined["#" + route].path = "#" + route } } Path.listen() } } } }, match: function (a, b) { var c = {}, d = null, e, f, g, h, i; for (d in Path.routes.defined) { if (d !== null && d !== undefined) { d = Path.routes.defined[d]; e = d.partition(); for (h = 0; h < e.length; h++) { f = e[h]; i = a; if (f.search(/:/) > 0) { for (g = 0; g < f.split("/").length; g++) { if (g < i.split("/").length && f.split("/")[g].charAt(0) === ":") { c[f.split("/")[g].replace(/:/, "")] = i.split("/")[g]; i = i.replace(i.split("/")[g], f.split("/")[g]) } } } if (f === i) { if (b) { d.params = c } return d } } } } return null }, dispatch: function (a) { var b, c; if (Path.routes.current !== a) { Path.routes.previous = Path.routes.current; Path.routes.current = a; c = Path.match(a, true); if (Path.routes.previous) { b = Path.match(Path.routes.previous); if (b !== null && b.do_exit !== null) { b.do_exit() } } if (c !== null) { c.run(); return true } else { if (Path.routes.rescue !== null) { Path.routes.rescue() } } } }, listen: function () { var a = function () { Path.dispatch(location.hash) }; if (location.hash === "") { if (Path.routes.root !== null) { location.hash = Path.routes.root } } if ("onhashchange" in window && (!document.documentMode || document.documentMode >= 8)) { window.onhashchange = a } else { setInterval(a, 50) } if (location.hash !== "") { Path.dispatch(location.hash) } }, core: { route: function (a) { this.path = a; this.action = null; this.do_enter = []; this.do_exit = null; this.params = {}; Path.routes.defined[a] = this } }, routes: { current: null, root: null, rescue: null, previous: null, defined: {} } }; Path.core.route.prototype = { to: function (a) { this.action = a; return this }, enter: function (a) { if (a instanceof Array) { this.do_enter = this.do_enter.concat(a) } else { this.do_enter.push(a) } return this }, exit: function (a) { this.do_exit = a; return this }, partition: function () { var a = [], b = [], c = /\(([^}]+?)\)/g, d, e; while (d = c.exec(this.path)) { a.push(d[1]) } b.push(this.path.split("(")[0]); for (e = 0; e < a.length; e++) { b.push(b[b.length - 1] + a[e]) } return b }, run: function () { var a = false, b, c, d; if (Path.routes.defined[this.path].hasOwnProperty("do_enter")) { if (Path.routes.defined[this.path].do_enter.length > 0) { for (b = 0; b < Path.routes.defined[this.path].do_enter.length; b++) { c = Path.routes.defined[this.path].do_enter[b](); if (c === false) { a = true; break } } } } if (!a) { Path.routes.defined[this.path].action() } } };


var pages = {};
pages.constructed = {};

pages.viewmodels = {};
pages.services = {};
pages.servicesSingelton = {};


pages.viewmodel = function(name, vm){
    pages.viewmodels[name] = vm;
};

pages.service = function(name, service){
    pages.services[name] = service;
};

pages.loadControls = function(element){
        
    var items = element.find("[data-control='pivot']");
    if(items.length > 0){
        items.pivot();
    }

    items = element.find("[data-control='page']");
    if(items.length > 0){
        //items.page();
        for(var i = 0; i < items.length; i++){
            $(items[i]).page();
        }
    }

};

function getObjectFromString(item){
    var splited = item.split(".");
    var obj = null;

    splited.forEach(function(s){
        var test = obj ? obj[s] : window[s];
        if(test){
            obj = test;
        }
    });
    return obj;
}

function isArray(obj) {
    if (Object.prototype.toString.call(obj) === '[object Array]') {
        return true;
    }
    return false;
}

function constructService(serviceToConstruct){

    if(pages.servicesSingelton[serviceToConstruct]){
        return pages.servicesSingelton[serviceToConstruct];
    }

    var service = pages.services[serviceToConstruct];
    if(!service){
        console.log("Could not find Service with name: " + serviceToConstruct);
        return;
    }
    pages.servicesSingelton[serviceToConstruct] = construct(service);
    return pages.servicesSingelton[serviceToConstruct];
}

function constructVM(vmToConstruct){
    var vm = pages.viewmodels[vmToConstruct];
    if(!vm){
        console.log("No ViewModel found with name: " + vmToConstruct);
        return;
    }
    return construct(vm)
}

function construct(objToConstruct){

    var convertedArgs = [];
    var args = [];

    
    if (isArray(objToConstruct)) {
        if (objToConstruct.length > 1) {
            for (var i = 0; i < objToConstruct.length - 1; i++) {
                args.push(objToConstruct[i]);
            }
        }
        objToConstruct = objToConstruct[objToConstruct.length - 1];
    }

    args.forEach(function(item){
        var service = constructService(item);
        convertedArgs.push(service);

    });

    function F() { return objToConstruct.apply(this, convertedArgs); };
    F.prototype = objToConstruct.prototype;
    return new F();
}

function parseOptions(json){
    if(!json) return {};
    if(json.indexOf("{") != 1){
        json = "{" + json + "}";
    }
    json = json.replace(/\'/g, '"');
    json = json.replace(/(\w+)\s*:/g, '"$1":');
    return JSON.parse(json);
}


(function( $ ) {
 
    $.fn.pages = function( options ) {
        var self = this;
        self.root = $(self);
        var settings = $.extend({
            // These are the defaults.
            pages: [],
            transitionTimeout: 1000,
            //time2wait: 1000,
            backgroundColor: "white"
        }, options );

        var transitionTimeout = 0;
        settings.pages.forEach(function(page){

            Path.map(page.route)
            .enter(function () {})
            .exit(function () {

                self.root.css("animation", "page_leave_sequence " + settings.transitionTimeout + "ms linear");
                //self.root.removeClass('page-enter');
                //self.root.addClass('page-leave');

                /*
                self.root.removeClass('animated fadeOutLeft');
                self.root.removeClass('animated fadeInRight');
                self.root.addClass('animated fadeOutLeft');
                */
            })
            .to(function () {
                var params = this.params;

                setTimeout(function () {
                    transitionTimeout = settings.transitionTimeout;
                    loadCurrentPage(page, params);

                    self.root.css("animation", "page_enter_sequence " + settings.transitionTimeout + "ms linear");
                    //self.root.removeClass('page-leave');
                    //self.root.removeClass('page-enter');
                    //self.root.addClass('page-enter');

                }, transitionTimeout);

                /*
                setTimeout(function () {
                    settings.timeout = settings.time2wait;
                    loadCurrentPage(page, params);
                    self.root.removeClass('animated fadeOutLeft');
                    self.root.removeClass('animated fadeInRight');
                    self.root.addClass('animated fadeInRight');

                }, settings.timeout);
                */
            });
        });


        var loadCurrentPage = function(page, params){
            page.params = params;
            self.root.page(page);
        }

        var firstPage = settings.pages[0];
        Path.root(firstPage.route);
        Path.listen();

        return self;
    };
 
}( jQuery ));

pages.uniqueId = function(el){
    var id = el.attr("id");
    if(id === undefined){
        var id = new Date().getTime();
        el.attr("id", id);
    };
    return id;
};

(function( $ ) {
 
    $.fn.page = function( settings ) {
        var self = this;
        self.root = $(self);
        
        var dataOptions = self.root.data("options");
        if(!settings && typeof dataOptions === "string"){
            dataOptions = parseOptions(dataOptions);
        }
        else{
            dataOptions = settings;
        }

        self.options = dataOptions;

        if(self.options === undefined){
            console.log("options not set for element " + self);
            return;
        }

        var loadView = function () {

            if (self.options.view && !self.options._view) {
                $.ajax({
                    url: self.options.view
                })
                .done(function (pageContent) {
                    self.options._view = pageContent;
                    self.activateVM();
                })
                .error(function (err) {
                    //Todo handle Errorcodes here!
                    //if (err) error(err);
                    console.log(err);
                });
            } else {
                self.activateVM();
            }
        };

        self.activateVM = function() {
            if(self.options._view){
                self.root.empty();
                self.root.append(self.options._view);
            }
            
            if (!self.options._vm && self.options.vm) {

                self.options._vm = constructVM(self.options.vm);//,self.options.args);
            }
            
            if (self.options._vm !== undefined){
                if(self.options._vm.activate){
                    self.options._vm.activate(self.options.params, self.root[0]);
                }

                if(window["ko"] !== undefined){
                    ko.applyBindings(self.options._vm, self.root[0]);
                }
            }
            pages.loadControls(self.root);
        };

        loadView();

        return self;
    }

})( jQuery );

(function( $ ) {
 
    $.fn.pivot = function( ) {
        var self = this;
        self.root = $(self);
        self.header = null;
        self.container = null;
        self.loadedPages = {};
        self.currentPage = null;
        
        //self.root.width($(window).width());
        

        self.pivotItems = [];
        self.children = self.root.children();
        for(var i = 0; i < self.children.length; i++){
            var child = $(self.children[i]);
            var options = child.data("options");
            var title = child.data("title");

            var pivotItem = {
                title: title ? title : "Item " + i,
                options: parseOptions(options),
                el: child.context.outerHTML
            };

            self.pivotItems.push(pivotItem);
        };

        var loadPage = function(index){
            var pivotitem = self.pivotItems[index];
            self.container.empty();

            //create a new pivot page
            if(!pivotitem.page){
                
                self.container.append(pivotitem.el);
                var pivotElement = $(self.container.children()[0]);
                pivotitem.page = pivotElement.page(pivotitem.options);

                //todo: find way to remove setTimeout
                setTimeout(function(){
                    pivotElement.addClass('animation pivot-enter');
                    pivotitem.html = pivotElement.html();
                }, 10);

            //append an existing pivot page
            }else{
                //set timeout to prevent a bloping effect
                setTimeout(function(){
                    self.container.append(pivotitem.page);
                    pivotitem.page.activateVM();
                }, 320);
            }            
        };

        var addContainer = function(){
            self.root.append('<div class="pivot-container"></div>');
            self.container = $(".pivot-container");
        };

        var addHeader = function(){
            var header = "<ul class='pivot-header'>";
            for(var i = 0; i < self.pivotItems.length; i++){
                var item = self.pivotItems[i];
                header += "<li class='pivot-header-item' data-index='" + i + "'>";
                header += "<a>"+ item.title + "</a>";
                header += "</li>"; 
            }
            header += "</ul>";
            self.root.append(header);
            $(".pivot-header-item").click(handleTitleClick);
        };

        var handleTitleClick = function(){
            var title = $(this);
            var listIndex = title.index();
            if(listIndex === 0) return;

            var paddingLeft = title.position().left;
            var parent = title.parent();
            var index = title.data("index");

            loadPage(index);

            var childs = parent.children();
            for(var i = 0; i < listIndex; i++){
                var child = $(childs[i]);
                child.addClass("transition-margin-left");
                child.css("margin-left", "-" + child.width() + "px");
            }
            
            setTimeout(function(){
                for(var i = 0; i < listIndex; i++){
                    var child = $(childs[i]);
                    child.removeClass("transition-margin-left");
                    child.appendTo(parent);
                    child.css("margin-left", "0px");
                }
            },300);
        };

        self.root.empty();
        addHeader();
        addContainer();
        loadPage(0);
        return self;
    }

})( jQuery );

(function( $ ) {
 
    $.fn.hub = function( settings ) {
        var self = this;
        self.root = $(self);
        self.options = {};

        var dataOptions = self.root.data("options");
        if(dataOptions){
            self.options = $.extend(self.options, dataOptions );
        }
        self.options = $.extend(self.options, settings);

        self.hubItems = [];
        self.children = self.root.children();
        for(var i = 0; i < self.children.length; i++){
            var child = $(self.children[i]);
            var options = child.data("options");
            var title = child.data("title");

            var hubItem = {
                title: title ? title : "Item " + i,
                options: parseOptions(options),
                el: child.context.outerHTML
            };
            self.hubItems.push(hubItem);
        };

        var loadPages = function(){
            for(var i = 0; i < self.hubItems.length; i++){
                var hubItem = self.hubItems[i];
                var hubElement = "<div class='hubitem-container'>";
                if(hubItem.title){
                    hubElement += "<div class='hubitem-title'>";
                    hubElement += "<h2>";
                    hubElement += hubItem.title;
                    hubElement += "</h2>";
                    hubElement += "</div>";
                }
                hubElement += "<div class='hubitem-content'>";
                hubElement += hubItem.el;
                hubElement += "</div>";
                self.root.append(hubElement);
            }

            var hubElements = $(".hubitem-content");
            for(var i = 0; i < hubElements.length; i++){
                $(hubElements[i]).page(self.hubItems[i].options);
            }
        };

        var handleTitleClick = function(){
            var index = $(this).data("index");
            
        };

        self.root.empty();
        loadPages();

        return self;
    }

})( jQuery );



$(document).ready(function(){
    pages.loadControls($("body"));
});