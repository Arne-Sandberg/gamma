
/* UPLOAD FILES */
function uploadFiles(){

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
	var url = "/data/cgi/folder/add/";
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

