
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
 * 	PLAY / STOP / RANDOM / LOOP 
 * 	1 = Stopped.-
 *	2 = Play linear.-
 * 	3 = Play random.-
 * 	4 = Play repeat.-
 *
 * *************************************************** */

	/* THESE WILL HOLD THE PLAYER DATA */
	var timer = null, interval = 7000;
	function startPlayer() {
		if (timer !== null) return;
      		timer = setInterval(function () {
			var type = getFileType();
			if (type=='AUD') {
			}
			else if (type=='VID') {
			}
			else 
				playNext();
      		}, interval); 
	}
	function stopPlayer() {
		clearInterval(timer);
      		timer = null
	}	

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
		setPlayStatus(2);
		window.QUEUE_NEXT = new Array;
		window.QUEUE_PREVIOUS = new Array;
		fetch();
		startPlayer();
		$('#playBtn span').hide();
		$('#playBtn #gplay').show();
			
	}
	function setRandom() {
		setPlayStatus(3);
		window.QUEUE_NEXT = new Array;
		window.QUEUE_PREVIOUS = new Array;
		fetch();
		$('#playBtn span').hide();
		$('#playBtn #grand').show();

	}
	function setLoop() {
		$('#playBtn span').hide();
		$('#playBtn #gloop').show();
		setPlayStatus(4);
			
	}
	function setStop() {
		stopPlayer();
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

