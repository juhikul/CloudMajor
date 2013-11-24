$(function() {
	$("button").click(function(event){

		var v1 =$(this).attr("key");
		var v2 =$(this).attr("abc");
		var v3 =$(this).attr("nextt");
		if ( v1 != undefined) {
		      	$( "#" + v1 ).toggle();
		      	return false;
		} else if ( v2 != undefined) {
		//	alert(v2);
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
		} else if (v3 != undefined) {
	//		alert("inside more");
			var v2 =$(this).attr("nextt");
	//		alert(v2);
			$.ajax({ 
				type: "GET",
				dataType: "json",
				url: "http://192.168.43.189:5000/home?start=" + v2,
				data:"",
			}).done(function(data) {
	//			alert( "success : " + data['d'] + " : " + data['l'][0] + " : " + data['t']['body']);
				createTweetString(data['d'],data['l'],data['f'],data['retweet']);
				$("#more").attr("nextt",data['start']);
//				alert(data['start']);
				if (data['start'] == 0){
					$('#more').hide();
				}
				update_link();

				
			}).fail(function() {
				alert( "error for moew values" );
			});	  

		}
	});

	setInterval(function(){
		checkUpdate();}, 30000);

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
	//alert("check update");
	$.ajax({ 
		type: "GET",
		dataType: "json",
		url: "http://192.168.43.189:5000/notification",
		data:"",
	}).done(function(data) {
	//	alert( "count : " + data['count']);
		if(data['count']>0) {
//			alert("show notification");
			$("#notification a").text("You have " +data['count'] +" new Tweets");
			$("#notification").show('1000');
		}
	}).fail(function() {
		alert( "error" );
	});	  

}

function printJsonKeyValue(dict,list) {
	
	var str = '';

	jQuery.each(list, function( i, val ) {
		if(val==0){
			str += '<li class="list-group-item"><span style="color:grey"><i>Be the first one to reply</i></span></li>'
			return false;
		} else {
		str += '<li class="list-group-item">' +
			'<span>' +	dict[val]['user'] + ' : </span><hr>' +
			'<span>' +	dict[val]['body'] + '</span></li>';
		}
	});
//	alert(str);
	$("#dialog ul").append(str);
}
function update_link(){
//alert("inside update");
$("p.tweets").each(function() {
        var b = $(this).text();
        var s = b.split(" ");
        var str = '';
        
        jQuery.each(s, function( i, val ) {
                if (val[0] == "#") {
                        tr = val.substring(1);
                        str += '<a href="show_trends?topic=' + tr + '">' + 
                                val + ' </a>';
                } else {
                        str += val + ' ';
                }
        });
//      alert(str);
        $(this).html(str);
});

}

function createTweetString(tweetdict,list,favlist,retweetdict) {
	jQuery.each(list, function( i, val ) {
		key = val.split("!")[0];
		var str="";
//		alert(tweetdict[key]['status'] + ' ' + key+' ' + tweetdict[key]['user'])
		if (tweetdict[key]['status'] == undefined) {
		//	alert("inside loop");
			str='<div class="container" style="background:lightgrey"><p>' +
				tweetdict[key]['user'] + '<a href="{{ url_for("favourite",id=' + key + ') }}" style="float:right">';
			if (favlist[key] == undefined) {
				str += '<i class="fa fa-star-o"></i></a></p>'
			} else {
				str += '<i class="fa fa-star"></i></a></p>';
			}
			
			if (val.indexOf('!') != -1) {
				str += '<p style="color:grey;">Retweeted by ' + val.split("!")[1] + ' </p>';
			}


			str += '<p style="color:grey;"  class="tweets">' + tweetdict[key]['body'] + '</p>';
			str += '<button class="btn pull-left btn-link btn-xs" class="rep" key=' + key + '>Reply</button>';
			str += '<span style="float:right"><button class="btn pull-left btn-link btn-xs" abc=' + key +'>' +
					'<i class="fa fa-search-plus"></i></button> | ';
			if (retweetdict[key] == undefined){
				str +=  '<a href="retweet?tid=' + key + '"><span>Retweet</span></a>|'
			} else {
				str += '<a href="untweet?tid=' + key + '"><span style="color:green">Retweeted</span></a> |';
			}
			str += '</span><div class="toggler"><div id=' + key +'  class="ui-widget-content ui-corner-all">';
			str += '<form action="{{ url_for("post_reply") }}" method="POST"> <span><input type="text" class="form-control" placeholder="Post a reply" name="repid" style="float:left" /><button class="btn pull-right btn-link btn-xs" type="submit">POST</button></span>';
			
		//	alert(str);
			str += '<input type="hidden" name="tid" value=' + key + ' /></form></div></div></div><br/>';
		//	alert(str);
			$("div.col-md-8").append(str);
		}
		
	});
	

}

