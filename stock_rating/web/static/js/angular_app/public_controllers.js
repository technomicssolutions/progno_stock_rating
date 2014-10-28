
function validateEmail(email) { 
    var re = /\S+@\S+\.\S+/;
    return re.test(email);
}
function add_to_compare_list($scope, $http, star_rating) {
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
            star_rating.company_in_compare_list = 'true';
            $scope.compare_list_count = parseInt($scope.compare_list_count) + 1;
        } else if (data.result == 'error_stock_exceed'){
            $scope.error_message = data.error_message;
        }
    }).error(function(data, status){
        console.log('Request failed');
    });
}
function add_to_watch_list($scope, $http, star_rating){
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
            star_rating.company_in_watch_list = 'true';
            $scope.watch_list_count = parseInt($scope.watch_list_count) + 1;             
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
        var url = '/progno/delete_user/?id='+user.id+'&ajax=true';
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
        var url = '/progno/users/?ajax=true';
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
        $scope.pages = 0;
        $scope.visible_list = [];
        $scope.error = false;
        if (star_count)
            $scope.get_company_star_rating(star_count);
    }
    $scope.range = function(n) {
        var n = Math.abs(n);
        return new Array(n);
    }
    $scope.get_company_star_rating = function(star_count) {
        show_loader()
        $http.get('/star_rating/?star_count='+star_count+'&ajax=true').success(function(data){
            hide_loader()
            $scope.star_ratings = data.star_ratings;
            if(data.star_ratings.length == 0){
                $scope.error = true;
            }
            paginate($scope.star_ratings, $scope, 5);
            $scope.watch_list_count = data.watch_list_count;
            $scope.compare_list_count = data.compare_list_count;
        }).error(function(data, status){
            console.log(data);
        });
    }
    $scope.view_rating_report = function(star_rating){
        document.location.href = '/star_rating_report/?isin_code='+star_rating.isin_code;
    }
    $scope.add_to_compare_list = function(star_rating) {
        params = {
            'isin_code': star_rating.isin_code,
            'csrfmiddlewaretoken': $scope.csrf_token,
        }
        show_loader();
        add_to_compare_list($scope, $http, star_rating);
    }
    $scope.select_page = function(page){
        select_page(page, $scope.star_ratings, $scope);
    }
    $scope.select_next_page = function(){
        var page = $scope.current_page + 1;
        if(page != $scope.pages + 1)
            select_page(page, $scope.star_ratings, $scope);
    }
    $scope.select_previous_page = function(){
        var page = $scope.current_page - 1
        if(page != 0)
            select_page(page, $scope.star_ratings, $scope);
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
        $http.get('/star_rating_report/?isin_code='+isin_code+'&ajax=true').success(function(data){
            hide_loader()
            $scope.star_ratings = data.star_ratings;
            $scope.watch_list_count = data.watch_list_count;
            $scope.compare_list_count = data.compare_list_count;
            $scope.analytical_heads = data.star_ratings[0].analytical_heads;
            $scope.analytical_heads_list = [];
            var list = []
            for(i=0;i<$scope.analytical_heads.length;i++){                
                list.push($scope.analytical_heads[i])
                if((i+1)%3 == 0 || (i+1) == $scope.analytical_heads.length) {
                    $scope.analytical_heads_list.push(list);
                    list = [];
                }
            }console.log($scope.analytical_heads_list);
        }).error(function(data, status){
            console.log(data);
        });
    }
    $scope.add_to_watch_list = function(star_rating) {
        params = {
            'isin_code': star_rating.isin_code,
            'csrfmiddlewaretoken': $scope.csrf_token,
        }
        show_loader();
        add_to_watch_list($scope, $http, star_rating);
    }
    $scope.add_to_compare_list = function(star_rating) {
        params = {
            'isin_code': star_rating.isin_code,
            'csrfmiddlewaretoken': $scope.csrf_token,
        }
        show_loader();
        add_to_compare_list($scope, $http, star_rating);
    }
    $scope.view_report = function(star_rating){
        document.location.href = '/star_rating_report/?isin_code='+star_rating.isin_code;
    }
}
function ViewWatchListController($scope, $http){
    $scope.init = function(csrf_token) {
        $scope.csrf_token = csrf_token;
        $scope.get_watch_list_details();
    }
    $scope.range = function(n) {
        var n = Math.abs(n);
        return new Array(n);
    }
    $scope.get_watch_list_details = function(){
        $http.get('/watch_list/?ajax=true').success(function(data){
            $scope.watch_list = data.watch_list;
            $scope.watch_list_count = data.watch_list_count;
            $scope.compare_list_count = data.compare_list_count;
        }).error(function(data, status){
            console.log('Request failed')
        });
    }
    $scope.add_to_compare = function(star_rating){
        params = {
            'isin_code': star_rating.isin_code,
            'csrfmiddlewaretoken': $scope.csrf_token,
        }
        show_loader();
        add_to_compare_list($scope, $http, star_rating);
    }
    $scope.view_report = function(star_rating) {
        document.location.href = '/star_rating_report/?isin_code='+star_rating.isin_code;
    }
}
function ViewCompareListController($scope, $http) {
    $scope.init = function(csrf_token) {
        $scope.csrf_token = csrf_token;
        $scope.current_stock = '';
        $scope.add_stock_flag = false;
        $scope.change_stock_flag = false;
        $scope.get_compare_list_details()
    }
    $scope.get_compare_list_details = function(){
        $http.get('/compare_list/').success(function(data){
            $scope.compare_list = data.compare_list;
            $scope.analytical_heads = data.analytical_heads;
        }).error(function(data, status){
            console.log('Request failed')
        });
    }
    $scope.range = function(n) {
        var n = Math.abs(n);
        return new Array(n);
    }
    $scope.show_stock_search_popup = function(){
        $('#stock_search_overlay').css('display', 'block');
        $('.popup').css('display', 'block');
    }
    $scope.hide_stock_search_popup = function(){
        $('#stock_search_overlay').css('display', 'none');
        $('.popup').css('display', 'none');
    }
    $scope.add_stock = function(){
        $scope.show_stock_search_popup();
        $scope.add_stock_flag = true;
        $scope.change_stock_flag = false;
    }
    $scope.change_stock = function(company){
        $scope.show_stock_search_popup();
        $scope.current_stock = company;
        $scope.add_stock_flag = false;
        $scope.change_stock_flag = true;
    }
    $scope.add_to_compare_list = function(company) {
        $scope.hide_stock_search_popup();
        params = {
            'isin_code': company.isin_code,
            'csrfmiddlewaretoken': $scope.csrf_token,
        }
        show_loader();
        add_to_compare_list($scope, $http, company);
        document.location.href = '/compare_list/';

    }
    $scope.change_compare_list = function(company) {
        $scope.hide_stock_search_popup();
        params = {
            'new_stock_isin_code': company.isin_code,
            'current_stock_isin_code': $scope.current_stock.isin_code,
            'csrfmiddlewaretoken': $scope.csrf_token,
        }
        show_loader();
        $http({
            method: 'post',
            data: $.param(params),
            url: '/change_compare_list/',
            headers : {
                'Content-Type' : 'application/x-www-form-urlencoded'
            }
        }).success(function(data){
            hide_loader();
            if (data.result == 'ok') {  
                document.location.href = '/compare_list/';
            }
        }).error(function(data, status){
            console.log('Request failed');
        });
    }
}

