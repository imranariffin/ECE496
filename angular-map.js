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

    var createMarker = function (info){
        
        var marker = GMapMarker("hoster", {
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