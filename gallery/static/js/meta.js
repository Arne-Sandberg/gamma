
/* ***************************************************
 *
 * 	METADATA 
 *
 * *************************************************** */

	/* METADATA SETTERS */	
	function setFileID(val) 	{ window.FILEID = val; }
	function setFileName(val) 	{ window.FILENAME = val; }
	function setFileType(val) 	{ window.FILETYPE = val; }
	function setFolderID(val) 	{ window.FOLDERID = val; }
	function setFolderName(val) 	{ window.FOLDERNAME = val; }
	function setFolderID(val) 	{ window.FOLDERID= val; }
	function setCacheSize(val) 	{ window.playlistCacheSize = val; }
	function setCacheFetch(val) 	{ window.playlistCacheFetch = val; }
	function setPlaylistID(val) 	{ window.PLAYLISTID = val; } 
	function setCursorID(val)   	{ window.CURSORID = val; } 
	function setPlaylistCount(val) 	{ window.PLAYLISTCOUNT = val; } 
	function setFilePath(val) 	{ window.FILEPATH = val; } 

	/* METADATA GETTERS */
	function getFileID() 		{ return window.FILEID; }
	function getFileName() 		{ return window.FILENAME; }
	function getFileType() 		{ return window.FILETYPE; }
	function getFileName() 		{ return window.FILENAME; }
	function getFolderID() 		{ return window.FOLDERID; }
	function getFolderName() 	{ return window.FOLDERNAME; }
	function getCacheSize() 	{ return window.playlistCacheSize; }
	function getCacheFetch() 	{ return window.playlistCacheFetch; }
	function getPlaylistID() 	{ return window.PLAYLISTID; } 
	function getCursorID()   	{ return window.CURSORID; } 
	function getPlaylistCount() 	{ return window.PLAYLISTCOUNT; } 
	function getFilePath() 		{ return window.FILEPATH; } 

/* ***************************************************
 *
 * 	CURSOR MOVEMENT.-
 *
 * *************************************************** */

	function setCursorUp () {
		var c = getCursorID();
		var t = getPlaylistCount()-1;
		if ( c == t ) 
			c = 0;
		else
			c++;
		setCursorID(c);
	}
	function setCursorDown () {
		var c = getCursorID();
		var t = getPlaylistCount();
		if ( c<0 ) 
			c = t-1;
		else
			c--;
		setCursorID(c);
	}

/* ***************************************************
 *
 * 	PATH
 *
 * *************************************************** */

	function clearPath() { $('#TOOLBAR .breadcrumb .dynamicPath').remove(); }
	function addPath(fid,fname) { 
		var html = '<li class="dynamicPath"><a href="/folder/'+fid+'/">'+fname+'</a></li>'	
		$('#TOOLBAR .breadcrumb').append(html);
	}
	function addFilePath(id,name) { 
		var html = '<li class="dynamicPath active"><a href="/gallery/'+id+'/">'+name+'</a></li>'	
		$('#TOOLBAR .breadcrumb').append(html);
	}

/* ***************************************************
 *
 * 	SWITCH RANDOM.-
 *
 * *************************************************** */

	/* PLAY STATUS */
	function isRandom()  		{ return window.RANDOM == 1; }
	function switchRandom() 	{
		if (isRandom()) {
			window.RANDOM = 0;
			$('#playBtn #rand').hide();
			$('#playBtn #none').show();
		}
		else {
			window.RANDOM = 1;
			$('#playBtn #none').hide();
			$('#playBtn #rand').show();
		}
		window.QUEUE_NEXT 	= new Array;
		window.QUEUE_PREVIOUS 	= new Array;
		fetch();

	}

