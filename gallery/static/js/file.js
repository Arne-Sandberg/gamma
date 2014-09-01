
/* ***************************************************
 * 
 * 	PLAY ONE FILE.-
 * 
 * *************************************************** */
function playme(elem) {
	
	/* UPDATE QUEUE */
	window.NOW_PLAYING = elem;
	// alert(JSON.stringify(elem));

	/* Update metadata */
	setFileID(elem.id);
	setFileName(elem.name);
	setFileType(elem.ftype);
	setFolderID(elem.folder_id);
	setFolderName(elem.folder_name);
	setFilePath(elem.fname);

	/* Update path */
	clearPath();
	for (p in elem.path) 
		addPath(elem.path[p][0], elem.path[p][1])
	addPath(elem.folder_id,elem.folder_name);
	addFilePath(elem.id,elem.name);

	/* Update download path */
	var dw = $('#downloadLink');
	dw.attr('href','/media/'+elem.fname);
	dw.attr('download',elem.name);

	/* CHANGE WINDOW NAME & WINDOW LOCATION WITHOUT RELOAD */
	document.title = elem.name;
	var myurl = '/gallery/'+elem.id+'/';
	history.pushState(null, null, myurl)

	/* HIDE CURRENT MEDIA */
	$('#MEDIA_CONTAINER div *').css('display','none');
	$('#MEDIA_CONTAINER div *').hide('fast');

	/* CLEAR MEDIA ELEMENTS */ 
	$('#MEDIA_IMAGE').attr('src','');
	$('#MEDIA_VIDEO').attr('src','');
	$('#MEDIA_FRAME').attr('src','');

	/* DISPLAY MEDIA */
	if ( elem.ftype == 'IMG' ) 
		$('#MEDIA_IMAGE').attr('src','/media/'+elem.fname).fadeIn(300);

	/* PLAY VIDEO */
	else if ( elem.ftype == 'VID') { 
		progress('10%');
		var flashvars_1990 = {};
		var params_1990 = {
        		quality:                "high",
        		wmode:                  "transparent",
        		bgcolor:                "#ffffff",
        		allowScriptAccess:      "always",
        		allowFullScreen:        "true",
        		flashvars:              "fichier="+encodeURIComponent('/media/'+elem.fname)
		};
		var attributes_1990 = {
			id: 'mediaPlayer'
		};
		progress('50%');
		// flashObject('/static/flash/watch_as3.swf', "MEDIA_VIDEO", "1024", "600", "8", false, 
		flashObject('/static/flash/v1_26.swf', "MEDIA_VIDEO", "1024", "600", "8", false, 
							flashvars_1990, params_1990, attributes_1990);
		$("#MEDIA_VIDEO").fadeIn();
		progress('100%');
		setTimeout(function(){ progress('0%'); },400);
	}

	/* PLAY MUSIC */
	else if ( elem.ftype == 'AUD') { 
		var flashvars_9719 = {};
		var params_9719 = {
			quality: "high",
			wmode: "transparent",
			bgcolor: "#ffffff",
			allowScriptAccess: "always",
			allowFullScreen: "true",
			flashvars: "url="+encodeURIComponent('/media/'+elem.fname)+"&autostart=on"
		};
		var attributes_9719 = {
			id: 'mediaPlayer'
		};
		flashObject("/static/flash/s_8.swf", "MEDIA_SOUND", "90%", "50", "8", false, 
						flashvars_9719, params_9719, attributes_9719);
		$("#MEDIA_SOUND").fadeIn();
		progress('100%');
		setTimeout(function(){ progress('0%'); },400);
	}

	/* ADD EVENT */ 
	$(window).load(function(){
	var obj = $("#MEDIA_SOUND object embed");
	obj.bind('onStateChange',onPlayerStateChange);
	obj.bind('onFinish',onPlayerStateChange);
	obj.bind('finish',onPlayerStateChange);
	alert(obj.id);
	});

	/* END */
	// alert(JSON.stringify(elem));
}

function onPlayerStateChange (state) {
	alert(3);
	alert(state);
    if (state === 0) {
        alert("Stack Overflow rocks!");
    }
};

/* ***************************************************
 * 
 * 	PLAY NEXT AND PREVIOUS 
 * 
 * *************************************************** */
function playNext() { 

	// Return if player is in progress or play is locked 
	// or if the queue is empty.-
	if (fetchInProgress())
		return;
	if (isPlayLocked())
		return;
 	lockPlay();
	if (window.QUEUE_NEXT.length<2) 
		return;

	// Add current to the top of the previous cache.-
	window.QUEUE_PREVIOUS.push(window.NOW_PLAYING);

	// Get first element of the next cache.-
	window.NOW_PLAYING = window.QUEUE_NEXT.shift();

	// Move cursor up.-
	setCursorUp();

	// Async fetch for other elements.-
	playme(window.NOW_PLAYING);

	// Automatic fetch for other elements.-
	fetch();	

	// Release lock.- 
	unlockPlay();
}
function playPrevious() {

	// Return if player is in progress or play is locked 
	// or if the queue is empty.-
	if (fetchInProgress())  
		return;
	if (isPlayLocked())
		return;
	if (window.QUEUE_NEXT.length<2) 
		return;
 	lockPlay();

	// Add current to the beginning of the next cache.-
	window.QUEUE_NEXT.unshift(window.NOW_PLAYING);

	// Get last element of the previous cache.-
	window.NOW_PLAYING = window.QUEUE_PREVIOUS.pop();

	// Move cursor down.-
	setCursorDown();

	// Play that element.-
	playme(window.NOW_PLAYING);

	// Async fetch for other elements.-
	fetch();	

	// Release lock.- 
	unlockPlay();
}

/* PREVENT FROM PLAYING TOO FAST */
window.PLOCK = false;
function lockPlay() 	{ window.PLOCK = true; }
function unlockPlay() 	{ window.PLOCK = false; }
function isPlayLocked() { return window.PLOCK == true; }
