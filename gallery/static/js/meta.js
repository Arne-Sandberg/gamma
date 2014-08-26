
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

/* ***************************************************
 *
 * 	CURSOR MOVEMENT.-
 *
 * *************************************************** */
function setCursorUp () {
	var c = getCursorID();
	var t = getPlaylistCount();
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
 * 	PLAY / LOOP 
 * 	1 = Stopped.-
 *	2 = Play linear.-
 * 	3 = Play random.-
 * 	4 = Play repeat.-
 *
 * *************************************************** */

	/* PLAY STATUS */
	function setPlayStatus(val) 	{ window.PLAY_STATUS = val; }	
	function getPlayStatus() 	{ return window.PLAY_STATUS; }	
	function isStopped() 		{ return getPlayStatus()==1; }
	function isPlaying() 		{ return getPlayStatus()==2; }
	function isRandom()  		{ return getPlayStatus()==3; }
	function isLoop()    		{ return getPlayStatus()==4; }
	function nextPlayStatus() { 
		var p = getPlayStatus();
		p++;
		if (p>4)
			p = 1;
		setPlayStatus(p);
	}

	// Set status.-
	function setPlay() {
		$('#playBtn span').hide();
		$('#playBtn #gplay').show();
		setPlayStatus(2);
			
	}
	function setRandom() {
		$('#playBtn span').hide();
		$('#playBtn #grand').show();
		setPlayStatus(3);
	}
	function setLoop() {
		$('#playBtn span').hide();
		$('#playBtn #gloop').show();
		setPlayStatus(4);
			
	}
	function setStop() {
		$('#playBtn span').hide();
		$('#playBtn #gstop').show();
		setPlayStatus(1);
	}

	/* PLAY BUTTON -> STOP -> PLAY -> RANDOM -> LOOP */
	function playBtn() {
		if (isStopped()) 
			setPlay();
		else if (isPlaying()) 
			setRandom();
		else if (isRandom()) 
			setLoop();
		else if (isLoop()) 
			setStop();
	}

