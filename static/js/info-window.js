/* 
	Call this function to create a custom InfoWindow. In order to be
	able to call this function, load the javascript first.
	i.e. <script src="infoWindow.js"></script>
 */
function createInfoWindow (options) {
	var title, desc;
	if (options) {
		title = options.title;
		desc = options.desc;
	}
	var iWindowContentString = 
	"<div>" +
	" 	<h5> " + title + " </h5>" +
	" 	<p>" + desc + "</p>" +
	"	<p><a href='#'>link</a> to location info" +
	"	</p>" +
	"</div>";
	var infoWindow = new google.maps.InfoWindow({
	content: iWindowContentString
	});
	return infoWindow;
}

