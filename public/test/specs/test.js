/// <reference path="../../scripts/knockout-2.2.1.js" />
/// <reference path="../../scripts/ko.Page.js" />
/// <reference path="../../viewmodels/pageing.js" />
/// <reference path="../../viewmodels/list.js" />

var api = null;
var player = null;
module("Basic Test", {
	setup: function(){
		api = {
			get: function(){

			}
		};
		player = {};
		console.log("setup");
	},
	teardown: function(){
		console.log("teardown");
	}
});

test("Just a test to test if tests work", function () {
    expect(1);
    ok(1 == 1);
});

test("test if listvm can create a new object", function(){
    var vm = new listvm(api, player);
    ok(vm !== null);
});

/*test("test that listvm cannot be instantiante without neccesary parameter", function () {
    expect(1);
    //var vm = new listvm();
    if(throws)
        raises = throws;

    raises(function () {
        new listvm();
    }, "an error should be thrown");
});*/
