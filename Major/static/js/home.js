$(function() {
	$("button").click(function(event){

		var v2 =$(this).attr("abc");
		if ( v2 != undefined) {
			alert(v2);
			$.ajax({ 
				type: "GET",
				dataType: "json",
				url: "http://192.168.43.189:5000/read_thread?id=" + v2,
				data:"",
			}).done(function(data) {
//				alert( "success : " + data['d'] + " : " + data['l'][0] + " : " + data['t']['body']);
				$("#dialog p").text(data['t']['body']);
				printJsonKeyValue(data['d'], data['l']);
				$( "#dialog" ).dialog( "open" );
				
			}).fail(function() {
				alert( "error" );
				});	  
			}
		});


	$( "#dialog" ).dialog({
		autoOpen: false,
		width: 650,
		show: {
			effect: "clip",
			duration: 200
      		},
	      	hide: {
			effect: "clip",
			duration: 200
	      	},
		close: function() {
			$("#dialog ul").empty();
		}
    	});

});


function checkUpdate() {
	$.ajax({ 
		type: "GET",
		dataType: "json",
		url: "http://10.2.4.228:5000/notification",
		data:"",
	}).done(function(data) {
		alert( "count : " + data['count']);
		if(data['count']>=0) {
			$("#notification a").text("You have " +data[count] +" new notification");
			$("#notification").show();
		}
	}).fail(function() {
		alert( "error" );
	});	  

}

function printJsonKeyValue(dict,list) {
	
	var str = '';

	jQuery.each(list, function( i, val ) {
		str += '<li class="list-group-item">' +
			'<span>' +	dict[val]['user'] + ' : </span><hr>' +
			'<span>' +	dict[val]['body'] + '</span></li>';
	});
//	alert(str);
	$("#dialog ul").append(str);
}

