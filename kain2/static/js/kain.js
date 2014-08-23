
/* Configs a bookmark */
function cfgB(gid) {

	/* Name */
	$("#NAME-"+gid+' b').toggle();
	$("#NAME-"+gid+' input').toggle();

	/* User */
	$("#USER-"+gid+' span').toggle();
	$("#USER-"+gid+' input').toggle();

	/* URL */
	$("#URL-"+gid+' a').toggle();
	$("#URL-"+gid+' input').toggle();

	/* Pass */
	$("#PASS-"+gid+' span').toggle();
	$("#PASS-"+gid+' input').toggle();

	/* Focus */
	$("#NAME-"+gid+' input').focus();
}

/* Updates bookmark name */
function upd_name(gid){
	name		= $("#input-name-"+gid).val();
        var data        = {};
        data['gid']     = gid;
        data['name']    = name;
        var url = '/kain/cgi/name/'+gid+"/";
	if ( $("#NAME-"+gid+' b').html() == name )
		return;
        $.ajax({
                type:           "GET",
                data:           data,
                dataType:       'json',
                url:            url,
                success:        function(data) {
                                        if (data.status==0) {
                                                alert(data.message);
                                        } else {
						$("#NAME-"+gid+' b').html(name);
						cfgB(gid);
                                        }
                                },
                error:          function(e,msg) {
                                        alert("ERROR");
                                        alert(msg);
                }
        });
}

/* Updates bookmark user */
function upd_user(gid){
	user		= $("#input-user-"+gid).val();
        var data        = {};
        data['gid']     = gid;
        data['user']    = user;
        var url = '/kain/cgi/user/'+gid+"/";
	if ( $("#USER-"+gid+' span').html() == user )
		return;
        $.ajax({
                type:           "GET",
                data:           data,
                dataType:       'json',
                url:            url,
                success:        function(data) {
                                        if (data.status==0) {
                                                alert(data.message);
                                        } else {
						$("#USER-"+gid+' span').html(user);
						cfgB(gid);
                                        }
                                },
                error:          function(e,msg) {
                                        alert("ERROR");
                                        alert(msg);
                }
        });
}

/* Updates bookmark password */
function upd_pass(gid){
	pasw 		= $("#input-pass-"+gid).val();
        var data        = {};
        data['gid']     = gid;
        data['pass']    = pasw;
        var url = '/kain/cgi/pass/'+gid+"/";
        $.ajax({
                type:           "GET",
                data:           data,
                dataType:       'json',
                url:            url,
                success:        function(data) {
                                        if (data.status==0) {
                                                alert(data.message);
                                        } else {
						if ( pasw == "" )
							$("#PASS-"+gid+' span').html("");
						else
							$("#PASS-"+gid+' span').html("************");
						cfgB(gid);
                                        }
                                },
                error:          function(e,msg) {
                                        alert("ERROR");
                                        alert(msg);
                }
        });
}

/* Updates bookmark user */
function upd_url(gid){
	myurl		= $("#input-url-"+gid).val();
	myurl		= encodeURI(myurl);
        var data        = {};
        data['gid']     = gid;
        data['url']     = myurl;
        var url = '/kain/cgi/url/'+gid+"/";
	if ( $("#URL-"+gid+' a').html() == myurl )
		return;
        $.ajax({
                type:           "GET",
                data:           data,
                dataType:       'json',
                url:            url,
                success:        function(data) {
                                        if (data.status==0) {
                                                alert(data.message);
                                        } else {
						$("#URL-"+gid+' a').html(myurl.substring(0,27));
						$("#URL-"+gid+' a').attr("href",myurl);
						cfgB(gid);
                                        }
                                },
                error:          function(e,msg) {
                                        alert("ERROR");
                                        alert(msg);
                }
        });
}

/* Creates a skel for one bookmark */
function skelBookmark(gid,name,user,pasw,url) {
	var html = "";
	html += "<TR ID='ROW-"+gid+"'>";
	html += "	<TD ID='NAME-"+gid+"'>";
	html += "		<b>"+name.substring(0,27)+"</b>";
	html += "		<input class='HIDDEN' value='"+name+"' id='input-name-"+gid+"' onchange='upd_name("+gid+")' AUTOCOMPLETE=OFF />";
	html += "	</TD>";
	html += "	<TD ID='URL-"+gid+"'>";
	html += "		<A HREF='"+url+"'>"+url.substring(0,27)+"</A>";
	html += "		<input class='HIDDEN'  value='"+url+"' id='input-url-"+gid+"' onchange='upd_url("+gid+")' AUTOCOMPLETE=OFF />";
	html += "	</TD>";
	html += "	<TD ID='USER-"+gid+"'>";
	html += "		<span>"+user.substring(0,27)+"</span>";
	html += "		<input class='HIDDEN'  value='"+user+"' id='input-user-"+gid+"' onchange='upd_user("+gid+")' />";
	html += "	</TD>";
	html += "	<TD ID='PASS-"+gid+"'>";
	html += "		<span> ";
	if ( pasw != '') 
		html += "************"
	html += "		</span>";
	html += "		<input class='HIDDEN' value='"+pasw+"' id='input-pass-"+gid+"' onchange='upd_pass("+gid+")' AUTOCOMPLETE=OFF />";
	html += "	</TD>";
	html += "	<TD CLASS='TOOLS' >";
	html += "		<span class='glyphicon glyphicon-cog' ONCLICK='cfgB("+gid+");'> Edit</span> ";
	html += "		<span class='glyphicon glyphicon-remove' ONCLICK='delB("+gid+");'> Delete</span> ";
	html += "	</TD>";
	html += "</TR>";
	$("#FOLDER TBODY").append(html);
}

/* Adds a new bookmark */
function addB(fid){
	name = $("#ADD-BK").val();
        var data = {};
        data['name'] = name;
        data['fid']  = fid;
        var url = '/kain/cgi/add/'; 
        $.ajax({
                type:           "GET",
                data:           data,
                dataType:       'json',
                url:            url,
                success:        function(data) {
                                        if (data.status==0) {
                                                alert(data.message);
                                        } else {
						$("#ADD-BK").val('');
						$("#ADD-BK").focus();
						skelBookmark(data.gid,name,'','','');	
                                        }
                                },
                error:          function(e,msg) {
                                        alert("ERROR");
                                        alert(msg);
                }
        });
}

/* Deletes a bookmark */
function delB(gid){
        var data = {};
        var url = '/kain/cgi/delete/'+gid+"/";
        $.ajax({
                type:           "GET",
                data:           data,
                dataType:       'json',
                url:            url,
                success:        function(data) {
                                        if (data.status==0) {
                                                alert(data.message);
                                        } else {
						$("#ROW-"+gid).remove();
                                        }
                                },
                error:          function(e,msg) {
                                        alert("ERROR");
                                        alert(msg);
                }
        });
}
