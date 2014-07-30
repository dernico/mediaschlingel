pages.viewmodel("playervm", ["player","api", function(player, api, background) {

    var self = this;

    self.showPlaying = player.showPlaying;
    self.randomOff = player.randomOff;

    self.Album = player.Album;
    self.Name = player.Name;
    self.Volumn = player.Volumn;

    self.toggleRandom = player.toggleRandom;

    //Operate the player
    self.playpause = player.playpause;

    self.play = player.play;

    self.next = player.next;

    self.prev = player.prev;

    self.volUp = player.volUp;

    self.volDown = player.volDown;

    self.activate = function(){
        player.LoadCurrentInfo();
    };
}]);