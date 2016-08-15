var map;
var marker;
var infoWindow;

/*
This function is a callback that is called right after
google.map javascript is done loading
*/
function initMap() {
  var torontoLocation = {lat: 43.6765211, lng: -79.4354023};
  map = new google.maps.Map(document.getElementById('map'), {
    center: torontoLocation,
    zoom: 8
  });

  // imran tests infoWindow @ imran-7-infowindow
  marker = new google.maps.Marker({
    map: map,
    position: torontoLocation
  });
  google.maps.event.addListener(marker, 'click', function() {
    // infoWindow is defined at "./infoWindow.js"
    infoWindow = createInfoWindow(infoWindow);
    infoWindow.open(map, this);
  });
}

/* add a marker */
function addMarker(lat, lng) {
  var latLng = new google.maps.LatLng({lat: lat, lng: lng});
  createMarker(latLng);
}

function createMarker(position) {
  var marker = new google.maps.Marker({
    map: map,
    position: position
  });

  google.maps.event.addListener(marker, 'click', function() {
    infoWindow.setContent("New Marker");
    infoWindow.open(map, this);
  });
}

// /* onClick to run add marker function */
// var addMarkerBtn = document.getElementById("addMarkerBtn");      
// addMarkerBtn.onclick = function addMarkerOnClick() {
//   // console.log(document.getElementById("latInput").value);
//   var lat = parseFloat(document.getElementById("latInput").value);
//   var lng = parseFloat(document.getElementById("lngInput").value);
//   addMarker(lat, lng);
// }

/* onChange to the city location*/
function changeCity() {
  var index = document.getElementById("city").value;
  var cityLocation = [{lat:43.6765211, lng:-79.4354023}, {lat:40.7142700, lng:-74.0059700}, {lat:37.7749300, lng:-122.4194200}, {lat:49.246292, lng:-123.116226}];
  map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: cityLocation[index].lat, lng:  cityLocation[index].lng},
    zoom: 8
  });
  // imran tests infoWindow @ imran-7-infowindow
  marker = new google.maps.Marker({
    map: map,
    position: cityLocation[index]
  });
  google.maps.event.addListener(marker, 'click', function() {
    // infoWindow is defined at "./infoWindow.js"
    infoWindow = createInfoWindow(infoWindow);
    infoWindow.open(map, this);
  });
}