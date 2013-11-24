$(function() {
	setInterval(function(){
		checkUpdate();}, 30000);
});

function checkUpdate() {
	$.ajax({ 
		type: "GET",
		dataType: "json",
		url: "http://192.168.43.189:5000/notification",
		data:"",
	}).done(function(data) {
		alert( "count : " + data['count']);
		if(data['count']>0) {
			$("#notification a").text("You have " +data['count'] +" new Tweets");
			$("#notification").show('1000');
		}
	}).fail(function() {
		$("#notification").hide();
	});	  

}

