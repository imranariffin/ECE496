/*
	controllers for authApp. These controllers will use auth api
	provided by backend and handle session using cookies and global scope.

	Make sure this file is loaded after authApp.js
*/

function LoginController($scope, $http, $cookies, $window) {
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
}

function SignupController($scope, $http, $cookies, $window) {
	$scope.errorMessage = null;

	/*
		POST:
			body:
				username: string
				password: string
				confirmPassword: string
			response:
				token1: string
				token2: string
				username: string
				success_message: string
			after success:
				redirect to main page
			error:
				show err
	*/

	$scope.signup = function (user) {

		console.log(user.host);
		var host = user.host;
		if (host === undefined)
			host = false;

		var data = {
			username: user.username,
			password: user.password,
			confirmPassword: user.confirmPassword,
			host: host
		};

		$http
			.post('/api/signup', data)
			.then(function(response) {
				// session is saved on backend

				// save sessionToken and user on cookies
				var currentUser = user.username;
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
}

function LogoutController($scope, $http, $cookies, $window) {
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
}

function AuthNavbarController($scope, $cookies) {
	$scope.currentUser = $cookies.getObject('current-user');
}

function DashboardController($scope, $cookies) {
			$scope.currentUser = $cookies.currentUser;
}