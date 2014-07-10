
if(Array.prototype.select === undefined){
  Array.prototype.select = function(action){
    for(var i = 0; i < this.length; i++){
      if(action !== undefined) {
        var result = action(this[i]);
        if(result) {
          return this[i];
        }
      }
    }
  };
}
if(Array.prototype.selectAll === undefined){
  Array.prototype.selectAll = function(action){
    var data = [];
    for(var i = 0; i < this.length; i++){
      if(action !== undefined && this[i] !== undefined) {
        var result = action(this[i]);
        if(result) {
          data.push(this[i]);
        }
      }
    }
    return data;
  };
}