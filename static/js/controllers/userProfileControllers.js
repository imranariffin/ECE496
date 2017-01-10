/*
	All controllers within userProfileApp should be defined here
*/

function UserProfileTabController($scope) {
	$scope.tab = 'edit';

  // tabs constants
  $scope.EDIT_TAB = 'edit';
  $scope.TIME_TAB = 'time';
  $scope.PAYMENT_TAB = 'payment';
  $scope.RESET_PASSWORD = 'reset-password';
  $scope.VIEW_PROFILE_TAB = 'view-profile';

  $scope.changeUserTab = function(tab) {
    $scope.tab = tab;
  };
}

function UserProfileEditController($scope, $cookies, $routeParams, $http) {
  $scope.sitterProfile = null;
  $scope.errorMessage = null;

  var profileApiUrl = '/api/babysitter/' + 
    $routeParams.username + '/profile';

  console.log('GET request: ' + profileApiUrl);

  var reqProfile = {
    method: "GET",
    url: profileApiUrl,
    headers: $cookies.getObject('tokens')
  };

  $http(reqProfile)
    .then(function(response) {
      $scope.profile = response.data.profile;

      // for shorter lookup in html
      $scope.general_info = response.data.profile.service.general_info;
      $scope.price = response.data.profile.service.price;
      $scope.extra = response.data.profile.service.extra;
      $scope.personal_info = response.data.profile.basic.personal_info;
      $scope.contact_info = response.data.profile.basic.contact_info;
      $scope.languages = $scope.personal_info.languages.join(", ");
      $scope.policy = response.data.profile.service.policy;

    })
    .catch(function(errorResponse) {
      $scope.errorMessage = errorResponse;
      console.log(errorResponse);
    });

}