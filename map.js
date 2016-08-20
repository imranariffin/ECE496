/*
  All global functions and variables related to map is declared 
  and define here
*/

var map;
var infoWindow; // assure only one infoWindow

function Map(mapOptions) {
  this.gMap = new google.maps.Map(document.getElementById('map'), mapOptions);
}

/* constructor for world map */
function WorldGoogleMap (mapOptions) {
  Map.call(this, mapOptions);
  // google.maps.Map.call(this, document.getElementById('map'), mapOptions);
  // this.gMap = new google.maps.Map(document.getElementById('map'), mapOptions);
  this.cityMarkers = [];

  WorldGoogleMap.prototype.addCityMarker = function (marker) {
    this.cityMarkers.push(marker);
  }
}

/* constructor for city map */
function CityGoogleMap (mapOptions) {
  Map.call(this, mapOptions);
  // var cityMap = new google.maps.Map(document.getElementById('map'), mapOptions);

  /* 
    map member data defined below
  */
  this.hosterMarkers = [];
  this.markerClusterer = null;

  /* 
    map events defined below 
  */
  this.gMap.addListener('zoom_changed', function() {
    // prevent zooming out too far away
    if (this.getZoom() <= 7) {
      this.setZoom(8);
    }
  });
  

  /* 
    map methods defined below
  */

  /* 
    Use this function everytime a new marker is made so that
    we have control of all markers
  */
  CityGoogleMap.prototype.addHosterMarker = function (marker) {
    this.hosterMarkers.push(marker);
  }
  /*
    Group hoster markers into clusters when they exceed a certain density.
    Don't need to supply the markers, it uses the global var hosterMarkers
    for list of markers to cluster
  */
  CityGoogleMap.prototype.clusterizeHosterMarkers = function () {
    markerClusterer = new MarkerClusterer(this.gMap, [], {
      gridSize: 100, 
      maxZoom: 15, 
      imagePath: 'img/marker-cluster'
    });
    // load hosterMarkers to MarkerClusterer
    this.hosterMarkers.forEach(function(marker) {
      this.markerClusterer.addMarker(marker);
    });
  }

  // return cityMap;
}

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




var createHosterMarker = function (map, place){
  // imran tests infoWindow @ imran-7-infowindow
  var marker = GMapMarker('hoster', {
    map: map,
    position: new google.maps.LatLng(place.lat, place.lng),
    title: place.host
  });
  var contentString = '<div id="content" Style = "width: 483px; height: 144px">'+
    '<div id = "wi-head" class = "row">'+
      '<div class="col-xs-2">'+
        '<img src="https://s3-media4.fl.yelpcdn.com/bphoto/GqZdB0uAO54gbDHlG_VI6A/90s.jpg" alt="Porcelain Factory of Vista Alegre" height="60" width="60">'+
      '</div>'+
      '<div Style = "padding-left: 5px"; class="col-xs-5" >'+
        '<h4 id="firstHeading">'+
          place.host+
        '</h4>'+
        '<p>Rating: <img src="http://cliparts.co/cliparts/gce/oXx/gceoXx7gi.png" height="20" width="50"></p>'+
      '</div>'+
      '<div Style = "padding-top: 3px"; class="col-xs-5">'+
        '<p Style = "margin-bottom: 5px">Phone: 647-830-8636</p>' +
        '<p>Email: richard874410593@gmail.com</p>' +
      '</div>'+
    '</div>' +
    '<div  id="bodyContent">'+
      '<p>Description: sacred to the Pitjantjatjara and Yankunytjatjara, the '+
      'Aboriginal people of the area. It has many springs, waterholes, '+
      'Heritage Site. <a href="url">Read more</a></p>'+
      '<hr Style = "margin-bottom: 5px; margin-top: 5px">'+
      '<p> <a href="url">Save</a>  |  <a href="url">Facebook</a>   |   <a href="url">Twitter</a>   </p>' + 
    '</div>'+
  '</div>';
  if (infoWindow)
    infoWindow.close();
  infoWindow = createInfoWindow();
  google.maps.event.addListener(marker, 'click', function() {
    // infoWindow is defined at "./infoWindow.js"
    infoWindow.setContent(contentString);
    infoWindow.open(map, this);
  });
  return marker;
}

/* 
  loading the Markers on a map for the selected city: from world map to city map
*/
function clickCity(marker, hoster) {
  map = new CityGoogleMap({
    zoom: 8,
    center: marker.getPosition()
  });

  var hosts = hoster;
  for (i = 0; i < hosts.length; i++) {
    map.addHosterMarker(createHosterMarker(map.gMap, hosts[i]));
  }
  map.clusterizeHosterMarkers();
}


var createCityMarker = function (map, place){
  var marker = GMapMarker("city", {
      map: map,
      position: new google.maps.LatLng(place.lat, place.lng),
      title: place.city
  });

  if (infoWindow)
    infoWindow.close();
  var infowindow = new google.maps.InfoWindow();
  var content = '<div Style = "text-align: center; width: 80px; height: 30px; padding: 0px; margin: 0px">' +
    '<h5>' + 
      marker.title + 
    '</h5>'+
  '</div>';

  //for the zoom in effect
  google.maps.event.addListener(marker, 'click', function(){
    clickCity(marker, place.hoster);
  });
  
  //display the city name
  google.maps.event.addListener(marker, 'mouseover', (function(marker, content, infowindow) {
    return function() {
      infowindow.setContent(content);
      infowindow.open(map.gMap, marker);
    };
  })(marker, content, infowindow));
  google.maps.event.addListener(marker, 'mouseout', (function(marker, content, infowindow) {
    return function() {
      infowindow.close();
    };
  })(marker, content, infowindow));    

  return marker;    
}