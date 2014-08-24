
/* CREATE A NEW FOLDER */
function addFolder(){

	/* GET FOLDER NAME */
	progress('20%');
	var name = prompt("Nombre de la carpeta");
	if (!name) {
		progress('0%');
		return;
	}

	/* GET PARENT ID */
	progress('40%');
	var fid = $("#FOLDERID").val();

	/* GENERATE DATA */
	var data 	= {};
	data['fid'] 	= fid;
	data['name'] 	= name;

	/* MAKE REQUEST */
	var url = "/data/cgi/folder/add/";
	$.ajax({
		type: 		"GET",
                data:		data,
                dataType:	'json',
                url: 		url,
                success: 	function(data) {
                        		if (data.status==0) {
						progress('0%');
                                		alert(data.message);
                        		} else {
						progress('100%');
						location.reload();
                        		}
                		},
                error: 		function(e,msg) {
					progress('0%');
                        		alert("ERROR");
                        		alert(msg);
                }
        });
}

/* EDIT A FOLDER NAME */
function editFolder(){

	/* GET FOLDER NAME */
	progress('20%');
	var name = prompt("Nuevo nombre?");
	if (!name) {
		progress('0%');
		return;
	}

	/* GET PARENT ID */
	progress('40%');
	var fid = $("#FOLDERID").val();

	/* GENERATE DATA */
	var data 	= {};
	data['fid'] 	= fid;
	data['name'] 	= name;

	/* MAKE REQUEST */
	var url = "/data/cgi/folder/mod/";
	$.ajax({
		type: 		"GET",
                data:		data,
                dataType:	'json',
                url: 		url,
                success: 	function(data) {
                        		if (data.status==0) {
						progress('0%');
                                		alert(data.message);
                        		} else {
						progress('100%');
						location.reload();
                        		}
                		},
                error: 		function(e,msg) {
					progress('0%');
                        		alert("ERROR");
                        		alert(msg);
                }
        });
}

/* REMOVE A FOLDER NAME PERMANENTLY */ 
function removeFolder(){

	/* CONFIRM */
	progress('40%');
	if (!confirm("Está seguro que quiere borrar esto?") ) {
		progress('0%');
		return;
	}

	/* GET FOLDER ID TO REDIRECT */
	next = $("#F1ID").val();

	/* GET PARENT ID */
	progress('40%');
	var fid = $("#FOLDERID").val();

	/* GENERATE DATA */
	var data 	= {};
	data['fid'] 	= fid;

	/* MAKE REQUEST */
	var url = "/data/cgi/folder/rem/";
	$.ajax({
		type: 		"GET",
                data:		data,
                dataType:	'json',
                url: 		url,
                success: 	function(data) {
                        		if (data.status==0) {
						progress('0%');
                                		alert(data.message);
                        		} else {
						progress('100%');
						if (next>0)
							location.href='/data/folder/'+next+'/';
						else
							location.href='/data/root/';
                        		}
                		},
                error: 		function(e,msg) {
					progress('0%');
                        		alert("ERROR");
                        		alert(msg);
                }
        });
}

/* SWITCH FOLDER READ PERMISSIONS */
function readFolder(){

	/* GET PARENT ID */
	progress('40%');
	var fid = $("#FOLDERID").val();

	/* GENERATE DATA */
	var data 	= {};
	data['fid'] 	= fid;

	/* MAKE REQUEST */
	var url = "/data/cgi/folder/read/";
	$.ajax({
		type: 		"GET",
                data:		data,
                dataType:	'json',
                url: 		url,
                success: 	function(data) {
                        		if (data.status==0) {
						progress('0%');
                                		alert(data.message);
                        		} else {
						progress('100%');
						location.reload();
                        		}
                		},
                error: 		function(e,msg) {
					progress('0%');
                        		alert("ERROR");
                        		alert(msg);
                }
        });
}

/* SWITCH FOLDER WRITE PERMISSIONS */
function writeFolder(){

	/* GET PARENT ID */
	progress('40%');
	var fid = $("#FOLDERID").val();

	/* GENERATE DATA */
	var data 	= {};
	data['fid'] 	= fid;

	/* MAKE REQUEST */
	var url = "/data/cgi/folder/write/";
	$.ajax({
		type: 		"GET",
                data:		data,
                dataType:	'json',
                url: 		url,
                success: 	function(data) {
                        		if (data.status==0) {
						progress('0%');
                                		alert(data.message);
                        		} else {
						progress('100%');
						location.reload();
                        		}
                		},
                error: 		function(e,msg) {
					progress('0%');
                        		alert("ERROR");
                        		alert(msg);
                }
        });
}

