//Angular App Module and Controller

var mainApp = angular.module('mainApp', 
  [
    'ngRoute',
    'authApp',
  ]);

mainApp
  .controller('MapController', MapController)
;