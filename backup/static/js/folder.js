
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
	var url = "/folder/add/";
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
	var current = $("#F1Name").val();
	var name = prompt("Nuevo nombre?",current);
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
	var url = "/folder/mod/";
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
	var url = "/folder/rem/";
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
							location.href='/folder/'+next+'/';
						else
							location.href='/folder/';
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
	var url = "/folder/read/";
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
	var url = "/folder/write/";
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


/* UPLOAD FILES */
function upload(){
	var input = $('#fileinput');
	input.replaceWith(input.val('').clone(true));
	input.trigger('click');
}

/* UPLOAD MULTIPLER FILES LISTENER */
function fileListener(input) {

	/* BEGIN */
	var files = input.files;
	window.uploadSize=files.length;
	var url = "/gallery/add/";
	var csrf = $('#csrf input').val();
	var fid = $("#FOLDERID").val();
	var max_size = $("#TASK_UPLOAD_FILE_MAX_SIZE").val();

	/* VALIDATE FILES */
	for (var i=0; i<window.uploadSize; i++) {
		if (files[i].size > max_size) {
			alert("ERROR " + files[i].name + " es demasiado grande " + files[i].size);
			return;
		}
		// alert(files[i].name);
		// alert(files[i].type);
	}

	/* FOR EACH FILE */
	shadowOn();
	for (var i=0; i<window.uploadSize; i++) {

		/* SUBMIT SINGLE FILE */
		var myform = new FormData()
		myform.append('file',files[i]);
		myform.append('csrfmiddlewaretoken',csrf);
		myform.append('fid',fid);

		/* MAKE SYNCHRONIZED REQUEST TO BACKEND */
		$.ajax({
      			url: url,
      			type: 'POST',
			async: false,
      			data: myform,
      			processData: false,
      			contentType: false,
                	success: function(data) {
                        		if (data.status==0) {
                        			alert("ERROR " + files[i].name);
                        			alert(msg);
                                		alert(data.message);
                        		}
					progress(parseInt(100*i/window.uploadSize)+"%");
                	},
                	error: function(e,msg) {
					progress(parseInt(100*i/window.uploadSize)+"%");
                        		alert("ERROR " + files[i].name + " " + msg);
                	}
    		});
	}

	/* RELOAD WHEN EVERYTHING IS DONE */
	shadowOff();
	progress('100%');
	location.reload();
}

/* COMPRESS FOLDER */
function zipFolder(){

	/* GET PARENT ID */
	progress('20%');
	var fid = $("#FOLDERID").val();

	/* GENERATE DATA */
	var data 	= {};
	data['fid'] 	= fid;

	/* MAKE REQUEST */
	shadowOn();
	progress('50%');
	var url = "/folder/zip/";
	$.ajax({
		type: 		"GET",
                data:		data,
                dataType:	'json',
                url: 		url,
                success: 	function(data) {
                        		if (data.status==0) {
						progress('0%');
                                		alert(data.message);
						shadowOff();
                        		} else {
						progress('100%');
						shadowOff();
						prompt("Clave",data.pass);
						progress('0%');
						location.href="/media/"+data.src;
                        		}
                		},
                error: 		function(e,msg) {
					progress('0%');
                        		alert("ERROR");
                        		alert(msg);
					shadowOff();
                }
        });
}
