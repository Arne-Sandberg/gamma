
/* ***************************************************
 * 
 * 	TOGGLE FULLSCREEN
 * 
 * *************************************************** */
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
	$('.navbar').hide();
	$('.progress').hide();
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
	$('.navbar').show();
	$('.progress').show();
    }
}

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
	var animSpeed = 100; 
	$('.media_display').fadeOut(animSpeed,function() {
		if ($(".media_display:animated").length === 0) {

			/* CLEAR MEDIA ELEMENTS */ 
			$('#MEDIA_IMAGE').attr('src','');
			$('#MEDIA_FRAME').attr('src','');

			/* DISPLAY MEDIA */
			if ( elem.ftype == 'IMG' ) {
				$('#MEDIA_IMAGE').attr('src','/media/'+elem.fname);
				$('#MEDIA_IMAGE').fadeIn(animSpeed);
			}

		}
	});

	/* END */
	// alert(JSON.stringify(elem));
}

/* ***************************************************
 * 
 * 	DISPLAY CONTENT.-
 * 
 * *************************************************** */
function displayImage(src) {
	clearDisplays(function(){ 
	});
}
function displayFile() {
	clearDisplays(function(){ 
	});
}
function displayFrame(src) {
	clearDisplays(function(){ 
		$('#MEDIA_FRAME').attr('src','/media/'+src);
		$('#MEDIA_FRAME').fadeIn('slow');
	});
}
function clearDisplays(callback) {

}

/* ***************************************************
 * 
 * 	PLAY NEXT AND PREVIOUS 
 * 
 * *************************************************** */
function playNext() { 
	
	// Check queue size.-
	if (window.QUEUE_NEXT.length<2) 
		return;

	// Add current to the top of the previous cache.-
	window.QUEUE_PREVIOUS.push(window.NOW_PLAYING);

	// Get first element of the next cache.-
	window.NOW_PLAYING = window.QUEUE_NEXT.shift();

	// Move cursor up.-
	setCursorUp();

	// Automatic fetch for other elements.-
	fetch();	

	// Async fetch for other elements.-
	playme(window.NOW_PLAYING);
}
function playPrevious() {
	
	// Check queue size.-
	if (window.QUEUE_PREVIOUS.length<2) 
		return;

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
}
