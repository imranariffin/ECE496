/*
	all angular routes should be here
*/

/*
	All routes except for auth routes are handled by GMapsApp
*/
mainApp.config(['$routeProvider',
   function($routeProvider) {
    $routeProvider
     .when('/', {
      templateUrl: '/static/partials/map.html',
      controller: "MapController"
     })
     .when('/babysitter/:sitter_username', {
     	templateUrl: '/static/partials/profile.html',
     	controller: "ProfileController",
     })
     .otherwise({
      redirectTo: '/'
     });
  }]);

/*
	All routes involving auth are handled by authApp
*/
authApp.config(['$routeProvider', 
	function ($routeProvider) {
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