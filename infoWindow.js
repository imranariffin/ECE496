/* 
	Call this function to create a custom InfoWindow. In order to be
	able to call this function, load the javascript first.
	i.e. <script src="infoWindow.js"></script>
 */
function createInfoWindow (infoWindow) {
	var iWindowContentString = [
	"<div>",
	" <h3> City_Name </h3>",
	" <p>Some description</p>",
	"</div>"
	].join();
	infoWindow = new google.maps.InfoWindow({
	content: iWindowContentString
	});
	return infoWindow;
}