
/* UPDATE PROGRESS BAR*/
function progress(i) {
	$('#main-progress').css('width',i);
}

/* TOGGLE SHADOW ON AND OFF */
function shadowOn() {
	$('#shadow').fadeIn('400');
	//$('#shadow').css('display','block');
}
function shadowOff() {
	$('#shadow').fadeOut('400');
	//$('#shadow').css('display','none');
}
