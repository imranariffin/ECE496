/*
  All main controllers should be defined here
*/

function MapController($scope, $http, $cookies) {
  /*
      This controller uses a few map-related variables from map.js
      See at the of of map.js to see their declaration.
      This controller also uses a few map-related functions defined 
      in map.js
  */

  var sessionToken1 = $cookies.get('session-token-1');
  var sessionToken2 = $cookies.get('session-token-2');

  $http
    .get('/api/city/' + sessionToken1 + '/' + sessionToken2)
    .success(function(data) { 
      var cities = data; 
      $scope.cities = cities;

      var mapOptions = {
          zoom: 4,
          center: new google.maps.LatLng(45.8996835,-95.2071532)
      }


      // map = new google.maps.Map(document.getElementById('map'), mapOptions);
      map = new WorldGoogleMap(mapOptions);
      
      for (i = 0; i < cities.length; i++) {
          map.addCityMarker(createCityMarker(map.gMap, cities[i]));
    }
  });

  /* 
    onChange to the city location
    called when dropdown item is select item (id:selectCity) is clicked
    to change map.
  */
  $scope.changeCity = function () {  
    var index = $scope.cityProfile;
    var cityLocation = index;

    // map = new google.maps.Map(document.getElementById('map'), {
    //   center: {lat: cityLocation.lat, lng: cityLocation.lng},
    //   zoom: 8
    // });
    map = new CityGoogleMap({
      zoom: 10,
      center: {lat: cityLocation.lat, lng: cityLocation.lng}
    });
    // map.setCenter({lat: cityLocation.lat, lng: cityLocation.lng});
    // map.setZoom(8);

    var hosts = cityLocation.hoster
    for (i = 0; i < hosts.length; i++) {
      map.addHosterMarker(createHosterMarker(map.gMap, hosts[i]));
    }
    map.clusterizeHosterMarkers();
  }
}