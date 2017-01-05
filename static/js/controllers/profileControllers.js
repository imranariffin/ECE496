/*
  profile controllers shouuld all be defined here
*/

function ProfileRatingAndReviewController($scope, $http, $cookies, $routeParams) {
  $scope.errorMessage = null;
  $scope.reviews = null;
  $scope.ratings = null;
  $scope.subject = "";
  $scope.rating = 0;
  $scope.review = "";

  var reviewApiUrl = '/api/babysitter/' + 
    $routeParams.sitter_username + '/review/' + 
    $cookies.get('session-token-1') + '/' + 
    $cookies.get('session-token-2');

  var ratingApiUrl = '/api/babysitter/' + 
    $routeParams.sitter_username + '/rating/' + 
    $cookies.get('session-token-1') + '/' + 
    $cookies.get('session-token-2');

  /*
    get average rating
  */

  $http
    .get(ratingApiUrl)
    .then(function(response) {
      $scope.ratingAvg = response.data.rating;
      console.log(response);
    })
    .catch(function(errorResponse) {
      console.log(errorResponse);
    });

  /*
    get reviews from backend
  */
  $http
    .get(reviewApiUrl)
    .then(function(response) {
      $scope.reviews = response.data;
      console.log(response);
    })
    .catch(function(errorResponse) {
      $scope.errorMessage = errorResponse;
      console.log(errorResponse);
    });
}

function ProfileSubmitRatingAndReviewController($scope, $http, $cookies, $routeParams) {

  var reviewApiUrl = '/api/babysitter/' + 
    $routeParams.sitter_username + '/review/' + 
    $cookies.get('session-token-1') + '/' + 
    $cookies.get('session-token-2');

  var ratingApiUrl = '/api/babysitter/' + 
    $routeParams.sitter_username + '/rating/' + 
    $cookies.get('session-token-1') + '/' + 
    $cookies.get('session-token-2');

  /*
    POST rating and review
  */
  $scope.postRateAndReview = function() {

    $http
      .post(ratingApiUrl, {
        rating: $scope.rating,
        username: $cookies.get('current-user'),
      })
      .then(function(response) {
        console.log(response);
      })
      .catch(function(errorResponse) {
        $scope.errorMessage = errorResponse;
        console.log(errorResponse);
      });

    $http
      .post(reviewApiUrl, {
        subject: $scope.subject,
        review: $scope.review,
        username: $cookies.get('current-user'),
      })
      .then(function(response) {
        console.log(response);
      })
      .catch(function(errorResponse) {
        $scope.errorMessage = errorResponse;
        console.log(errorResponse);
      });
  }
}

function ProfilePageController($scope, $cookies, $routeParams, $http) {
  $scope.tab = 'home';
  $scope.changeTab = function (tab) {
    $scope.tab = tab;
  }

  // get sitter info
  var sitter_username = $routeParams.sitter_username;
  var sitterApiUrl = '/api/babysitter/' + 
    sitter_username + '/profile/' +
    $cookies.get('session-token-1') + '/' + 
    $cookies.get('session-token-2');
  $http
    .get(sitterApiUrl)
    .then(function(response) {
      $scope.sitter = response.data;
    })
    .catch(function(errorResponse) {
      console.log(errorResponse);
    });
}

function ProfileServiceController($scope, $http, $cookies, $routeParams) {
  $scope.sitterProfile = null;
  $scope.errorMessage = null;

  var profileApiUrl = '/api/babysitter/' + 
    $routeParams.sitter_username + '/profile/' +
    $cookies.get('session-token-1') + '/' + 
    $cookies.get('session-token-2');

  $http
    .get(profileApiUrl)
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

function ProfileProfileController($scope) {;}
function ProfileSettingsController($scope) {;}