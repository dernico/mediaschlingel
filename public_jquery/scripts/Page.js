
var Path = { version: "0.8.4", map: function (a) { if (Path.routes.defined.hasOwnProperty(a)) { return Path.routes.defined[a] } else { return new Path.core.route(a) } }, root: function (a) { Path.routes.root = a }, rescue: function (a) { Path.routes.rescue = a }, history: { initial: {}, pushState: function (a, b, c) { if (Path.history.supported) { if (Path.dispatch(c)) { history.pushState(a, b, c) } } else { if (Path.history.fallback) { window.location.hash = "#" + c } } }, popState: function (a) { var b = !Path.history.initial.popped && location.href == Path.history.initial.URL; Path.history.initial.popped = true; if (b) return; Path.dispatch(document.location.pathname) }, listen: function (a) { Path.history.supported = !!(window.history && window.history.pushState); Path.history.fallback = a; if (Path.history.supported) { Path.history.initial.popped = "state" in window.history, Path.history.initial.URL = location.href; window.onpopstate = Path.history.popState } else { if (Path.history.fallback) { for (route in Path.routes.defined) { if (route.charAt(0) != "#") { Path.routes.defined["#" + route] = Path.routes.defined[route]; Path.routes.defined["#" + route].path = "#" + route } } Path.listen() } } } }, match: function (a, b) { var c = {}, d = null, e, f, g, h, i; for (d in Path.routes.defined) { if (d !== null && d !== undefined) { d = Path.routes.defined[d]; e = d.partition(); for (h = 0; h < e.length; h++) { f = e[h]; i = a; if (f.search(/:/) > 0) { for (g = 0; g < f.split("/").length; g++) { if (g < i.split("/").length && f.split("/")[g].charAt(0) === ":") { c[f.split("/")[g].replace(/:/, "")] = i.split("/")[g]; i = i.replace(i.split("/")[g], f.split("/")[g]) } } } if (f === i) { if (b) { d.params = c } return d } } } } return null }, dispatch: function (a) { var b, c; if (Path.routes.current !== a) { Path.routes.previous = Path.routes.current; Path.routes.current = a; c = Path.match(a, true); if (Path.routes.previous) { b = Path.match(Path.routes.previous); if (b !== null && b.do_exit !== null) { b.do_exit() } } if (c !== null) { c.run(); return true } else { if (Path.routes.rescue !== null) { Path.routes.rescue() } } } }, listen: function () { var a = function () { Path.dispatch(location.hash) }; if (location.hash === "") { if (Path.routes.root !== null) { location.hash = Path.routes.root } } if ("onhashchange" in window && (!document.documentMode || document.documentMode >= 8)) { window.onhashchange = a } else { setInterval(a, 50) } if (location.hash !== "") { Path.dispatch(location.hash) } }, core: { route: function (a) { this.path = a; this.action = null; this.do_enter = []; this.do_exit = null; this.params = {}; Path.routes.defined[a] = this } }, routes: { current: null, root: null, rescue: null, previous: null, defined: {} } }; Path.core.route.prototype = { to: function (a) { this.action = a; return this }, enter: function (a) { if (a instanceof Array) { this.do_enter = this.do_enter.concat(a) } else { this.do_enter.push(a) } return this }, exit: function (a) { this.do_exit = a; return this }, partition: function () { var a = [], b = [], c = /\(([^}]+?)\)/g, d, e; while (d = c.exec(this.path)) { a.push(d[1]) } b.push(this.path.split("(")[0]); for (e = 0; e < a.length; e++) { b.push(b[b.length - 1] + a[e]) } return b }, run: function () { var a = false, b, c, d; if (Path.routes.defined[this.path].hasOwnProperty("do_enter")) { if (Path.routes.defined[this.path].do_enter.length > 0) { for (b = 0; b < Path.routes.defined[this.path].do_enter.length; b++) { c = Path.routes.defined[this.path].do_enter[b](); if (c === false) { a = true; break } } } } if (!a) { Path.routes.defined[this.path].action() } } };

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

function construct(con, args){
    var convertedArgs = [];
    if(args){
        args.forEach(function(item){
            var itemType = typeof item;
            if( itemType === "string" || itemType === "String" || itemType === "STRING"){
                
                var obj = getObjectFromString(item);
                
                if(obj){
                    convertedArgs.push(obj);
                }
            }
            else if(itemType === "object" || itemType == "function"){
                convertedArgs.push(item);
            }
        });
    }
    function F(){ return con.apply(this, convertedArgs)};
    F.prototype = con.prototype;
    return new F();
}

