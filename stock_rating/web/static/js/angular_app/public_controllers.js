
function validateEmail(email) { 
    var re = /\S+@\S+\.\S+/;
    return re.test(email);
}
function add_to_compare_list($scope, $http, start_rating) {
    $http({
        method: 'post',
        data: $.param(params),
        url: '/add_to_compare_list/',
        headers : {
            'Content-Type' : 'application/x-www-form-urlencoded'
        }
    }).success(function(data){
        hide_loader();
        if (data.result == 'ok') {  
            start_rating.company_in_compare_list = 'true';
            $scope.compare_list_count = parseInt($scope.compare_list_count) + 1;
        } else if (data.result == 'error_stock_exceed'){
            $scope.error_message = data.error_message;
        }
    }).error(function(data, status){
        console.log('Request failed');
    });
}
function LoginRegistrationController($scope, $element, $http, $timeout, $location)
{
    $scope.init = function(csrf_token, recaptcha_private_key){
        $scope.csrf_token = csrf_token;
        $scope.edit_flag = false;
        $scope.username = '';
        $scope.password = '';
        $scope.recaptcha_private_key = recaptcha_private_key;
        $scope.new_user = {
            'username': '',
            'password': '',
            'confirm_password': '',
            'fullname': '',
            'terms': false,
        }
    }
    $scope.reset_user = function(){
        $scope.msg = '';
        $scope.new_user = {
            'username': '',
            'password': '',
            'confirm_password': '',
            'fullname': '',
            'terms': false,
        }
    }

    $scope.validate_user = function(){
        $scope.msg = '';
        if($scope.new_user.fullname == ''){
            $scope.msg = "Please enter Your Name";
            return false;
        } else if($scope.new_user.username == '') {
            $scope.msg = "Please enter Username";
            return false;
        } else if(!validateEmail($scope.new_user.username)) {
            $scope.msg = "Please Enter a valid Email";
            return false;
        } else if($scope.new_user.password == '' && !$scope.edit_flag ) {
            $scope.msg = "Please enter Password";
            return false;
        } else if($scope.new_user.password != $scope.new_user.confirm_password && !$scope.edit_flag) {
            $scope.msg = "Password mismatch";
            return false;
        } else if(!$scope.new_user.terms) {
            $scope.msg = "Please Agree Terms and Conditions";
        }else {
            return true;
        }
    }
    $scope.validate_login = function(){        
        $scope.login_msg = '';
        if($scope.username == '') {
            $scope.login_msg = "Please enter Username";
        } else if($scope.password == '') {
            $scope.login_msg = "Please enter Password";
        } else if(Recaptcha.get_response() == '') {
            $scope.login_msg = "Please enter the text in Image"
        } else {
            $.ajax({
                url: '//freegeoip.net/json/',
                type: 'POST',
                dataType: 'jsonp',
                success: function(location) {
                    $scope.ip = location.ip;
                    params = {
                        privatekey: $scope.recaptcha_private_key,
                        remoteip: $scope.ip,
                        challenge: Recaptcha.get_challenge(),
                        response: Recaptcha.get_response(),
                        csrfmiddlewaretoken: $scope.csrf_token
                    }
                    $http({
                        method : 'post',
                        url : "/verify_recaptcha/",
                        data : $.param(params),
                        headers : {
                            'Content-Type' : 'application/x-www-form-urlencoded'
                        }
                    }).success(function(data, status) {   
                        if(data=="false"){
                            $scope.login_msg = "Text Entered is not correct";
                            Recaptcha.reload();
                        } else {
                            $scope.login();
                        }
                    }).error(function(data, status){
                        console.log(data);
                    });
                }
            });
        }
        
    }

    $scope.save_new_user = function(){
        $scope.msg = '';
        if($scope.validate_user()){
            $scope.new_user.terms = String($scope.new_user.terms);
            params = { 
                'user_details': angular.toJson($scope.new_user),
                "csrfmiddlewaretoken" : $scope.csrf_token,
            }
            $http({
                method : 'post',
                url : "/signup/",
                data : $.param(params),
                headers : {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data, status) {   
             if(data.result == 'ok'){
                $scope.msg = "";
                $scope.reset_user();
                $scope.edit_flag = false;
                document.location.href = "/"
             }         
             else
                $scope.msg = "Username already exists";
                
            }).error(function(data, status){
                $scope.message = data.message;
            });
        }        
    }
    $scope.login = function(){
        params = { 
            'username': $scope.username,
            'password': $scope.password,
            "csrfmiddlewaretoken" : $scope.csrf_token,
        }
        $http({
            method : 'post',
            url : "/login/",
            data : $.param(params),
            headers : {
                'Content-Type' : 'application/x-www-form-urlencoded'
            }
        }).success(function(data, status) {   
         if(data.result == 'Ok'){
            $scope.msg = "";
            document.location.href = "/";
         } else
            $scope.login_msg = "Username or Password is incorrect";
            
        }).error(function(data, status){
            $scope.message = data.message;
        });
    }
    $scope.delete_user = function(user){
        show_loader();
        var url = '/progno/delete_user/?id='+user.id;
        $http.get(url).success(function(data){
        if(data.result == 'ok'){
            hide_loader();
            $scope.msg = "User deleted";
        }
        else {
            hide_loader();
            $scope.msg = "Error";
        }
        $scope.get_users();                    
        })
    }
    $scope.get_users = function(){
        var url = '/progno/users/';
        show_loader();
        $http.get(url).success(function(data) {
            $scope.users = data.users;
            paginate($scope.users, $scope);
            hide_loader();
        })
    }
}
function StarRatingController($scope, $http){
    $scope.init = function(csrf_token, star_count) {
        $scope.csrf_token = csrf_token;
        $scope.count = star_count;
        if (star_count)
            $scope.get_company_star_rating(star_count);
    }
    $scope.get_company_star_rating = function(star_count) {
        show_loader()
        $http.get('/star_rating/?star_count='+star_count).success(function(data){
            hide_loader()
            $scope.star_ratings = data.star_ratings;
            $scope.watch_list_count = data.watch_list_count;
            $scope.compare_list_count = data.compare_list_count;
            console.log(data.watch_list_count, data.compare_list_count);
        }).error(function(data, status){
            console.log(data);
        });
    }
    $scope.view_rating_report = function(star_rating){
        document.location.href = '/star_rating_report/?isin_code='+star_rating.isin_code;
    }
    $scope.add_to_compare_list = function(start_rating) {
        params = {
            'isin_code': start_rating.isin_code,
            'csrfmiddlewaretoken': $scope.csrf_token,
        }
        show_loader();
        add_to_compare_list($scope, $http, start_rating);
    }
}

function StarRatingReportController($scope, $http) {
    $scope.init = function(csrf_token, isin_code) {
        $scope.csrf_token = csrf_token;
        if (isin_code)
            $scope.get_company_star_rating_report(isin_code);
    }
    $scope.get_company_star_rating_report = function(isin_code) {
        show_loader()
        $http.get('/star_rating_report/?isin_code='+isin_code).success(function(data){
            hide_loader()
            $scope.star_ratings = data.star_ratings;
            $scope.watch_list_count = data.watch_list_count;
            $scope.compare_list_count = data.compare_list_count;
            $scope.analytical_heads = data.star_ratings[0].analytical_heads;
            console.log(data.analytical_heads);
        }).error(function(data, status){
            console.log(data);
        });
    }
    $scope.add_to_watch_list = function(start_rating) {
        params = {
            'isin_code': start_rating.isin_code,
            'csrfmiddlewaretoken': $scope.csrf_token,
        }
        show_loader();
        $http({
            method: 'post',
            data: $.param(params),
            url: '/add_to_watch_list/',
            headers : {
                'Content-Type' : 'application/x-www-form-urlencoded'
            }
        }).success(function(data){
            hide_loader();
            if (data.result == 'ok'){
                start_rating.company_in_watch_list = 'true';
                $scope.watch_list_count = parseInt($scope.watch_list_count) + 1;             
            } else if (data.result == 'error_stock_exceed'){
                $scope.error_message = data.error_message;
            }
            
        }).error(function(data, status){
            console.log('Request failed');
        })
    }
    $scope.add_to_compare_list = function(start_rating) {
        params = {
            'isin_code': start_rating.isin_code,
            'csrfmiddlewaretoken': $scope.csrf_token,
        }
        show_loader();
        add_to_compare_list($scope, $http, start_rating);
    }
}

