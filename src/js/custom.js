var cabShare = angular.module('cabShare', ['ngRoute', 'ngMap','ngAutocomplete','mgcrea.ngStrap'])
	.controller('SimpleController', function ($scope, $route, $http, $location) {
	    /*** Date pickers **/
	    var today = new Date();
	    $scope.pickup_date = today;
	    var pickup_time = new Date(today.setHours(today.getHours() + 2));
	    $scope.time = new Date(pickup_time.setMinutes(0));
	    $scope.pickup_datetime = $scope.time;
	    $scope.mobile_no = '';
	    $scope.email_address = '';
	    $scope.address = '';
	    $scope.user = 'Sign In';
	    $scope.login_url = '#';
	    $scope.to_airport = false;
	    $scope.fetched_bookings = true;
	    $scope.booking_history = [];
	    $scope.selected_cancel = [];
	    var bounds = new google.maps.LatLngBounds(
		    new google.maps.LatLng(17.2168886, 78.1599217),
		    new google.maps.LatLng(17.6078088, 78.6561694)
		);
	    $scope.pickup = '';
	    $scope.hyd_options = {
	      country: 'in',
	      types: '(regions, geocode)',
	      bounds: bounds,
	    };    
	    $scope.details = '';
	    $scope.booking_id = -1;
	    $http({
    		method: "POST",
    		url: "/do_signin",
    	}).success(function (data, status) {
    		$scope.login_url = data[0];
    		$scope.user = data[1];
    	});
	    $scope.get_bookings = function() {
	    	$http({
	    		method: "POST",
	    		url: "/my_bookings",
	    	}).success(function (data, status) {
	    		$scope.booking_history = data;
	    		console.log($scope.booking_history)
	    	});
	    };
	    
	    $scope.setMarker = function(geo) {
	    	console.log("setMarker called");
	    	console.log(geo);
	    	if (geo) {
	    		var lat = geo['k'];
	    		var lng = geo['B'];
	    		$scope.positions = [[lat, lng]];
	    		console.log($scope.positions);
	    	}
	    };
	    $scope.take_bookings = function (mob, email, add, to_airport) {
	    	$scope.mobile_no = mob;
	    	$scope.email_address = email;
	    	$scope.address = add;
	    	$scope.to_airport = to_airport;
	    	$scope.booking_id = -1;
	    	$scope.pickup_datetime = new Date($scope.pickup_date.getFullYear(),
	    								      $scope.pickup_date.getMonth(),
	    								      $scope.pickup_date.getDay(),
	    								      $scope.time.getHours(),
	    								      $scope.time.getMinutes());
	    	$location.url('/confirmation');
	    }
	    $scope.submit = function() {
	    	$scope.fetched_bookings = false;
	    	var request = $http({
                method: "POST",
                url: "/confirm_booking",
                params: {
                    pickup: $scope.pickup,
                    pickup_date : $scope.pickup_datetime,
                    mobile_no : $scope.mobile_no,
                    email_address : $scope.email_address,
                    address : $scope.address,
                    to_airport : $scope.to_airport
                }
            }).success(function (data, status){
            	console.log(data);
            	console.log(status);
	    		$scope.booking_id = data;
	    		$scope.fetched_bookings = true;
	    		$location.url('/confirmation')
	    		//$scope.booking_id = -1;
	    		console.log($scope.booking_id);
            });
	    };
	    
	    $scope.cancelSelected = function() {
	    	console.log($scope.selected_cancel);
	    	var request = $http({
                method: "POST",
                url: "/cancel_booking",
                params: {
                	booking_ids : $scope.selected_cancel
                }
            }).success(function (data, status){
            	$scope.get_bookings();
        		//$scope.booking_history = data;            	
            	//console.log(data);
            	//console.log(status);
            	//$location.url('/account');
            });
	    	
    	};

    	$scope.updateSelection = function(id) {
	    	  $scope.selected_cancel.push(id);
    	};

    	$scope.getSelectedClass = function(id) {
	    	  return $scope.isSelected(id) ? 'selected' : '';
    	};

    	$scope.isSelected = function(id) {
	    	  return $scope.selected_cancel.indexOf(id) >= 0;
    	};
});

cabShare.config(function($routeProvider) {
	$routeProvider
		.when('/', 
			{
				controllerAs: 'SimpleController',
				templateUrl: 'partial/map.html',
			})
		.when('/bookings', 
			{
				controllerAs: 'SimpleController',
				templateUrl: 'partial/bookings.html',
			})
		.when('/map', 
			{
				controllerAs: 'SimpleController',
				templateUrl: 'partial/map.html',
			})
		.when('/confirmation', 
			{
				controllerAs: 'SimpleController',
				templateUrl: 'partial/confirmation.html',
			})
		.when('/account', 
			{
				controllerAs: 'SimpleController',
				templateUrl: 'partial/my_account.html',
			})
		.otherwise({ redirectTo: '/'});
});
