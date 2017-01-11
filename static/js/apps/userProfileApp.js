var userProfileApp = angular.module('userProfileApp', 
  [
    'ngRoute',
  ]);

// controllers
userProfileApp
  .controller('UserProfileEditController', UserProfileEditController)
  .controller('UserProfileTabController', UserProfileTabController)
  .controller('UserProfilePasswordController', UserProfilePasswordController)
;

// directives
userProfileApp
	.directive('userProfileEdit', function() {
		return {
			templateUrl: 'static/partials/user_profile/edit.html',
		};
	})
;


userProfileApp
	.directive('resetPassword', function() {
			return {
				templateUrl: 'static/partials/user_profile/reset.html',
			};
	})
;
	