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

      google.maps.event.addListener(marker, 'click', function() {
        // infoWindow is defined at "./infoWindow.js"
        infoWindow.setContent(contentString);
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