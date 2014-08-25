
/* EDIT A FILE NAME */
function editFile(){

        /* GET FOLDER NAME */
        progress('20%');
        var current = $("#FILENAME").val();
        var name = prompt("Nuevo nombre?",current);
        if (!name) {
                progress('0%');
                return;
        }

	/* GET FILE ID */
        progress('40%');
        var fid = $("#FILEID").val();

        /* GENERATE DATA */
        var data        = {};
        data['fid']     = fid;
        data['name']    = name;

	/* MAKE REQUEST */
        var url = "/gallery/mod/";
        $.ajax({
                type:           "GET",
                data:           data,
                dataType:       'json',
                url:            url,
                success:        function(data) {
                                        if (data.status==0) {
                                                progress('0%');
                                                alert(data.message);
                                        } else {
                                                progress('100%');
                                                location.reload();
                                        }
                                },
                error:          function(e,msg) {
                                        progress('0%');
                                        alert("ERROR");
                                        alert(msg);
                }
        });
}

/* REMOVE A FILE */
function removeFile(){

	/* CONFIRM */
        progress('20%');
	if (!confirm('Está seguro que desea borrar este archivo?')) {
        	progress('0%');
		return;
	}

	/* GET FILE ID */
        progress('40%');
        var fid = $("#FILEID").val();

	/* GET FATHER ID */
        progress('60%');
        var next= $("#FOLDERID").val();

        /* GENERATE DATA */
        var data        = {};
        data['fid']     = fid;

	/* MAKE REQUEST */
        var url = "/gallery/rem/";
        $.ajax({
                type:           "GET",
                data:           data,
                dataType:       'json',
                url:            url,
                success:        function(data) {
                                        if (data.status==0) {
                                                progress('0%');
                                                alert(data.message);
                                        } else {
                                                progress('100%');
						location.href='/folder/'+next+'/';
                                        }
                                },
                error:          function(e,msg) {
                                        progress('0%');
                                        alert("ERROR");
                                        alert(msg);
                }
        });
}
	
/* TOGGLE FULLSCREEN */
function toggleFullScreen(elem) {
    if ((document.fullScreenElement && document.fullScreenElement !== null) || (document.msfullscreenElement && document.msfullscreenElement !== null) || (!document.mozFullScreen && !document.webkitIsFullScreen)) {
        if (elem.requestFullScreen) {
            elem.requestFullScreen();
        } else if (elem.mozRequestFullScreen) {
            elem.mozRequestFullScreen();
        } else if (elem.webkitRequestFullScreen) {
            elem.webkitRequestFullScreen(Element.ALLOW_KEYBOARD_INPUT);
        } else if (elem.msRequestFullscreen) {
            elem.msRequestFullscreen();
        }
    } else {
        if (document.cancelFullScreen) {
            document.cancelFullScreen();
        } else if (document.mozCancelFullScreen) {
            document.mozCancelFullScreen();
        } else if (document.webkitCancelFullScreen) {
            document.webkitCancelFullScreen();
        } else if (document.msExitFullscreen) {
            document.msExitFullscreen();
        }
    }
}
	
/* UPDATE METADATA */	
function updateMetadata(id,name,fid,fname,cid,lid) {

	/* METADATA FIELDS */
	$("#FILEID").val(id);
	$("#FILENAME").val(name);
	$("#FOLDERID").val(fid);
	$("#PLAYINDEX").val(cid);
	$("#PLAYLIST").val(lid);

}

/* CLEAR PATH */
function clearPath() { $('#TOOLBAR .breadcrumb .dynamicPath').remove(); }

/* ADD TO PATH */
function addPath(fid,fname) { 
	var html = '<li class="dynamicPath"><a href="/folder/'+fid+'/">'+fname+'</a></li>'	
	$('#TOOLBAR .breadcrumb').append(html);
}

/* ADD FILE TO PATH */
function addFilePath(id,name) { 
	var html = '<li class="dynamicPath active"><a href="/gallery/'+id+'/">'+name+'</a></li>'	
	$('#TOOLBAR .breadcrumb').append(html);
}

/* LOAD IMAGE */
function loadImage(src) { $("#MEDIA_IMAGE").show(); $("#MEDIA_IMAGE").attr('src','/media/'+src); }
function loadText(src)  { $("#MEDIA_TEXT").show();  $("#MEDIA_TEXT").html(value); }
