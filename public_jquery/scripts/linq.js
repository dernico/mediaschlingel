
Array.prototype.Where = function (func) {
    var result = [];
    this.forEach(function (item) {
        if (func(item)) {
            result.push( item );
        }
    });
    return result;
};


Array.prototype.SelectFirst = function (func) {
    var result = null;
    this.forEach(function (item) {
        if (func(item)) {
            result = item;
            return;
        }
    });
    return result;
};