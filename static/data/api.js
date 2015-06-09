//var api;
//(function(api){
pages.service("api", [function(){
    var api = {};
    var loading = '<div id="loadingContainer" class="" style="position:fixed; top: 0px; left: 0px; height: 100%; width: 100%;z-index:100">';
    loading += '<div style="position:absolute;width:100%; height: 100%; background-color: gray; opacity: 0.8;"></div>';
    loading += '<div class="loadingSpinner">';
    loading += '';
    loading += '</div>';
    loading += '<div class="loadingText" style="position:absolute;height: 100%; width:100%; ';
    loading += 'font-size: xx-large;font-variant: small-caps;color: dimgrey;text-align:center;top:50%">';
    loading += '<p>Woop Woop! Gleich geht es weiter ...</p>';
    loading += '</div>';
    loading += '';
    loading += '</div>';


    var showLoading = function() {
        removeLoading();
        $("body").append(loading);
    };
    var removeLoading = function() {
        $("#loadingContainer").remove(); 
    };

    var ajax = function(config, showLoadingScreen,success,error){
        if (showLoadingScreen) showLoading();
        $.ajax(config)
        .done(function (data) {
            console.log("ajax done.");
            removeLoading();
            if(success) success(data);
        })
        .error(function (data) {
            console.log("ajax error.");
            removeLoading();
            if(error) error(data);
        });
    };

    api.showLoading = showLoading;
    api.removeLoading = removeLoading;

    //TODO: Remove generic get and POST and build explicit functions to call

    api.get = function(config){
        //var data = [{"path":"http:\/\/icecast.timlradio.co.uk\/a732.ogg","id":1,"dbid":4,"type":"Stream","name":"icecast.timlradio.co.uk"},{"path":"http:\/\/bcb-high.rautemusik.fm","id":2,"dbid":9,"type":"Stream","name":"bcb-high.rautemusik.fm"},{"path":"http:\/\/stream.blackbeatslive.de\/","id":3,"dbid":10,"type":"Stream","name":"stream.blackbeatslive.de"},{"path":"http:\/\/stream.blackbeats.fm\/","id":4,"dbid":11,"type":"Stream","name":"stream.blackbeats.fm"},{"path":"http:\/\/jam-high.rautemusik.fm","id":5,"dbid":14,"type":"Stream","name":"jam-high.rautemusik.fm"},{"path":"http:\/\/hr-mp3-m-youfm.akacast.akamaistream.net\/7\/246\/142136\/v1\/gnl.akacast.akamaistream.net\/hr-mp3-m-youfm","id":6,"dbid":18,"type":"Stream","name":"hr-mp3-m-youfm.akacast.akamaistream.net"},{"path":"http:\/\/gffstream.ic.llnwd.net\/stream\/gffstream_mp3_w76a","id":7,"dbid":21,"type":"Stream","name":"gffstream.ic.llnwd.net"},{"path":"http:\/\/gffstream.ic.llnwd.net\/stream\/gffstream_mp3_w75a","id":8,"dbid":22,"type":"Stream","name":"gffstream.ic.llnwd.net"},{"path":"http:\/\/bw.bigfm.fmstreams.de\/dnb","id":9,"dbid":23,"type":"Stream","name":"bw.bigfm.fmstreams.de"},{"path":"\/mnt\/sdcard\/sample.mp3","id":10,"dbid":-1,"type":"Localfile","name":"sample.mp3"},{"path":"\/mnt\/sdcard\/Music\/13-chiddy_bang-slow_down_(feat._black_thought_and_eldee_the_don).mp3","id":11,"dbid":-1,"type":"Localfile","name":"13-chiddy_bang-slow_down_(feat._black_thought_and_eldee_the_don).mp3"},{"path":"\/mnt\/sdcard\/Music\/18-chiddy_bang-all_things_go.mp3","id":12,"dbid":-1,"type":"Localfile","name":"18-chiddy_bang-all_things_go.mp3"},{"path":"\/mnt\/sdcard\/Music\/14-chiddy_bang-decline.mp3","id":13,"dbid":-1,"type":"Localfile","name":"14-chiddy_bang-decline.mp3"},{"path":"\/mnt\/sdcard\/Music\/05-chiddy_bang-now_u_know_(feat._jordan_brown).mp3","id":14,"dbid":-1,"type":"Localfile","name":"05-chiddy_bang-now_u_know_(feat._jordan_brown).mp3"},{"path":"\/mnt\/sdcard\/Music\/01-chiddy_bang-get_up_in_the_morning.mp3","id":15,"dbid":-1,"type":"Localfile","name":"01-chiddy_bang-get_up_in_the_morning.mp3"},{"path":"\/mnt\/sdcard\/Music\/04-chiddy_bang-fresh_like_us.mp3","id":16,"dbid":-1,"type":"Localfile","name":"04-chiddy_bang-fresh_like_us.mp3"},{"path":"\/mnt\/sdcard\/Music\/03-chiddy_bang-danger_zone.mp3","id":17,"dbid":-1,"type":"Localfile","name":"03-chiddy_bang-danger_zone.mp3"},{"path":"\/mnt\/sdcard\/Music\/02-chiddy_bang-never.mp3","id":18,"dbid":-1,"type":"Localfile","name":"02-chiddy_bang-never.mp3"},{"path":"\/mnt\/sdcard\/Music\/Chiddy Bang - Ray Charles.mp3","id":19,"dbid":-1,"type":"Localfile","name":"Chiddy Bang - Ray Charles.mp3"},{"path":"\/mnt\/sdcard\/Music\/Chiddy Bang - Opposite of Adults.mp3","id":20,"dbid":-1,"type":"Localfile","name":"Chiddy Bang - Opposite of Adults.mp3"},{"path":"\/mnt\/sdcard\/Music\/Chiddy Bang - I Can't Stop feat. Busta Rhyme.mp3","id":21,"dbid":-1,"type":"Localfile","name":"Chiddy Bang - I Can't Stop feat. Busta Rhyme.mp3"},{"path":"\/mnt\/sdcard\/Music\/Chiddy Bang  - Hey London.mp3","id":22,"dbid":-1,"type":"Localfile","name":"Chiddy Bang  - Hey London.mp3"}];
        //success(data);
        var action = config.action;
        var params = config.params;
        var success = config.success;
        var error = config.error;
        var showLoadingScreen = config.showLoading === undefined ? true : config.showLoading;

        params = params ? params : "?";
        params += "&random=" + Math.random().toString();

        ajax({
            url: '/api/music/' + action + params 
        }, showLoadingScreen, success, error);
      
    };


    api.post = function(action,data,success,error) {
        var showLoadingScreen = true;
        ajax({
            url: '/api/music/' + action+ "?random=" + Math.random().toString(),
            type: 'POST',
            data: data
        }, showLoadingScreen, success, error);
    };

    api.loadAlbums = function(search, page, albumCount, success, error){
        
        albumCount = albumCount ? albumCount : 10;
        page = page ? page : 1;
        search = search !== undefined ? search : "";
        ajax({
            url: "/api/music/albums",
            data: {search: search, albumCount: albumCount, albumPage: page}
        },true, function(data){

            var albums = [];
            data.albums.forEach(function(album){
                albums.push(new AlbumModel(album));
            });

            if(success) success(albums);

        }, error);
    };

    api.vote = function(item, done, error){
        api.get({
            action: "vote",
            params: "?id=" + item.id,
            success: done,
            error: error
        });
    };

    api.restartSchlingel = function(){
        ajax({
            url: 'api/restartSchlingel',
        }, false, null, null);
    };

    api.radio = {};

    api.radio.recommendations = function(success, error){
        ajax({
            url: '/api/music/radio/recommendations'
        }, true, function(data){
            var recommendations = [];
            data.recommendations.forEach(function(reco){
                var model = new radioModel(reco);
                recommendations.push(model);
            });
            if(success) success(recommendations);
        }, error);
    };

    api.radio.top = function(success, error){
        ajax({
            url: '/api/music/radio/top'
        }, true, function(data){
            var tops = [];
            data.top.forEach(function(top){
                var model = new radioModel(top);
                tops.push(model);
            });
            if(success) success(tops);
        }, error);
    };

    api.radio.mostWanted = function(success, error){
        ajax({
            url: '/api/music/radio/mostWanted'
        }, true, function(data){
            var mostWanted = [];
            data.mostWanted.forEach(function(most){
                var model = new radioModel(most);
                mostWanted.push(model);
            });
            if(success) success(tops);
        }, error);
    };

    api.radio.categories = function(type, success, error){
        ajax({
            url: '/api/music/radio/categories',
            data: { categorieType: type}
        }, false, success, error);
    };

    api.radio.bycategorie = function(type, categorie, success, error){
        ajax({
            url: '/api/music/radio/bycategorie',
            data: { categorieType: type, categorie: categorie}
        }, false, function(data){
            var stations = [];
            data.stations.forEach(function(station){
                var model = new radioModel(station);
                stations.push(model);
            });
            if(success) success(stations);

        }, error);
    };

    api.tracks = {};

    api.tracks.tags = function(tag, done){
        ajax({
            url: '/api/8tracks/tags',
            data: {tag: tag}
        }, true, function(data){
            done(data, null);
        }, function(err){
            done(null, err);
        });
    };

    api.tracks.explore = function(tags, done){
        ajax({
            url: '/api/8tracks/explore',
            type: 'POST',
            data: {tags: tags}
        }, true, function(data){
            done(data, null);
        }, function(err){
            done(null, err);
        });
    };

    api.tracks.play = function(mix, done){
        ajax({
                url: '/api/8tracks/play',///' + mix.id,
                type: 'POST',
                data: {mix: JSON.stringify(mix)}
            }, 
            false, 
            function(data){
                if(done) done(data);
            },
            function(err){
                if(done) done(null, err);
            });
    };

    api.tracks.search = function(search, done){
        ajax({
                url: '/api/8tracks/search',///' + mix.id,
                data: {search: search}
            }, 
            true, 
            function(data){
                if(done) done(data);
            },
            function(err){
                if(done) done(null, err);
            });
    };

    api.tracks.page = function(pageTo, done){
        ajax({
                url: '/api/8tracks/page',
                data: {page_to: pageTo}
            },
            true, 
            function(data){
                if(done) done(data);
            },
            function(err){
                if(done) done(null, err);
            });
    };

    api.youtube = {};

    api.youtube.search = function(data, done){

        ajax({
                url: '/api/youtube/search',
                data: data
            }, 
            true, 
            function(data){

                var ytModels = [];
                data.tracks.forEach(function(item){
                    ytModels.push(new youtubeModel(item));
                });
                data.tracks = ytModels;
                if(done) done(data);
            },
            function(err){
                if(done) done(null, err);
            });
    };

    api.youtube.play = function(track, done){
        ajax({
                url: '/api/youtube/play?id=' + track.id,
                type: 'POST'
            }, 
            false, 
            function(data){
                if(done) done(data);
            },
            function(err){
                if(done) done(null, err);
            });
    };

    api.youtube.addPlaylist = function(track, done, error){
        ajax({
            url: "/api/youtube/addplaylist",
            type: "POST",
            data: {track: JSON.stringify( track )}
        }, false, done, error);
    };

    api.youtube.related = function(track, done, error){
        ajax({
            url: "/api/youtube/related",
            data: {id: track.id}
        }, false, 
            function(data){

                var ytModels = [];
                data.tracks.forEach(function(item){
                    ytModels.push(new youtubeModel(item));
                });
                data.tracks = ytModels;
                if(done) done(data);
            }, error);
    };

    api.youtube.getPlaylist = function(done, error){
        ajax({
            url: "/api/youtube/playlist"
        }, false, done, error);
    };

    var laut = "http://api.laut.fm";
    api.laut = api.laut ? api.laut : {};
    api.laut.search = function(term, success, error){
        var query = "/search/stations?query=";
        query += decodeURIComponent(term);
        query += "&limit=200";
        ajax({
            url: laut + query
        },success,error);
    };

    return api;
}]);
//})(api || (api = {}));
