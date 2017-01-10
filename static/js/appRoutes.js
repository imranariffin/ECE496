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
				templateUrl: '/static/partials/auth/__login__.html',
				controller: 'LoginController',
			})
			.when('/signup', {
				templateUrl: '/static/partials/auth/__signup__.html',
				controller: 'SignupController',
			})
			.when('/dashboard', {
				templateUrl: '/static/partials/auth/dashboard.html',
				controller: 'DashboardController',
			});
	}]);

profileApp.config(['$routeProvider',
	function($routeProvider) {
		$routeProvider
     .when('/babysitter/:sitter_username', {
     	templateUrl: '/static/partials/profile/__profile__.html',
     });
}]);

userProfileApp.config(['$routeProvider',
	function($routeProvider) {
		$routeProvider
			.when('/user/:username', {
				templateUrl: '/static/partials/user_profile/main.html',
			})
}]);