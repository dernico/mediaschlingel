
if (Array.prototype.forEach === undefined) {
    Array.prototype.forEach = function (callback) {
        for (var i = 0; i < this.length; i++) {
            if (callback !== undefined) {
                callback(this[i]);
            }
        }
        return null;
    };
}

if (Array.prototype.select === undefined) {
    Array.prototype.select = function (action) {
        for (var i = 0; i < this.length; i++) {
            if (action !== undefined) {
                var result = action(this[i]);
                if (result) {
                    return this[i];
                }
            }
        }
        return null;
    };
}
if (Array.prototype.selectAll === undefined) {
    Array.prototype.selectAll = function (action) {
        var data = [];
        for (var i = 0; i < this.length; i++) {
            if (action !== undefined && this[i] !== undefined) {
                var result = action(this[i]);
                if (result) {
                    data.push(this[i]);
                }
            }
        }
        return data;
    };
}
if (Array.prototype.contains === undefined) {
    Array.prototype.contains = function (item) {
        for (var i = 0; i < this.length; i++) {
            if (item !== undefined) {
                if (this[i] === item) {
                    return true;
                }
            }
        }
        return false;
    };
}

if (Array.prototype.remove === undefined) {
    Array.prototype.remove = function (item) {
        var index = this.indexOf(item);
        this.splice(index, 1);
        //for (var i = 0; i < this.length; i++) {
        //    if (item !== undefined) {
        //        if (this[i] === item) {
        //            return true;
        //        }
        //    }
        //}
    };
}