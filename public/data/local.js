var LocalData;
(function (LocalData) {
    var key = "worktimeDate";
    var store = window.localStorage;
    function save(value) {
        store.setItem(key, value);
    }
    LocalData.save = save;
    ;
    function load() {
        return store.getItem(key);
    }
    LocalData.load = load;
})(LocalData || (LocalData = {}));
;