function parseOptions(json){
    if(!json) return {};
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
            timeout: 0,
            time2wait: 1000,
            backgroundColor: "white"
        }, options );

        settings.pages.forEach(function(page){

            Path.map(page.route)
            .enter(function () {})
            .exit(function () {
                self.root.removeClass('animated fadeOutLeft');
                self.root.removeClass('animated fadeInRight');
                self.root.addClass('animated fadeOutLeft');
            })
            .to(function () {
                var params = this.params;
                setTimeout(function () {
                    settings.timeout = settings.time2wait;
                    setCurrentVM(page, params);
                    self.root.removeClass('animated fadeOutLeft');
                    self.root.removeClass('animated fadeInRight');
                    self.root.addClass('animated fadeInRight');

                }, settings.timeout);
            });
        });


        var setCurrentVM = function(page, params){
            page.params = params;
            self.root.page(page);
        }

        var firstPage = settings.pages[0];
        Path.root(firstPage.route);
        Path.listen();

        return self;
    };
 
}( jQuery ));

(function( $ ) {
 
    $.fn.page = function( settings ) {
        var self = this;
        self.root = $(self);
        
        var dataOptions = self.root.data("options");
        if(!settings && typeof dataOptions === "string"){
            dataOptions = parseOptions("{" + dataOptions + "}");
        }
        else{
            dataOptions = {};
        }

        var options = $.extend({
            // These are the defaults.
            view: undefined, // This is the URL to the view
            _view: undefined, // THis is the raw HTML
            vm: undefined, // This is the constructor from the ViewModel
            _vm: undefined, // This is the constructed ViewModel
            params: undefined, // This is an Object of possible params pass to the page
            args: []
        }, dataOptions );

        
        options = $.extend(options, settings);

        var loadView = function () {
            if (options.view && !options._view) {
                $.ajax({
                    url: options.view
                })
                .done(function (pageContent) {
                    options._view = pageContent;
                    activateVM();
                })
                .error(function (err) {
                    //Todo handle Errorcodes here!
                    if (error) error(er);
                });
            } else {
                activateVM();
            }
        };

        var activateVM = function() {
            self.root.empty();
            self.root.append(options._view);
            
            if (!options._vm && options.vm) {
                var vmtype = typeof options.vm;
                if( vmtype === "string" ||vmtype === "String" || vmtype === "STRING"){
                    var vm = window[options.vm];
                    if(vm !== undefined){
                        options.vm = vm;
                    }
                    else{
                        options._vm = {};
                        return;
                    }
                }
                options._vm = construct(options.vm,options.args);
            }
            
            if (options._vm !== undefined && options._vm.activate){
                options._vm.activate(options.params);

                if(window["ko"] !== undefined){
                    ko.applyBindings(options._vm, self.root[0]);
                }
            }
        };

        loadView();
    }

})( jQuery );

(function( $ ) {
 
    $.fn.pivot = function( options ) {
        var self = this;
        self.root = $(self);
        self.header = null;
        self.container = null;

        self.pivotItems = [];
        self.children = self.root.children();
        for(var i = 0; i < self.children.length; i++){
            var child = $(self.children[i]);
            var options = child.data("options");
            var title = child.data("title");

            var pivotItem = {
                title: title ? title : "Item " + i,
                options: parseOptions("{" + options + "}"),
                el: child.context.outerHTML
            };

            self.pivotItems.push(pivotItem);
        };

        var loadPage = function(index){
            var pivotitem = self.pivotItems[index];
            self.container.empty();
            self.container.append(pivotitem.el);
            var pivotElement = $(self.container.children()[0]);
            pivotElement.page(pivotitem.options);
            
            //todo: find way to remove setTimeout
            setTimeout(function(){
                pivotElement.addClass('animation pivot-enter');
            }, 10);
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
            //title.addClass("transition-all");

            var childs = parent.children();
            for(var i = 0; i < listIndex; i++){
                var child = $(childs[i]);
                child.addClass("transition-margin-left");
                //child.appendTo(parent);
                child.css("margin-left", "-" + child.width() + "px");
            }
            
            setTimeout(function(){

                for(var i = 0; i < listIndex; i++){
                    var child = $(childs[i]);
                    child.removeClass("transition-margin-left");
                    child.appendTo(parent);
                    child.css("margin-left", "0px");
                }
       
                //title.css("padding-left", "0px");    
            },300);
        };

        self.root.empty();
        addHeader();
        addContainer();
        loadPage(0);
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
                options: parseOptions("{" + options + "}"),
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
    }

})( jQuery );
