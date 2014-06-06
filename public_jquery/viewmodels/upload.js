var uploadvm = (function() {


    return function() {
        var self = this;
        self.filename = ko.observable();
        self.upload = function() {
            //Wieder unser File Objekt
            var file = document.getElementById("fileA").files[0];
            //FormData Objekt erzeugen
            var formData = new FormData();
            //XMLHttpRequest Objekt erzeugen
            var client = new XMLHttpRequest();

            var prog = document.getElementById("progress");

            if (!file)
                return;

            prog.value = 0;
            prog.max = 100;

            //Fügt dem formData Objekt unser File Objekt hinzu
            formData.append("datei", file);

            client.onerror = function(e) {
                alert("onError");
            };

            client.onload = function(e) {
                document.getElementById("prozent").innerHTML = "100%";
                prog.value = prog.max;
            };

            client.upload.onprogress = function(e) {
                var p = Math.round(100 / e.total * e.loaded);
                document.getElementById("progress").value = p;
                document.getElementById("prozent").innerHTML = p + "%";
            };

            client.onabort = function(e) {
                alert("Upload abgebrochen");
            };

            client.open("POST", "upload");
            client.send(formData);
        };
    };
})();
