
function MusicFileInfoModel(data) {
    var self = this;
    var currentMusicFile = null;
    var duration = null;
    var position = null;
    var filter = "";
    var isplaying = false;
    var israndom = false;
    var volume = 0;

    if (data) {
        currentMusicFile = new MusicFileModel(data);
        duration = data.Duration;
        filter = data.PlayerFilter;
        position = data.Position;
        isplaying = data.IsPlaying;
        israndom = data.IsRandom;
        volume = data.Volume;
    }

    self.currentMusicFile = ko.observable(currentMusicFile);
    self.duration = ko.observable(duration);
    self.searchfilter = filter;
    self.position = ko.observable(position);
    self.isplaying = isplaying;
    self.israndom = israndom;
    self.volume = volume;
}
