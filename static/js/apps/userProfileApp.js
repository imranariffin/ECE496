var userProfileApp = angular.module('userProfileApp', 
  [
    'ngRoute',
  ]);

// controllers
userProfileApp
  .controller('UserProfileEditController', UserProfileEditController)
  .controller('ParentProfileEditController', ParentProfileEditController)
  .controller('UserProfileTabController', UserProfileTabController)
  .controller('UserProfilePasswordController', UserProfilePasswordController)
  .controller('UserController', UserController)
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

userProfileApp
	.directive('fileModel', ['$parse', function ($parse) {
    return {
      restrict: 'A',
      link: function(scope, element, attrs) {
        var model = $parse(attrs.fileModel);
        var modelSetter = model.assign;
        
        element.bind('change', function(){
          scope.$apply(function(){
             modelSetter(scope, element[0].files[0]);
          });
        });
      }
    };
}])
;