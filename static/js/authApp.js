
var authApp = angular.module('authApp', 
	[
		'ngRoute', 
		'ngCookies',
	]);

authApp
  .controller('LoginController', LoginController)
  .controller('SignupController', SignupController)
  .controller('LogoutController', LogoutController)

  // controller for navbar auth buttons
  .controller('AuthNavbarController', AuthNavbarController)

  // dashboard is used just for testing auth
  .controller('DashboardController', DashboardController)
;

// always update global user sesion on refresh, so
// that we won't lose user session. Also to protect
// certain pages from unauthorized users
authApp.run(function($rootScope, $cookies, $location, $http) {

  // list all the restricted pages here
  var restrictedPages = new Set(['/', '/dashboard']);

  $rootScope.$on('$locationChangeStart', function(event, next, current) {
    var currentPath = $location.path();
    // restric access to certain pages
    if (restrictedPages.has(currentPath)) {
      // redirect to login page if not logged in
      // if (!$rootScope.currentUser) {
      if (!$cookies.get('session-token-1' || !$cookies.get('session-token-2'))) {
          $location.path('/login');
      }
    }
  });
});