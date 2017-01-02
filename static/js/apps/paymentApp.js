var paymentApp = angular.module('paymentApp', 
  [
    'ngRoute',
  ]);

paymentApp
	.controller('paymentMainController', paymentMainController)
;