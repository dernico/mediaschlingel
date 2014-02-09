$(document).bind("mobileinit",function(){
//$(document).ready(function(){
  //alert("mobileinit");
  $.mobile.ajaxEnabled = false;
  $.mobile.linkBindingEnabled = false;
  $.mobile.hashListeningEnabled = false;
  $.mobile.pushStateEnabled = false;
  $.mobile.changePage.defaults.changeHash = false;
  /*
  $('div[data-role="page"]').live('pagehide',function(event, ui){
    $(event.currentTarget).remove();
  });
  */
});