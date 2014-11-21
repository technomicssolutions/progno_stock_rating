'use strict';

var app = angular.module('stock', ['stock.services', 'stock.directives', 'ngDraggable', 'ngRoute', 'infinite-scroll']);

app.config(function($interpolateProvider)
{
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
})
app.config(['$routeProvider', '$locationProvider', function($routes, $location) {
	
}]);

app.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.headers.common["X-Requested-With"] = 'XMLHttpRequest';
}]);