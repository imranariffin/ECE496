// Data
var cities = [
  {
    city: "Toronto",
    desc: "Home of the Maple Leaf",
    lat:43.6765211, 
    lng:-79.4354023,
    "default": "selected"
  }, 
  {
    city: "New York",
    desc: "The city that never sleeps",
    lat:40.7142700, 
    lng:-74.0059700
  }, 
  {
    city: "San Francisco",
    desc: "The Golden Gate City",
    lat:37.7749300, 
    lng:-122.4194200
  }, 
  {
    city: "Vancouver",
    desc: "The Rain City",
    lat:49.246292, 
    lng:-123.116226
  }];

//Angular App Module and Controller
var sampleApp = angular.module('mapsApp', []);
sampleApp.controller('MapCtrl', function ($scope) {

    $scope.cities = cities;

    var mapOptions = {
        zoom: 4,
        center: new google.maps.LatLng(45.8996835,-95.2071532)
    }

    $scope.map = new google.maps.Map(document.getElementById('map'), mapOptions);

    $scope.markers = [];
    
    var infoWindow = new google.maps.InfoWindow();
    
    var createMarker = function (info){
        
        var marker = new google.maps.Marker({
            map: $scope.map,
            position: new google.maps.LatLng(info.lat, info.lng),
            title: info.city
        });
        marker.content = '<div class="infoWindowContent">' + info.desc + '</div>';
        
        google.maps.event.addListener(marker, 'click', function(){
            infoWindow.setContent('<h2>' + marker.title + '</h2>' + marker.content);
            infoWindow.open($scope.map, marker);
        });
        
        $scope.markers.push(marker);
        
    }  
    
    for (i = 0; i < cities.length; i++){
        createMarker(cities[i]);
    }

    /* 
      onChange to the city location
      called when dropdown item is select item (id:selectCity) is clicked
      to change map.
    */
    $scope.changeCity = function () {  
      var index = $scope.cityIndex;
      // var index = document.getElementById("city").value;
      var cityLocation = [{lat:43.6765211, lng:-79.4354023}, {lat:40.7142700, lng:-74.0059700}, {lat:37.7749300, lng:-122.4194200}, {lat:49.246292, lng:-123.116226}];
      map = new google.maps.Map(document.getElementById('map'), {
        center: cityLocation[index],
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

});


/* unused functions */
    // $scope.openInfoWindow = function(e, selectedMarker){
    //     e.preventDefault();
    //     google.maps.event.trigger(selectedMarker, 'click');
    // }