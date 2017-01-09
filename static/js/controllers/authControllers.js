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
				$cookies.put('current-user', response.data.user);
				$cookies.putObject('tokens', {
					'Token1': response.data.session_token[0],
					'Token2': response.data.session_token[1],
				});

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
				$cookies.put('current-user', user.username);
				$cookies.putObject('tokens', {
					'Token1': response.data.session_token[0],
					'Token2': response.data.session_token[1],
				});

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

			var req = {
				method: "POST",
				url: "/api/logout",
				headers: $cookies.getObject('tokens'),
				data: {username: $cookies.get('current-user')}
			};

			$http(req)
				// .post('/api/logout/', config)
				.then(function(response) {
					// clear scope and cookies
					$scope.currentUser = null;
					$cookies.remove('current-user');
					$cookies.remove('tokens');

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

function AuthNavbarController($scope, $cookies, $window) {
	$scope.currentUser = $cookies.get('current-user');

	// show my profile
	$scope.toMyProfile = function() {
		$window.location.href = '/#/babysitter/' + 
			$cookies.get('current-user') + '?tab=profile';
	}
}

function DashboardController($scope, $cookies) {
	$scope.currentUser = $cookies.currentUser;
}