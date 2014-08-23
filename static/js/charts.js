/*****************************************************************
 * LOAD GRAPHS
 *****************************************************************/
function reload_graphs() {
	$("#GRAPHS DIV").empty();
} 

/*****************************************************************
 * DRAW A BAR CHART
 *****************************************************************/
function bar_chart(divid,legend,title,colors,rows) {
	// Validate arguments
	divid 	= typeof divid 	!== 'undefined' ? divid 	: 'visualization';
	legend 	= typeof legend	!== 'undefined' ? legend	: 'none';
	colors	= colors 			? colors	: null;
	title	= typeof title	!== 'undefined' ? title		: '';
	if ( !divid || !rows ) { alert("Can't load graphs properly"); return; }
	// Create new graphic
	var data = google.visualization.arrayToDataTable(rows);
	new google.visualization.BarChart(document.getElementById(divid)).draw(data, {
		isStacked: true,
		title: title, 
		legend: legend,
                backgroundColor: 'transparent', 
                colors: colors,
	});
}

/*****************************************************************
 * DRAW A PIE CHART
 *****************************************************************/
function pie_chart(divid,legend,title,rows,colors) {
	// Validate arguments
	divid 	= typeof divid 	!== 'undefined' ? divid 	: 'visualization';
	legend 	= typeof legend	!== 'undefined' ? legend	: 'none';
	colors	= colors 			? colors	: null;
	title	= typeof title	!== 'undefined' ? title		: '';
	if ( !divid || !rows ) { alert("Can't load graphs properly"); return; }
	// Create new graphic
	var data = google.visualization.arrayToDataTable(rows);
	new google.visualization.PieChart(document.getElementById(divid)).draw(data, {
		title: title, 
		legend:legend,
                backgroundColor: 'transparent', 
                colors: colors,
	});
}

/*****************************************************************
 * DRAW A LINE TREND.-
 *****************************************************************/
function line_chart(divid,legend,title,colors,cols,rows,trend) {
	// Validate arguments
	divid 	= typeof divid 	!= 'undefined'  ? divid 	: 'visualization';
	legend 	= typeof legend	!= 'undefined'  ? legend	: 'none';
	title	= typeof title	!= 'undefined'  ? title		: '';
	colors	= colors 			? colors	: ['black'];
	trend   = typeof trend	!= 'undefined'  ? trend		: { 0:{} };
	if ( !divid || !cols || !rows ) { alert("Can't load graphs properly"); return; }
	// Create new graphic
	var data = data_table(cols,rows);
	new google.visualization.LineChart(document.getElementById(divid)).draw(data, {
		curveType: "function", 
		pointSize: 4, 
		title: title, 
                width: '100%', 
		height: '100%', 
		hAxis: {direction: 1}, 
		trendlines: trend,
		legend:legend,
                backgroundColor: 'transparent', 
                colors: colors,
	});
}

/*****************************************************************
 * CREATE A GOOGLE DATA TABLE.-
 *****************************************************************/
function data_table(cols,rows) {
	if ( !cols || !rows ) { alert("Can't create data table properly"); return; }
	var data = new google.visualization.DataTable();
	// Set table columns.-
	for( var i=0; i<cols.length; i++ ) {
		data.addColumn(cols[i][0],cols[i][1]);
	}		
	// Set table rows.-
	for( var i=0; i<rows.length; i++ ) {
		data.addRows([rows[i]])	
	}
	return data;
}
