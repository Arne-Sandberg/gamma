/*****************************************************************
 * DISPLAYS OR HIDES SOME WHOLE CLASS.-
 *****************************************************************/
function toggleAll(c) {
	$('.'+c).toggle(1);
}

/*****************************************************************
 * FADES IN AND OUT SOME CLASS
 *****************************************************************/
function fadeAll(c) {
	$('.'+c).fadeToggle();
}

/*****************************************************************
 * TOGGLES MENU OPTIONS.-
 *****************************************************************/
function toggleMenu(id) {
	// Determine if it needs to hide or display
	me 	= $("#"+id);
	display = me.css('display');
	if ( display == "none" ) {
		$(".MENU-LISTS").css('display','none');
		me.show('fast');
	} else { 
		$(".MENU-LISTS").css('display','none');
	}
}

/*****************************************************************
 * HIDES THINGS WHEN CLICKED OUTSIDE
 *****************************************************************/
$('html').click(function(e) {
	// This hides the menus when clicked outside.-
	if (e.target.className == "MENU-TITLE-IMG" )
		;
	else
		$(".MENU-LISTS").hide('fast');
	$("#.ui-datepicker").slideUp('fast');
});

/*****************************************************************
 * SHOWS SOMETHING AND HIDES
 * SOME OTHER THINGS.-
 *****************************************************************/
function show_me(c,h,callback) {
	if (c==window.current_tabs_id) 
		return;
	else
		window.current_tabs_id = c;
	for ( i=0; i<h.length; i++ ) {
		$('.'+h[i]).hide();
	}
	$('.'+c).toggle();
	if ( callback ) 
		callback()
}

/*****************************************************************
 * REDIRECTS TO ANOTHER PAGE, BUT FIRST
 * IT CHECKS WITH THE BACKEND SCRIPT WHERE TO GO.-
 *****************************************************************/
function redirect(args) {
	url = "/redirect/?"+window.QUERY_STRING+"&"+args
	$.ajax({
                type: "GET",
                dataType:'json',
                url: url,
                success: function(data) {
                        if (data.error) 
                                alert(data.error);
                        else 
				location.href="?"+data.url;
                },
                error: function(e,msg) {
                        alert("ERROR");
                        alert(msg);
                }
        });		
}

/*****************************************************************
 * CONFIRM BEFORE REMOVING SOMETHING IMPORTANT.-
 *****************************************************************/
function confirmlink(url) {
	if ( confirm("Are you sure?") )
		location.href = url;
}