function SearchViewController($scope, $http) {
    $scope.init = function(csrf_token) {
        $scope.csrf_token = csrf_token;
    }
    $scope.search_companies = function() {
        if($scope.company_name.length >= 3){
            var url = '/search_company/?search_key='+$scope.company_name+'&ajax=true';
            show_loader();
            $http.get(url).success(function(data) {
                $scope.companies = data.companies;
                paginate($scope.companies, $scope);
                hide_loader();
            })
        }  
    }
    $scope.select_company = function(company) {
        console.log('here');
        $scope.companies = [];
        document.location.href ='/search_result/?isin_code='+company.isin_code;
    }
}
function SearchResultController($scope, $http) {
    $scope.init = function(csrf_token, isin_code) {
        $scope.csrf_token = csrf_token;
        $scope.isin_code = isin_code;
        $scope.get_company_details();
    }
    $scope.get_company_details = function() {
        $http.get('/search_result/?isin_code='+$scope.isin_code+'&ajax=true').success(function(data){
            $scope.company_details = data.star_ratings;
        }).error(function(data, status){
            console.log('Request failed');
        });
    }
    $scope.add_to_watch_list = function(company){
        params = {
            'isin_code': company.isin_code,
            'csrfmiddlewaretoken': $scope.csrf_token,
        }
        add_to_watch_list($scope, $http, company);
    }
    $scope.add_to_compare_list = function(company){
        params = {
            'isin_code': company.isin_code,
            'csrfmiddlewaretoken': $scope.csrf_token,
        }
        show_loader();
        add_to_compare_list($scope, $http, company);
    }
    $scope.view_rating_report = function(company) {
        document.location.href = '/star_rating_report/?isin_code='+company.isin_code;
    }
}