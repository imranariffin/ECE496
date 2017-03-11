/*
  profile controllers shouuld all be defined here
*/

function ProfileRatingAndReviewController($scope, $http, $cookies, $routeParams) {
  $scope.errorMessage = null;
  $scope.reviews = null;
  $scope.ratings = null;
  $scope.title = "";
  $scope.rating = 0;
  $scope.review = "";

  var ratingApiUrl = '/api/babysitter/' + 
    $routeParams.sitter_username + '/rating';

  var reviewApiUrl = '/api/babysitter/' + 
    $routeParams.sitter_username + '/review';

  /*
    get average rating
  */
  var reqRating = {
    method: "GET",
    url: ratingApiUrl,
    headers: $cookies.getObject('tokens')
  };

  $http(reqRating)
    // .get(ratingApiUrl)
    .then(function(response) {
      $scope.ratingAvg = response.data.rating;
    })
    .catch(function(errorResponse) {
      console.log(errorResponse);
    });

  /*
    get reviews from backend
  */
  var reqReview = {
    method: "GET",
    url: reviewApiUrl,
    headers: $cookies.getObject('tokens')
  };

  $http(reqReview)
    // .get(reviewApiUrl)
    .then(function(response) {
      $scope.reviews = response.data;
    })
    .catch(function(errorResponse) {
      console.log(errorResponse);
    });
}

function ProfileSubmitRatingAndReviewController($scope, $http, $cookies, $routeParams) {

  $scope.ratingSuccess = false;
  $scope.reviewSuccess = false;
  $scope.ratingReviewError = false;
  $scope.errorMessage = null;

  var reviewApiUrl = '/api/babysitter/' + 
    $routeParams.sitter_username + '/review';

  var ratingApiUrl = '/api/babysitter/' + 
    $routeParams.sitter_username + '/rating';

  /*
    POST rating and review
  */
  $scope.postRateAndReview = function() {

    var reqRating = {
      method: "POST",
      url: ratingApiUrl,
      headers: $cookies.getObject('tokens'),
      data: {
        rating: $scope.rating,
        username: $cookies.get('current-user')
      }
    };

    var reqReview = {
      method: "POST",
      url: reviewApiUrl,
      headers: $cookies.getObject('tokens'),
      data: {
        title: $scope.title,
        review: $scope.review,
        username: $cookies.get('current-user')
      }
    };

    $http(reqRating)
      .then(function(response) {
        $scope.ratingSuccess = true;
        console.log(response);
        console.log($scope.ratingReviewSuccess);
      })
      .catch(function(errorResponse) {
        $scope.ratingReviewError = true;
        $scope.ratingSuccess = false;
        $scope.errorMessage = errorResponse.data.err;
        console.log(errorResponse);
      });

    $http(reqReview)
      .then(function(response) {
        console.log(response);
        $scope.reviewSuccess = true;
        console.log($scope.ratingReviewSuccess);
      })
      .catch(function(errorResponse) {
        $scope.ratingReviewError = true;
        $scope.reviewSuccess = false;
        $scope.errorMessage = errorResponse.data.err;
        console.log(errorResponse);
      });
  }
}

function ProfilePageController($scope, $cookies, $routeParams, $http) {
  $scope.changeTab = function (tab) {
    $scope.tab = tab;
  }

  if ($routeParams.tab)
    $scope.changeTab($routeParams.tab);
  else
    $scope.changeTab('service');

  // get sitter info
  var sitterApiUrl = '/api/babysitter/' + 
    $routeParams.sitter_username + '/profile';

  var reqSitter = {
    method: "GET",
    url: sitterApiUrl,
    headers: $cookies.getObject('tokens')
  };

  $http(reqSitter)
    .then(function(response) {
      $scope.sitter = response.data;
      $scope.tab = 'home';
    })
    .catch(function(errorResponse) {
      $scope.errorMessage = errorResponse;
      console.log(errorResponse);
    });
}

function ProfileServiceController($scope, $http, $cookies, $routeParams) {
  $scope.sitterProfile = null;
  $scope.errorMessage = null;

  var profileApiUrl = '/api/babysitter/' + 
    $routeParams.sitter_username + '/profile';

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

function ProfileProfileController($scope) {;}
function ProfileSettingsController($scope, $routeParams) {
  $scope.sitter_username = $routeParams.sitter_username;
}