/*
	all angular routes for all apps should be here
*/

mainApp.config(['$routeProvider',
   function($routeProvider) {
    $routeProvider
     .when('/', {
      templateUrl: '/static/partials/map.html',
      controller: "MapController"
     })
     .otherwise({
      redirectTo: '/'
     });
  }]);

/*
	All routes involving auth are handled by authApp
*/
authApp.config(['$routeProvider', 
	function($routeProvider) {
		$routeProvider
			.when('/login', {
				templateUrl: '/static/partials/login.html',
				controller: 'LoginController',
			})
			.when('/signup', {
				templateUrl: '/static/partials/signup.html',
				controller: 'SignupController',
			})
			.when('/dashboard', {
				templateUrl: '/static/partials/dashboard.html',
				controller: 'DashboardController',
			});
	}]);

profileApp.config(['$routeProvider',
	function($routeProvider) {
		$routeProvider
     .when('/babysitter/:sitter_username', {
     	templateUrl: '/static/partials/__profile__.html',
     	controller: "ProfilePageController",
     });
}]);