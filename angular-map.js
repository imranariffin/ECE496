//Angular App Module and Controller


var sampleApp = angular.module('mapsApp', []);
sampleApp.controller('MapCtrl', function ($scope, $http) {
  $http.get('data.json').success(function(data) { 
    var cities = data; 

    var mapOptions = {
        zoom: 4,
        center: new google.maps.LatLng(45.8996835,-95.2071532)
    }

    $scope.cities = cities;
    $scope.map = new google.maps.Map(document.getElementById('map'), mapOptions);
    $scope.markers = [];
    
    var infoWindow = createInfoWindow();
    var createMarker = function (place){
        var marker = GMapMarker("hoster", {
            map: $scope.map,
            position: new google.maps.LatLng(place.lat, place.lng),
            title: place.city
        });
        marker.content = '<div class="infoWindowContent">' + place.desc + '</div>';
        
        google.maps.event.addListener(marker, 'click', function(){
            infoWindow.setContent('<h2>' + marker.title + '</h2>' + marker.content);
            infoWindow.open($scope.map, this);
        });
        
        $scope.markers.push(marker);
        
    }  
    
    for (i = 0; i < cities.length; i++) {
        createMarker(cities[i]);
    }

    /* 
      loading the Markers on a map for the selected city
    */
    var createMarkerForCity = function (place, map){
      // imran tests infoWindow @ imran-7-infowindow
      var marker = GMapMarker('city', {
        map: map,
        position: new google.maps.LatLng(place.lat, place.lng),
        title: place.host
      });
      marker.content = '<div class="infoWindowContent">' + place.desc + '</div>';

      google.maps.event.addListener(marker, 'click', function() {
        // infoWindow is defined at "./infoWindow.js"
        infoWindow.setContent('<h2>' + marker.title + '</h2>' + marker.content);
        infoWindow.open(map, this);
      });

    }

    /* 
      onChange to the city location
      called when dropdown item is select item (id:selectCity) is clicked
      to change map.
    */
    $scope.changeCity = function () {  
      var index = $scope.cityIndex;
      var cityLocation = cities[index];

      map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: cityLocation.lat, lng: cityLocation.lng},
        zoom: 8
      });

      var hosts = cityLocation.hoster
      for (i = 0; i < hosts.length; i++) {
        createMarkerForCity(hosts[i], map);
      }
    }
  });

});


/* unused functions */
    // $scope.openInfoWindow = function(e, selectedMarker){
    //     e.preventDefault();
    //     google.maps.event.trigger(selectedMarker, 'click');
    // }