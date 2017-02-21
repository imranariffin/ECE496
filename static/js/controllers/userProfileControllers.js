/*
  All controllers within userProfileApp should be defined here
*/

function UserController ($scope, $routeParams, $cookies, $http) {
  $scope.user = null;
  var userApiUrl = "/api/user/" + $routeParams.username;

  $scope.isHost = function() {
    if ($scope.user)
      return $scope.user.host===true;
  }

  var reqProfile = {
    method: "GET",
    url: userApiUrl,
    headers: $cookies.getObject('tokens')
  };

  /* GET profile */
  $http(reqProfile)
    .then(function(response) {
      $scope.user = response.data.user;
      console.log($scope.user);
    })
    .catch(function(errorResponse) {
      console.log(errorResponse);
    });
}

function UserProfileTabController($scope) {
  $scope.tab = 'edit';

  // tabs constants
  $scope.EDIT_TAB = 'edit';
  $scope.TIME_TAB = 'time';
  $scope.PAYMENT_TAB = 'payment';
  $scope.RESET_PASSWORD = 'reset-password';
  $scope.VIEW_PROFILE_TAB = 'view-profile';
  $scope.SEARCH_TAB = 'search';

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

      // // for shorter lookup in html
      var service = response.data.profile.service;
      var general_info = response.data.profile.service.general_info;
      var price = response.data.profile.service.price;
      var extra = response.data.profile.service.extra;
      var personal_info = response.data.profile.basic.personal_info;
      var contact_info = response.data.profile.basic.contact_info;
      var languages = personal_info.languages.join(", ");

      // TEST
      $scope.personal_info = personal_info;

      $scope.policy = service.policy;
      $scope.about = service.about;
      
      $scope.service_location = general_info.service_location;
      $scope.age_range = general_info.age_range;
      $scope.sitter_status = general_info.sitter_status;
      $scope.pickup = general_info.pickup;

      $scope.weekday_hourly = price.weekday_hourly;
      $scope.weekend_hourly = price.weekend_hourly;
      $scope.security_deposit = price.security_deposit;

      $scope.free_parking = extra.free_parking;
      $scope.air_condition = extra.air_condition;
      $scope.meal = extra.meal;
      $scope.child_education = extra.child_education;
      $scope.wireless_internet = extra.wireless_internet;

      $scope.profile_pic = personal_info.profile_pic;
      $scope.cover_pic = personal_info.cover_pic;
      $scope.display_name = personal_info.display_name;
      $scope.city = personal_info.city.city;
      $scope.prov_state = personal_info.city.prov_state;
      $scope.gender = personal_info.gender;
      $scope.experience = personal_info.experience;
      $scope.languages = languages;
      $scope.langArr = personal_info.languages;
      $scope.education = personal_info.education;

      $scope.website = contact_info.website;
      $scope.phone = contact_info.phone;
      $scope.email = contact_info.email;

    })
    .catch(function(errorResponse) {
      $scope.errorMessage = errorResponse;
      console.log(errorResponse);
    });

  /* POST profile */
  $scope.updateProfile = function () {

    var updateProfileApiUrl = '/api/babysitter/' +
      $routeParams.username + '/profile_upload';
    var profilePic = $scope.profilePic;
    var coverPic = $scope.coverPic;
    var fd = new FormData();
    fd.append('profile_pic', profilePic);
    fd.append('cover_pic', coverPic);

    var jsonData = {
      profile: {
        service: {
          policy: $scope.policy,
          about: $scope.about,
          general_info: {
            service_location: $scope.service_location,
            age_range: $scope.age_range,
            sitter_status: $scope.sitter_status,
            pickup: $scope.pickup
          },
          price: {
            weekend_hourly: $scope.weekend_hourly,
            weekday_hourly: $scope.weekday_hourly,
            security_deposit: $scope.security_deposit
          },
          extra: {
            free_parking: $scope.free_parking,
            air_condition: $scope.air_condition,
            meal: $scope.meal,
            child_education: $scope.child_education,
            wireless_internet: $scope.wireless_internet
          }
        },
        basic: {
          personal_info: {
            profile_pic: $scope.profile_pic,
            cover_pic: $scope.cover_pic,
            display_name: $scope.display_name,
            city: {
              city: $scope.city,
              prov_state: $scope.prov_state
            },
            gender: $scope.gender,
            experience: $scope.experience,
            languages: $scope.langArr,
            education: $scope.education
          },
          contact_info: {
            website: $scope.website,
            phone: $scope.phone,
            email: $scope.email
          }
        }
      }
    };

    $http.post(updateProfileApiUrl, fd, {
        transformRequest: angular.identity,
        headers: {
          'Content-Type': undefined,
          'Token1': $cookies.getObject('tokens')['Token1'],
          'Token2': $cookies.getObject('tokens')['Token2'],
          'Json': angular.toJson(jsonData)
        }
    })
    .then(function(response){
      console.log(response);
    })
    .catch(function(errorResponse){
      console.log(errorResponse);
    });
  };
}

