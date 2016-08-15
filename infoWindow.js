/* 
	Call this function to create a custom InfoWindow. In order to be
	able to call this function, load the javascript first.
	i.e. <script src="infoWindow.js"></script>
 */
function createInfoWindow (infoWindow) {
	var iWindowContentString = 
	"<div>" +
	" 	<h5> Location_Name </h5>" +
	" 	<p>Some description</p>" +
	"	<p><a href='#'>link</a> to location info" +
	"	</p>" +
	"</div>";
	infoWindow = new google.maps.InfoWindow({
	content: iWindowContentString
	});
	return infoWindow;
}