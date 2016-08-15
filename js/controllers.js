

angular.module('appMaps', ['uiGmapgoogle-maps'])
    .controller('mainCtrl', function($scope) {
        $scope.map = {center: {latitude: 51.219053, longitude: 4.404418 }, zoom: 14 };
        $scope.options = {scrollwheel: false};
    });



//these is not related 
var appControllers = angular.module('appControllers', []);

appControllers.controller('listController', ['$scope', '$http', function($scope, $http) {
	$http.get('js/data.json').success(function(data){		
		$scope.author = data;		
		$scope.Order = "name";		 
    });		  
}]);