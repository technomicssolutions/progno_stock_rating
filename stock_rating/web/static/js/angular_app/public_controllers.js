
function validateEmail(email) { 
    var re = /\S+@\S+\.\S+/;
    return re.test(email);
}

function LoginRegistrationController($scope, $element, $http, $timeout, $location)
{
    $scope.init = function(csrf_token){
        $scope.csrf_token = csrf_token;
        $scope.edit_flag = false;
        $scope.username = '';
        $scope.password = '';
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
/*    $scope.edit_user = function(user){
        $scope.edit_flag = true;
        $scope.reset_password_flag = false;
        $scope.new_user.username = user.username;
        $scope.new_user.first_name = user.first_name;
        $scope.new_user.data_upload = user.data_upload;
        $scope.new_user.field_settings = user.field_settings;
        $scope.new_user.score_settings = user.score_settings;
        $scope.new_user.function_settings = user.function_settings;
        $scope.new_user.analytical_heads = user.analytical_heads;
        $scope.new_user.id = user.id;
    }
    $scope.reset_password = function(user){
        $scope.reset_password_flag = true;
        $scope.edit_flag = false;
        $scope.current_user.id = user.id;
        $scope.current_user.password = '';
        $scope.current_user.confirm_password = '';
    }
    $scope.save_password = function(){
        if($scope.validate_password()){
           params = { 
                'id': $scope.current_user.id,
                'password': $scope.current_user.password,
                "csrfmiddlewaretoken" : $scope.csrf_token,
            }
            $http({
                method : 'post',
                url : "/progno/reset_password/",
                data : $.param(params),
                headers : {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data, status) {            
                $scope.reset_password_flag = false;
            }).error(function(data, status){
                $scope.message = data.message;
            }); 
        }
    }
    $scope.validate_password = function(){
        $scope.msg = '';
        if($scope.current_user.password == '') {
            $scope.msg = "Please enter Password";
            return false;
        } else if($scope.current_user.password != $scope.current_user.confirm_password) {
            $scope.msg = "Password mismatch";
            return false;
        } else {
            return true;
        }
    }*/
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
            return false;
        } else if($scope.password == '') {
            $scope.login_msg = "Please enter Password";
            return false;
        } else {
            return true;
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
        if($scope.validate_login()){
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
             }         
             else
                $scope.login_msg = "Username or Password is incorrect";
                
            }).error(function(data, status){
                $scope.message = data.message;
            });
        }        
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
        $http.get('/star_rating/?star_count='+star_count).success(function(data){
            $scope.star_ratings = data.star_ratings;
        }).error(function(data, status){
            console.log(data);
        });
    }
}