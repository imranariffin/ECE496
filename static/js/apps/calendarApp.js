var calendarApp = angular.module('calendarApp', 
  [
    'ngRoute',
  ]);

calendarApp
	.controller('calendarMainController', calendarMainController)
;