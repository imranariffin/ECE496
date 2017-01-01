/*
	controllers for authApp. These controllers will use auth api
	provided by backend and handle session using cookies and global scope.

	Make sure this file is loaded after authApp.js
*/


authApp
	.controller('LoginController', 
		function($scope, $http, $cookies, $window) {
			// init scope vars
			$scope.errorMessage = null;

			/* 
				expect views to provide username and 
				password over within credentials
			*/
			$scope.login = function (credentials) {
				var username = credentials.username;
				var password = credentials.password;
				var data = {username: username, password: password};

				// make post request to backend
				$http
					.post('/api/login', data)
					.then(function(response) {
						// session is saved on backend

						// save sessionToken and user on cookies
						var currentUser = response.data.user;
						var sessionToken1 = response.data.session_token[0];
						var sessionToken2 = response.data.session_token[1];

						$cookies.putObject('current-user', currentUser);
						$cookies.put('session-token-1', sessionToken1);
						$cookies.put('session-token-2', sessionToken2);

						// redirect to map page
						$window.location.href = '/';
					})
					.catch(function(errorResponse) {
						$scope.errorMessage = errorResponse;
					});
		}
	})
	.controller('SignupController', 
		function($scope, $http) {

	})
	.controller('LogoutController', 
		function($scope, $http, $cookies, $window) {
			// init vars
			$scope.errorMessage = null;

			/*
				assume user is already logged in.
			*/
			$scope.logout = function() {
				try {
					var username = $scope.currentUser;
					var data = {username: username};

				  var sessionToken1 = $cookies.get('session-token-1');
				  var sessionToken2 = $cookies.get('session-token-2');

					$http
						.post('/api/logout/' + sessionToken1 + '/' + sessionToken2 , data)
						.then(function(response) {
							// clear scope and cookies
							$scope.currentUser = null;
							$cookies.remove('current-user');
							$cookies.remove('session-token-1');
							$cookies.remove('session-token-2');

							// redirect to main page
							$window.location.href = '/';
						})
						.catch(function(errorResponse) {
							$scope.errorMessage = errorResponse;
						});
				}
				catch (err) {
					throw err;
				}
			}
	})

	// controller for navbar auth buttons
	.controller('AuthNavbarController',
		function($scope, $cookies) {
			$scope.currentUser = $cookies.getObject('current-user');
	})

	// dashboard is used just for testing auth
	.controller('DashboardController',
		function($scope, $cookies) {
			$scope.currentUser = $cookies.currentUser;
	});