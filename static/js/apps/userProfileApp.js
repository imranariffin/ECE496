var userProfileApp = angular.module('userProfileApp', 
  [
    'ngRoute',
  ]);

// controllers
userProfileApp
  .controller('UserProfileEditController', UserProfileEditController)
  .controller('UserProfileTabController', UserProfileTabController)
;

// directives
userProfileApp
	.directive('userProfileEdit', function() {
		return {
			templateUrl: 'static/partials/user_profile/edit.html',
		};
	})
;