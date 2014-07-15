
function validateEmail(email) { 
    var re = /\S+@\S+\.\S+/;
    return re.test(email);
}


function DashboardController($scope, $element, $http, $timeout, $location)
{
    $scope.init = function(user){
        $scope.user_id = user;
        $scope.show_popup = false;
        $scope.hide_dropdown();
    }
    $scope.range = function(n) {
        return new Array(n);
    }
    $scope.getClass = function(page) {
        if(page == $scope.current_page)
            return "current";
        else
            return '';
    }
  
    $scope.show_dropdown = function(){
        $('#dropdown_menu').css('display', 'block');
    }
    $scope.hide_dropdown = function(){
        $('#dropdown_menu').css('display', 'none');
    }
    $scope.paginate = function(){
        $scope.current_ques_page = 1;
        $scope.que_pages = $scope.questionairs.length / $scope.ques_page_interval;
        if($scope.que_pages > parseInt($scope.que_pages))
            $scope.que_pages = parseInt($scope.que_pages) + 1;
        $scope.visible_questionairs = $scope.questionairs.slice(0, $scope.ques_page_interval);
        console.log($scope.que_pages);
    }

    $scope.select_page = function(page) {
        if(ques_page == 0){
            ques_page = $scope.current_ques_page + 1;
        } else if(ques_page == -1){
            ques_page = $scope.current_ques_page - 1;
        }
        var last_ques_page = ques_page - 1;
        var start = (last_ques_page * $scope.ques_page_interval) ;
        var end = $scope.ques_page_interval * ques_page;
        $scope.current_ques_page = ques_page;
        $scope.visible_questionairs = $scope.questionairs.slice(start, end);
    }

    $scope.hide_popup_divs = function(){
        $('#assign_mentee_mentor').css('display', 'none');
        $('#assign_mentee_saq').css('display', 'none');
    }
}

