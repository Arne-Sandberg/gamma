
/* ***************************************************
 * 
 * 	EDIT FILE 
 * 
 * *************************************************** */
function editFile(){

        /* GET FOLDER NAME */
        progress('20%');
        var current = getFileName();
        var name = prompt("Nuevo nombre?",current);
        if (!name) {
                progress('0%');
                return;
        }

	/* GET FILE ID */
        progress('40%');
        var fid = getFileID();

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

/* ***************************************************
 * 
 * 	REMOVE A FILE 
 * 
 * *************************************************** */
function removeFile(){

	/* CONFIRM */
        progress('20%');
	if (!confirm('Está seguro que desea borrar este archivo?')) {
        	progress('0%');
		return;
	}

	/* GET FILE ID */
        progress('40%');
        var fid = getFileID();

	/* GET FATHER ID */
        progress('60%');
        var next = getFolderID();

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

/* ***************************************************
 * 
 * 	FETCH A GROUP OF FILES
 * 
 * *************************************************** */
function fetch(){

	/* GENERATE URL */
        var url = "/gallery/fetch/?";
	url = url + "&cursorID="+getCursorID();	
	url = url + "&playlistID="+getPlaylistID();	
	if ( isRandom() ) 
        	url = url + "&random=1";
	if ( QUEUE_NEXT.length < getCacheFetch() ) 
        	url = url + "&fetchNext=1";
	if ( QUEUE_PREVIOUS.length < getCacheFetch() )
        	url = url + "&fetchPrevious=1";
	// alert(url);

	/* MAKE REQUEST */
        $.ajax({
                type:           "GET",
                dataType:       'json',
                url:            url,
                success:        function(data) {
                                        if (data.status==0) {
                                                alert(data.message);
                                        } else {
						/* UPDATE QUEUES */
						// alert(JSON.stringify(data.cachePrevious));
						// alert(JSON.stringify(data.cacheNext.length));
						if ( data.cacheNext.length>1) {
							buffer = new Array;
							for (c in data.cacheNext) 	
								buffer.push(data.cacheNext[c]);	
							window.QUEUE_NEXT = buffer;
						}
						if ( data.cachePrevious.length>1) {
							buffer = new Array;
							for (c in data.cachePrevious) 	
								buffer.push(data.cachePrevious[c]);
							window.QUEUE_PREVIOUS = buffer;
						}
                                        }
                                },
                error:          function(e,msg) {
                                        alert("ERROR " + msg);
                }
        });
}

/* ***************************************************
 * 
 * 	FETCH ONE ELEMENT.-
 * 
 * *************************************************** */
function fetchOne(id,playlistID,callback) {
        var url = "/gallery/get/"+id+"/";
	if (playlistID) 
		url = url + "&?playlistID="+playlistID;
        $.ajax({
                type:           "GET",
                dataType:       'json',
                url:            url,
                success:        function(data) {
                                        if (data.status==0) {
                                                alert(data.message);
                                        } else {
						/* UPDATE METADATA */
						setCursorID(data.cursorID);
						setPlaylistID(data.playlistID);
						setPlaylistCount(data.playlistCount);
						setCacheSize(data.cache_size);
						setCacheFetch(data.cache_fetch);
						playme(data.file);
						callback();
                                        }
                                },
                error:          function(e,msg) {
                                        alert("ERROR " + msg);
                }
        });
}
