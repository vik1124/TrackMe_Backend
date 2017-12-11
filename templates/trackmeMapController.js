//var myApp = angular.module('myApp', []);
var app = angular.module('trackme',[]);

app.directive('datepicker', function() {
    return {
        restrict: 'A',
        require : 'ngModel',
        link : function (scope, element, attrs, ngModelCtrl) {
            $(function(){
                element.datepicker({
                    dateFormat:'yy-mm-dd',
                    onSelect:function (date) {
                        ngModelCtrl.$setViewValue(date);
                        scope.$apply();
                    }
                });
            });
        }
    }
});

app.controller('trackmeController', function($scope, $window, $http) {
	$scope.loginShow = true;
	$scope.signupShow = false;
	$scope.coordsShow = false;
    $scope.names = "";
    $scope.shValErr = false;
    $scope.ackornot = "";
	$scope.loginID = "";
	$scope.uPwd = "";
	//$scope.url = "vik1124.pythonanywhere.com";
	$scope.url = "www.vikwiz.org";
	var todate = new Date();
	$scope.endate = String(todate.getFullYear()) + "-" + ("0"+String(todate.getMonth() + 1)).slice(-2) + "-" + ("0"+String(todate.getDate())).slice(-2);
	$scope.stdate = String(todate.getFullYear() - 2) + "-" + ("0"+String(todate.getMonth() + 1)).slice(-2) + "-" + ("0"+String(todate.getDate())).slice(-2);
    $scope.authLogon = function () {
        $http.get("http://"+$scope.url+"/API/Login?loginid=" + $scope.loginID + "&pwd=" + $scope.uPwd + "")
      .success(function (response) { $scope.ackornot = response;
			//$window.alert($scope.ackornot.result);
			if ($scope.ackornot.result == "ACK") {
				$http.get("http://"+$scope.url+"/API/Trackme?loginid=" + $scope.loginID + "&pwd=" + $scope.uPwd + "")
				.success(function (response) {$scope.names = response;
					//$window.alert($scope.names.coords.length);
				//});
					var mapOptions = {
						zoom: 4,
						center: new google.maps.LatLng(40.0000, -98.0000),
						mapTypeId: google.maps.MapTypeId.TERRAIN
					}

					$scope.map = new google.maps.Map(document.getElementById('map'), mapOptions);
					//$window.alert($scope.map);
					$scope.markers = [];

					var infoWindow = new google.maps.InfoWindow();

					var createMarker = function (info){

						var marker = new google.maps.Marker({
							map: $scope.map,
							position: new google.maps.LatLng(info.lat, info.lon),
							title: String(info.n)
						});

						marker.content = '<div class="infoWindowContent">' + info.tstamp + '</div>';

						google.maps.event.addListener(marker, 'click', function(){
							infoWindow.setContent('<h2>' + marker.title + '</h2>' + marker.content);
							infoWindow.open($scope.map, marker);
						});

						$scope.markers.push(marker);

					}

					//$window.alert($scope.names.coords[0].lat);
					for (i = 0; i < $scope.names.coords.length; i++){
						createMarker($scope.names.coords[i]);
					}

					$scope.openInfoWindow = function(e, selectedMarker){
							e.preventDefault();
							google.maps.event.trigger(selectedMarker, 'click');
						}

					//$window.alert($scope.markers);
				});

				$scope.shValErr = false;
				$scope.ValErr = "";
				$scope.signupShow = false;
				$scope.coordsShow = true;
				$scope.loginShow = false;
			}
			else {
				$scope.shValErr = true;
				$scope.ValErr = "User Not Found!";
				$scope.loginShow = false;
				$scope.signupShow = true;
				$scope.coordsShow = false;
			};
		});
    };
    //$scope.names = $scope.loginID + " " + $scope.uPwd;
    //};

	$scope.gotoLogin = function(){
			$scope.loginShow = true;
			$scope.signupShow = false;
			$scope.coordsShow = false;
	};


    $scope.createUser = function () {
        if ($scope.inpPwd == $scope.pwdre) {
            $http.get("http://"+$scope.url+"/API/Signup?loginid=" + $scope.inpLoginID + "&pwd=" + $scope.inpPwd + "&Uname=" + $scope.Uname + "&phnum=" + $scope.phnum + "&mailID=" + $scope.mailID + "")
  .success(function (response) { $scope.resp = response; });
            if ($scope.resp == "NCK") {
                $scope.shValErr = true;
                $scope.ValErr = "Error in creating user";
            }
            else {
                $scope.shValErr = false;
                $scope.ValErr = "";
                $window.alert("User created successfully");
				$scope.loginID = $scope.inpLoginID;
				$scope.uPwd = $scope.inpPwd;
				$scope.loginShow = true;
				$scope.signupShow = false;
				$scope.coordsShow = false;
            }
        }
        else {
            $scope.shValErr = true;
            $scope.ValErr = "Passwords don't match";
        };
    };


	$scope.getLocation = function () {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition($scope.filterDates, $scope.showError);
            }
            else {
                $scope.error = "Geolocation is not supported by this browser.";
            }
    };
	//$scope.getLocation();


	$scope.filterDates = function(){
			$scope.fromDate = new Date($scope.stdate);
			$scope.toDate = new Date($scope.endate);
			//$window.alert($scope.fromDate);

			$http.get("http://"+$scope.url+"/API/Trackme?loginid=" + $scope.loginID + "&pwd=" + $scope.uPwd + "")
				.success(function (response) {$scope.names = response;
					//$window.alert($scope.names.coords.length);
				//});
					var mapOptions = {
						zoom: 4,
						center: new google.maps.LatLng(40.0000, -98.0000),
						mapTypeId: google.maps.MapTypeId.TERRAIN
					}

					$scope.map = new google.maps.Map(document.getElementById('map'), mapOptions);
					//$window.alert($scope.map);
					$scope.markers = [];

					var infoWindow = new google.maps.InfoWindow();

					var createMarker = function (info){

						var cDate = new Date(info.tstamp.split(" ")[0]);

						if ((cDate >= $scope.fromDate) && (cDate <= $scope.toDate)){
							var marker = new google.maps.Marker({
								map: $scope.map,
								position: new google.maps.LatLng(info.lat, info.lon),
								title: String(info.n)
							});

							marker.content = '<div class="infoWindowContent">' + info.tstamp + '</div>';

							google.maps.event.addListener(marker, 'click', function(){
								infoWindow.setContent('<h2>' + marker.title + '</h2>' + marker.content);
								infoWindow.open($scope.map, marker);
							});

							$scope.markers.push(marker);
						};

					}

					//$window.alert($scope.names.coords[0].lat);
					for (i = 0; i < $scope.names.coords.length; i++){
						createMarker($scope.names.coords[i]);
					}

					$scope.openInfoWindow = function(e, selectedMarker){
							e.preventDefault();
							google.maps.event.trigger(selectedMarker, 'click');
						}

					//$window.alert($scope.markers);
				});
	};

	$scope.gotoSignup = function(){
			$scope.loginShow = false;
			$scope.signupShow = true;
			$scope.coordsShow = false;
			$scope.shValErr = false;
			$scope.ValErr = "";
	};

	$scope.logout = function(){
		$scope.loginID = "";
		$scope.uPwd = "";
		$scope.gotoLogin();
	};



});