function ParentProfileEditController($scope, $routeParams, $cookies, $http) {
  $scope.parentProfilePic = null;
  $scope.errorMessage = null;

  $scope.uploadProfilePic = function () {

    var parentUpdateProfileApiUrl = '/api/parent/' + 
      $routeParams.username + '/profile_upload';
    var fd = new FormData();
    fd.append('profile_pic', $scope.parentProfilePic);

    $http.post(parentUpdateProfileApiUrl, fd, {
        transformRequest: angular.identity,
        headers: {
          'Content-Type': undefined,
          'Token1': $cookies.getObject('tokens')['Token1'],
          'Token2': $cookies.getObject('tokens')['Token2'],
          'Json': angular.toJson({})
        }
    })
    .then(function(response){
      console.log(response);
    })
    .catch(function(errorResponse){
      console.log(errorResponse);
      $scope.errorMessage = errorResponse;
    });
  }
}

function ParentAddressEditController($scope, $routeParams, $cookies, $http) {
  $scope.errorMessage = null;
  console.log("ParentAddressEditController");

  var parentAddressApiUrl = '/api/parent/' + 
    $routeParams.username + '/address';

  var reqGetAddress = {
    method: "GET",
    url: parentAddressApiUrl,
    headers: $cookies.getObject('tokens')
  };
  $http(reqGetAddress)
    .then(function(response) {
      console.log(response);
      $scope.addr = response.data.addr;
      $scope.errorMessage = null;
    })
    .catch(function(errorResponse) {
      $scope.errorMessage = errorResponse;
      $scope.addr = {};
    });

  $scope.updateAddress = function () {

    var reqUpdateAddress = {
      method: "POST",
      url: parentAddressApiUrl,
      headers: $cookies.getObject('tokens'),
      data: {
        addr: $scope.addr
      }
    };

    $http(reqUpdateAddress)
      .then(function(response){
        console.log(response.data.message);
      })
      .catch(function(errorResponse){
        console.log(errorResponse.data.err);
        $scope.errorMessage = errorResponse;
      });
  }
}

function NameSearchController($scope, $cookies, $http) {
  $scope.sitter_name = "";
  $scope.nameSearchRes = null;
  $scope.errorMessage = null;

  $scope.nameSearch = function(sitter_name) {
    console.log(sitter_name);

    var searchApiUrl = '/api/namesearch/' + sitter_name;
    var reqSearch = {
      method: "GET",
      url: searchApiUrl,
      headers: $cookies.getObject('tokens')
    };

    // $scope.nameSearchRes = 
    // [
    //   {
    //     'name': 'Cherry',
    //     'username': 'lichuanr',
    //     'city': 'Toronto'
    //   },
    //   {
    //     'name': 'Imran',
    //     'username': 'imran',
    //     'city': 'Toronto'
    //   },
    //   {
    //     'name': 'Flower',
    //     'username': 'changqi',
    //     'city': 'Toronto'
    //   }
    // ];

    $http(reqSearch)
      .then(function(response) {
        console.log(response);
        $scope.nameSearchRes = response.data;
        $scope.errorMessage = null;
      })
      .catch(function(errorResponse) {
        $scope.nameSearchRes = null;
        if (errorResponse.data && errorResponse.data.err)
          $scope.errorMessage = errorResponse.data.err;
        else
          $scope.errorMessage = errorResponse.data;
      });
  };
}

function FilterSearchController($scope, $routeParams, $cookies, $http) {
  $scope.errorMessage = null;
  $scope.rating = 0;
  $scope.distance = 0;
  $scope.price = 0;
  $scope.ratings = [
    "No selection", 
    1, 
    2, 
    3, 
    4, 
    5
  ];
  $scope.distances = [
    "No selection", 
    "less than 1km", 
    "1 - 5km", 
    "5 - 10km", 
    "10 - 50km",
    "greater than 50km"
  ];
  $scope.prices = [
    "No selection",
    "Under $20",
    "$20 - $30",
    "$30 - $40",
    "greater than $40"
  ];

  $scope.filterSearch = function(rating, distance, price) {

    var searchApiUrl = '/api/' + 
      $routeParams.username + 
      '/SearchByFilter/' +
      rating + '/' + 
      distance + '/' +
      price;
    var reqSearch = {
      method: "GET",
      url: searchApiUrl,
      headers: $cookies.getObject('tokens')
    };

    $http(reqSearch)
      .then(function(response) {
        console.log(response.data);
        $scope.filterSearchRes = response.data;
        $scope.errorMessage = null;
      })
      .catch(function(errorResponse) {
        $scope.errorMessage = errorResponse;
        $scope.filterSearchRes = null;
      });

    // $scope.filterSearchRes =  
    // [
    //   {
    //     'name': 'Cherry',
    //     'username': 'lichuanr',
    //     'city': 'Toronto'
    //   },
    //   {
    //     'name': 'Imran',
    //     'username': 'imran',
    //     'city': 'Toronto'
    //   },
    //   {
    //     'name': 'Flower',
    //     'username': 'changqi',
    //     'city': 'Toronto'
    //   }
    // ];
  };
}