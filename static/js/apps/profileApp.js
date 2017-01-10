var profileApp = angular.module('profileApp', 
  [
    'ngRoute',
  ]);

profileApp
  .controller('ProfilePageController', ProfilePageController)
  .controller('ProfileRatingAndReviewController', ProfileRatingAndReviewController)
  .controller('ProfileSubmitRatingAndReviewController', ProfileSubmitRatingAndReviewController)
  .controller('ProfileServiceController', ProfileServiceController)
  .controller('ProfileProfileController', ProfileProfileController)
  .controller('ProfileSettingsController', ProfileSettingsController)
;

// directives
profileApp
	.directive('profileHome', function() {
		return {
			templateUrl: 'static/partials/profile/profile_home.html',
		};
	})
	.directive('profileProfile', function() {
		return {
			templateUrl: 'static/partials/profile/profile_profile.html',
		};
	})
	.directive('profileReviews', function() {
		return {
			templateUrl: 'static/partials/profile/profile_reviews.html',
		};
	})
	.directive('profileSettings', function() {
		return {
			templateUrl: 'static/partials/profile/profile_settings.html',
		};
	})
;