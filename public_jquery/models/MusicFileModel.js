function MusicFileModel(data) {
    var self = this;
    var id = "";
    var webPath = "";
    var name = "";
    var type = "";
    var directoryName = "";
    var showVoting = false;
    var artist = "";
    var album = "";
    var title = "";
    var covername = "";

    if (data) {
        id = data.id;
        webPath = data.WebPath;
        name = data.Name || data.name;
        directoryName = data.DirectoryName || data.path;
        type = data.Type ? data.Type : "";
        showVoting = data.isVoted === true ? false : true;
        artist = data.artist;
        album = data.album;
        title = data.title;
        covername = data.cover;
    }

    self.id = id;
    self.webPath = webPath;
    self.name = name;
    self.directoryName = directoryName;
    self.type = type;
    self.showVoting = showVoting;
    self.title = title;
    self.album = album;
    self.artist = artist;
    self.covername = covername;
    self.hasCover = covername === "" ? false : true;
}
