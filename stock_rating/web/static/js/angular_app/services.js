'use strict';

/* Services */

// Demonstrate how to register services
// In this case it is a simple value service.
var estoppeleasy_serv = angular.module('stock.services', ['ngResource']);

estoppeleasy_serv.value('version', '0.1');

estoppeleasy_serv.factory('share', function()
{
    return {
        messages : {
            show : false,
            type : '',
            message : ''
        },
        loader : {
            show : false
        }
    };
});