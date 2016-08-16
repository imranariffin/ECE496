/* 
  A custom constructor for google.maps.Marker.
  Allows you to assign a type ('hoster' or 'city') to marker.
  The icon of marker will be assigned according to type. 
  Icon image is located at ./img
*/
function GMapMarker(type, options) {
  var image = {
    // This marker is 20 pixels wide by 32 pixels high.
    size: new google.maps.Size(30, 32),
    // The origin for this image is (0, 0).
    origin: new google.maps.Point(0, 0),
    // The anchor for this image is the base of the flagpole at (0, 32).
    anchor: new google.maps.Point(0, 32),
    // 
    scaledSize: new google.maps.Size(32, 32)
  };
  if (type=="hoster") {
    image.url = "./img/marker-hoster.png";
    options.icon = image;
    return new google.maps.Marker(options);
  } else if(type=="city") {
    image.url = "./img/marker-city.png";
    options.icon = image;
    return new google.maps.Marker(options);
  } else {
    return null;
  }
}