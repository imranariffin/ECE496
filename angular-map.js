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

  var hosts = [
  {
    host: "Casa Loma",
    desc: "1",
    lat:43.6924298, 
    lng:-79.4413491
  }, 
  {
    host: "Upper Canada College",
    desc: "2",
    lat:43.6941412, 
    lng:-79.3981012
  },
  {
    host: "Spadina Station",
    desc: "3",
    lat: 43.6711836, 
    lng: -79.4022474
  },
  {
    host: "Dundurn Castle",
    desc: "4",
    lat: 43.2736872,
    lng: -79.8657758
  },
  {
    host: "Niagara Falls",
    desc: "5",
    lat:43.054098,
    lng:-79.2281196
  },
  {
    host: "Hillcrest",
    desc: "6",
    lat:43.8678357,
    lng:-79.4245072
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
    
    for (i = 0; i < cities.length; i++) {
        createMarker(cities[i]);
    }

    /* 
      loading the Markers on a map for the selected city
    */
    var createMarkerForCity = function (info, map){
      // imran tests infoWindow @ imran-7-infowindow
      marker = new google.maps.Marker({
        map: map,
        position: new google.maps.LatLng(info.lat, info.lng)
      });

      google.maps.event.addListener(marker, 'click', function() {
        // infoWindow is defined at "./infoWindow.js"
        infoWindow = createInfoWindow();
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

      for (i = 0; i < hosts.length; i++) {
        createMarkerForCity(hosts[i], map);
      }
    }

});


/* unused functions */
    // $scope.openInfoWindow = function(e, selectedMarker){
    //     e.preventDefault();
    //     google.maps.event.trigger(selectedMarker, 'click');
    // }