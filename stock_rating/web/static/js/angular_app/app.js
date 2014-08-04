'use strict';

var app = angular.module('stock', ['stock.services', 'stock.directives', 'ngDraggable']);

app.config(function($interpolateProvider)
{
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
})
app.config(['$routeProvider', '$locationProvider', function($routes, $location) {
	
}]);
