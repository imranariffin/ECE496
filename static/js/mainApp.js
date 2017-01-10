//Angular App Module and Controller

var mainApp = angular.module('mainApp', 
  [
    'ngRoute',
    'ui.bootstrap',
    'authApp',
    'profileApp',
    'paymentApp',
    'calendarApp',
  ]);

mainApp
  .controller('MapController', MapController)
;

mainApp
	.directive('navBar', function() {
		return {
			templateUrl: 'static/partials/__navbar__.html',
		};
	})
;