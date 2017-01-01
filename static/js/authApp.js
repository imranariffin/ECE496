
var authApp = angular.module('authApp', 
	[
		'ngRoute', 
		'ngCookies',
	]);

// always update global user sesion on refresh, so
// that we won't lose user session. Also to protect
// certain pages from unauthorized users
authApp.run(function($rootScope, $cookies, $location, $http) {
  // $rootScope.currentUser = $cookies.get('current-user');
  // var currentUser = $cookies.get('current-user');

  // if ($rootScope.currentUser) {
  //   $http.defaults.headers.commmon['Authorization'] = 'Basic ' + $rootScope.globals.currentUser.authdata; // jshint ignore:line
  // }

  // list all the restricted pages here
  var restrictedPages = new Set(['/', '/dashboard']);

  $rootScope.$on('$locationChangeStart', function(event, next, current) {
    var currentPath = $location.path();
    // restric access to certain pages
    if (restrictedPages.has(currentPath)) {
      // redirect to login page if not logged in
      // if (!$rootScope.currentUser) {
      if (!$cookies.get('session-token')) {
          $location.path('/login');
      }
    }
  });
});