function AdministrationController($scope, $element, $http, $timeout, $location)
{
    $scope.init = function(csrf_token){
        $scope.csrf_token = csrf_token;
        $scope.show_popup = false;
        $scope.hide_dropdown();
        $scope.reset_user();
        $scope.get_users();
        $scope.edit_flag = false;
        $scope.current_user = {};        
    }
    $scope.reset_user = function(){
        $scope.msg = '';
        $scope.new_user = {
            'username': '',
            'password': '',
            'confirm_password': '',
            'first_name': '',
            'data_upload': false,
            'field_settings': false,
            'score_settings': false,
            'function_settings': false,
            'analytical_heads': false,
            'id': ''
        }
    }
    $scope.edit_user = function(user){
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
    }
    $scope.save_password = function(){
        if($scope.current_user.password != '' && $scope.current_user.password == $scope.current_user.confirm_password){
           params = { 
                'id': $scope.current_user.id,
                'password': $scope.current_user.password,
                "csrfmiddlewaretoken" : $scope.csrf_token,
            }
            $http({
                method : 'post',
                url : "/reset_password/",
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
    $scope.validate_user = function(){
        $scope.msg = '';
        if($scope.new_user.username == '') {
            $scope.msg = "Please enter User Id";
            return false;
        } else if($scope.new_user.password == '' && !$scope.edit_flag ) {
            $scope.msg = "Please enter Password";
            return false;
        } else if($scope.new_user.password != $scope.new_user.confirm_password && !$scope.edit_flag) {
            $scope.msg = "Password mismatch";
            return false;
        } else if($scope.new_user.first_name == ''){
            $scope.msg = "Please enter Name";
            return false;
        } else {
            return true;
        }
    }
    $scope.save_new_user = function(){
        if($scope.validate_user()){
            $scope.new_user.data_upload = String($scope.new_user.data_upload)
            $scope.new_user.field_settings = String($scope.new_user.field_settings)
            $scope.new_user.score_settings = String($scope.new_user.score_settings)
            $scope.new_user.function_settings = String($scope.new_user.function_settings)
            $scope.new_user.analytical_heads = String($scope.new_user.analytical_heads)
            params = { 
                'user_details': angular.toJson($scope.new_user),
                "csrfmiddlewaretoken" : $scope.csrf_token,
            }
            $http({
                method : 'post',
                url : "/save_user/",
                data : $.param(params),
                headers : {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data, status) {            
                $scope.get_users();
                $scope.reset_user();
                $scope.edit_flag = false;
            }).error(function(data, status){
                $scope.message = data.message;
            });
        }        
    }
    $scope.get_users = function(){
        var url = '/users/';
        $http.get(url).success(function(data) {
            $scope.users = data.users;
        })
    }
    $scope.range = function(n) {
        return new Array(n);
    }
    $scope.getClass = function(page) {
        if(page == $scope.current_page)
            return "current";
        else
            return '';
    }
    $scope.show_dropdown = function(){
        $('#dropdown_menu').css('display', 'block');
    }
    $scope.hide_dropdown = function(){
        $('#dropdown_menu').css('display', 'none');
    }
    $scope.paginate = function(){
        $scope.current_ques_page = 1;
        $scope.que_pages = $scope.questionairs.length / $scope.ques_page_interval;
        if($scope.que_pages > parseInt($scope.que_pages))
            $scope.que_pages = parseInt($scope.que_pages) + 1;
        $scope.visible_questionairs = $scope.questionairs.slice(0, $scope.ques_page_interval);
    }

    $scope.select_page = function(page) {
        if(ques_page == 0){
            ques_page = $scope.current_ques_page + 1;
        } else if(ques_page == -1){
            ques_page = $scope.current_ques_page - 1;
        }
        var last_ques_page = ques_page - 1;
        var start = (last_ques_page * $scope.ques_page_interval) ;
        var end = $scope.ques_page_interval * ques_page;
        $scope.current_ques_page = ques_page;
        $scope.visible_questionairs = $scope.questionairs.slice(start, end);
    }

    $scope.hide_popup_divs = function(){
        $('#assign_mentee_mentor').css('display', 'none');
        $('#assign_mentee_saq').css('display', 'none');
    }
}

function FieldController($scope, $element, $http, $timeout, $location)
{
    $scope.new_field = {
        'field_name': '',
        'field_description': '',
        'id': '',
    }
    $scope.init = function(csrf_token){
        $scope.csrf_token = csrf_token;
        $scope.get_fields();    
        $scope.hide_dropdown();
    }
    $scope.edit_field = function(field){
        $scope.new_field.field_name = field.name;
        $scope.new_field.field_description = field.description;
        $scope.new_field.id = field.id;
    }
    $scope.get_fields = function(){
        var url = '/fields/';
        $http.get(url).success(function(data) {
            $scope.fields = data.fields;
        })
    }
    $scope.validate_field = function(){
        $scope.msg = '';
        if($scope.new_field.field_name == '') {
            $scope.msg = "Please enter Field Name";
            return false;
        } else if($scope.new_field.field_description == '' ) {
            $scope.msg = "Please enter Field Description";
            return false;
        } else {
            return true;
        }
    }
    $scope.save_new_field = function(){
        if($scope.validate_field()){
           /* $scope.new_user.analytical_heads = String($scope.new_user.analytical_heads)*/
            params = { 
                'field_details': angular.toJson($scope.new_field),
                "csrfmiddlewaretoken" : $scope.csrf_token,
            }
            $http({
                method : 'post',
                url : "/save_field/",
                data : $.param(params),
                headers : {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data, status) {  
                if(data.result == 'error'){
                     $scope.msg = "Field already exists";
                    }
                else
                    {
                        $scope.msg = "";
                     $scope.new_field = {
                     'field_name': '',
                     'field_description': '',
                     'id': '',
                     }   
                    }       
                $scope.get_fields();                    
            }).error(function(data, status){
                $scope.message = data.message;
            });
        }        
    }
    $scope.getClass = function(page) {
        if(page == $scope.current_page)
            return "current";
        else
            return '';
    }
    $scope.show_dropdown = function(){
        $('#dropdown_menu').css('display', 'block');
    }
    $scope.hide_dropdown = function(){
        $('#dropdown_menu').css('display', 'none');
    }
    $scope.paginate = function(){
        $scope.current_ques_page = 1;
        $scope.que_pages = $scope.questionairs.length / $scope.ques_page_interval;
        if($scope.que_pages > parseInt($scope.que_pages))
            $scope.que_pages = parseInt($scope.que_pages) + 1;
        $scope.visible_questionairs = $scope.questionairs.slice(0, $scope.ques_page_interval);
    }
    $scope.select_page = function(page) {
        if(ques_page == 0){
            ques_page = $scope.current_ques_page + 1;
        } else if(ques_page == -1){
            ques_page = $scope.current_ques_page - 1;
        }
        var last_ques_page = ques_page - 1;
        var start = (last_ques_page * $scope.ques_page_interval) ;
        var end = $scope.ques_page_interval * ques_page;
        $scope.current_ques_page = ques_page;
        $scope.visible_questionairs = $scope.questionairs.slice(start, end);
    }
}


function FunctionController($scope, $element, $http, $timeout, $location)
{
    $scope.new_general = {
        'function_name': '',
        'function_description': '',
        'function_formula': '',
        'select_head': '',
    }
   $scope.new_continuity = {
        'function_name': '',
        'function_description': '',
        'no_of_periods': '',
        'minimum_value': '',
        'period_1': '',
        'period_2': '',
        'period_3': '',
        'select_head': '',
    }
   $scope.new_consistency = {
        'function_name': '',
        'function_description': '',
        'no_of_periods': '',
        'mean': '',
        'period_1': '',
        'period_2': '',
        'select_head': '',
    }
    $scope.select_category = ''
    $scope.init = function(csrf_token){
        $scope.csrf_token = csrf_token;
        $scope.hide_dropdown();
        $scope.change_type();
        $scope.get_category();
        $scope.get_anly_head();
        $scope.show_general = true;
        $scope.show_consistency = false;
        $scope.show_continuity = false;    
        $scope.select_type = 1;  
     }
    $scope.change_type = function(type){
        if(type==1)
        {
         $scope.show_general = true;
         $scope.show_continuity = false;
         $scope.show_consistency = false;
        }
       if(type==2)
        {
         $scope.show_general = false;
         $scope.show_continuity = true;
         $scope.show_consistency = false;
        }       
       if(type==3)
        {
         $scope.show_general = false;
         $scope.show_continuity = false;
         $scope.show_consistency = true;
        }       
    }
    $scope.show_dropdown = function(){
        $('#dropdown_menu').css('display', 'block');
    }
    $scope.hide_dropdown = function(){
        $('#dropdown_menu').css('display', 'none');
    }  
    $scope.validate_field_general = function(){
        $scope.msg = '';
        if($scope.new_general.function_name == '') {
            $scope.msg = "Please enter Function Name";
            return false;
        } else if($scope.new_general.function_description == '' ) {
            $scope.msg = "Please enter Function Description";
            return false;
        } else if($scope.new_general.function_formula == '' ) {
            $scope.msg = "Please enter Formula";
            return false;
        } else if($scope.new_general.select_head == '' ) {
            $scope.msg = "Please select analytical head";
            return false;
        } else if($scope.select_category == '' ) {
            $scope.msg = "Please select category";
            return false;
        } else {
            return true;
        }  
    }
    $scope.validate_field_continuity = function(){
        $scope.msg = '';
        if($scope.new_continuity.function_name == '') {
            $scope.msg = "Please enter Function Name";
            return false;
        } else if($scope.new_continuity.function_description == '' ) {
            $scope.msg = "Please enter Function Description";
            return false;
        } else if($scope.new_continuity.no_of_periods == '' ) {
            $scope.msg = "Please enter Number of periods";
            return false;
        } else if($scope.new_continuity.minimum_value == '' ) {
            $scope.msg = "Please enter Minimum Value";
            return false;
        } else if($scope.new_continuity.period_1 == '' ) {
            $scope.msg = "Please enter Period 1";
            return false;
        } else if($scope.new_continuity.period_2 == '' ) {
            $scope.msg = "Please enter Period 2";
            return false;
        } else if($scope.new_continuity.period_3 == '' ) {
            $scope.msg = "Please enter Period 3";
            return false;
        } else if($scope.new_continuity.select_head == '' ) {
            $scope.msg = "Please select analytical head";
            return false;
        } else if($scope.select_category == '' ) {
            $scope.msg = "Please select category";
            return false;
        } else {
            return true;
        }  
    }
    $scope.validate_field_consistency = function(){
        $scope.msg = '';
        if($scope.new_consistency.function_name == '') {
            $scope.msg = "Please enter Function Name";
            return false;
        } else if($scope.new_consistency.function_description == '' ) {
            $scope.msg = "Please enter Function Description";
            return false;
        }else if($scope.new_consistency.no_of_periods == '' ) {
            $scope.msg = "Please enter Number of periods";
            return false;
        }else if($scope.new_consistency.mean == '' ) {
            $scope.msg = "Please enter Mean";
            return false;
        } else if($scope.new_consistency.period_1 == '' ) {
            $scope.msg = "Please enter Period 1";
            return false;
        } else if($scope.new_consistency.period_2 == '' ) {
            $scope.msg = "Please enter Period 2";
            return false;
        } else if($scope.new_consistency.select_head == '' ) {
            $scope.msg = "Please select analytical head";
            return false;
        } else if($scope.select_category == '' ) {
            $scope.msg = "Please select category";
            return false;
        } else {
            return true;
        }  
    }
    $scope.save_new_general = function(){
        if($scope.validate_field_general()){
            params = { 
                'function_details': angular.toJson($scope.new_general),
                'function_type' : angular.toJson($scope.select_type),
                'function_category' : angular.toJson($scope.select_category),
                "csrfmiddlewaretoken" : $scope.csrf_token,
            }
            $http({
                method : 'post',
                url : "/save_function/",
                data : $.param(params),
                headers : {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data, status) {  
                if(data.result == 'error'){
                     $scope.msg = "Function already exists";
                    }
                else
                    {
                     $scope.msg = "";
                     $scope.new_general = {
                     'id': '',
                     'function_name': '',
                     'function_description': '',
                     'function_formula': '',            
                     'select_head': '',
                     }   
                    }       
            }).error(function(data, status){
                $scope.message = data.message;
            });
        }        
    }
    $scope.save_new_continuity = function(){
        if($scope.validate_field_continuity()){
            params = { 
                'function_details': angular.toJson($scope.new_continuity),
                'function_type' : angular.toJson($scope.select_type),
                'function_category' : angular.toJson($scope.select_category),
                "csrfmiddlewaretoken" : $scope.csrf_token,
            }
            $http({
                method : 'post',
                url : "/save_function/",
                data : $.param(params),
                headers : {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data, status) {  
                if(data.result == 'error'){
                     $scope.msg = "Function already exists";
                    }
                else
                    {
                     $scope.msg = "";
                     $scope.new_continuity = {
                     'id': '',
                     'function_name': '',
                     'function_description': '',
                     'no_of_periods': '',
                     'minimum_value': '',
                     'period_1': '',
                     'period_2': '',
                     'period_3': '',
                     'select_head': '',
                     }   
                    }       
            }).error(function(data, status){
                $scope.message = data.message;
            });
        }        
    }
    $scope.save_new_consistency = function(){
        if($scope.validate_field_consistency()){
            params = { 
                'function_details': angular.toJson($scope.new_consistency),
                'function_type' : angular.toJson($scope.select_type),
                'function_category' : angular.toJson($scope.select_category),
                "csrfmiddlewaretoken" : $scope.csrf_token,
            }
            $http({
                method : 'post',
                url : "/save_function/",
                data : $.param(params),
                headers : {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data, status) {  
                if(data.result == 'error'){
                     $scope.msg = "Function already exists";
                    }
                else
                    {
                     $scope.msg = "";
                     $scope.new_consistency = {
                     'id': '',
                     'function_name': '',
                     'function_description': '',
                     'no_of_periods': '',
                     'mean': '',
                     'period_1': '',
                     'period_2': '',
                     'select_head': '',
                     }   
                    }       
            }).error(function(data, status){
                $scope.message = data.message;
            });
        }        
    }
   $scope.get_category = function(){
        var url = '/category/';
        $http.get(url).success(function(data) {
            $scope.item_list = data.item_list;
        })
    }
    $scope.get_anly_head = function(){
        var url = '/anly_head/';
        $http.get(url).success(function(data) {
            $scope.cat_list = data.item_list;
        })
    }

}