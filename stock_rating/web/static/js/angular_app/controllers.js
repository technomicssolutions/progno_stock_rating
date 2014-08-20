

function paginate(list, $scope, page_interval) {
    if(!page_interval)
        var page_interval = 20;
    $scope.current_page = 1;
    $scope.pages = list.length / page_interval;
    if($scope.pages > parseInt($scope.pages))
        $scope.pages = parseInt($scope.pages) + 1;
    $scope.visible_list = list.slice(0, page_interval);
}
    
function select_page(page, list, $scope, page_interval) {
    if(!page_interval)
        var page_interval = 20;
    var last_page = page - 1;
    var start = (last_page * page_interval);
    var end = page_interval * page;
    $scope.visible_list = list.slice(start, end);
    $scope.current_page = page;
}

function validateEmail(email) { 
    var re = /\S+@\S+\.\S+/;
    return re.test(email);
}

function show_loader(){
    $('#overlay').css('display', 'block');
    $('.spinner').css('display', 'block');
}
function hide_loader(){
    $('#overlay').css('display', 'none');
    $('.spinner').css('display', 'none');
}
function show_dropdow(){
    $('#dropdown_menu').css('display', 'block');
}
function hide_dropdown(){
    $('#dropdown_menu').css('display', 'none');
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
            console.log($scope.new_user);
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
             if(data.result == 'ok'){
                $scope.msg = "";
                $scope.get_users();
                $scope.reset_user();
                $scope.edit_flag = false;
             }         
             else
                $scope.msg = "Username already exists";
                
            }).error(function(data, status){
                $scope.message = data.message;
            });
        }        
    }
    $scope.delete_user = function(user){
        show_loader();
        var url = '/delete_user/?id='+user.id;
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
        $scope.show_popup = false;
    }
    $scope.edit_field = function(field){
        $scope.new_field.field_name = field.name;
        $scope.new_field.field_description = field.description;
        $scope.new_field.id = field.id;
    }
    $scope.delete_field = function(field){
        var url = '/delete_field/?id='+field.id;
        $http.get(url).success(function(data){
            if(data.result == 'ok'){
                $scope.msg = "Field deleted";
            } else if(data.result == 'error'){
                $scope.error_msg = "This Field is used in a function formula";
            }
            $scope.get_fields(); 
        })
    }
    $scope.get_fields = function(){
        var url = '/field_settings/';
        $http.get(url).success(function(data) {
            $scope.fields = data.fields;
        })
    }
    $scope.validate_field = function(){
        $scope.msg = '';
        var letters = /^[0-9a-zA-Z_]+$/;  
        if($scope.new_field.field_name == '') {
            $scope.msg = "Please enter Field Name";
            return false;
        } else if(!$scope.new_field.field_name.match(letters)) {
            $scope.msg = "Special characters and spaces are not allowed in field name (Only Alphabets, Numerals and _ is allowed)";
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
            show_loader();
            params = { 
                'field_details': angular.toJson($scope.new_field),
                "csrfmiddlewaretoken" : $scope.csrf_token,
            }
            $http({
                method : 'post',
                url : "/field_settings/",
                data : $.param(params),
                headers : {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data, status) { 
                hide_loader(); 
                if(data.result == 'error')
                     $scope.msg = "Field already exists";
                else
                    $scope.reset_field();       
                $scope.get_fields();                    
            }).error(function(data, status){
                $scope.message = data.message;
            });
        }        
    }
    $scope.reset_field = function(){
        $scope.msg = "";
        $scope.new_field = {
         'field_name': '',
         'field_description': '',
         'id': '',
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
    $scope.hide_popup_divs = function(){
        $('#assign_mentee_mentor').css('display', 'none');
        $('#assign_mentee_saq').css('display', 'none');
    }
}


function FunctionController($scope, $element, $http, $timeout, $location)
{
    
    $scope.init = function(csrf_token){
        $scope.csrf_token = csrf_token;
        $scope.hide_dropdown();
        $scope.change_type();
        /*$scope.get_category();*/
        $scope.get_analytical_head();
        $scope.get_functions();
        $scope.show_general = true;
        $scope.show_consistency = false;
        $scope.show_continuity = false;    
        $scope.select_type = 1;  
        $scope.get_operands();
        $scope.get_operators();
        $scope.get_fields();
        $scope.new_general = {
            'function_name': '',
            'function_description': '',
            'function_formula': [],
            'select_head': '',
        }
        $scope.new_continuity = {
            'function_name': '',
            'function_description': '',
            'no_of_periods': '',           
            'periods': [],               
            'select_head': '',
        }
        $scope.new_consistency = {
            'function_name': '',
            'function_description': '',
            'no_of_periods': '',
            'mean': '',
            'periods': [],          
            'select_head': '',
        }
        /*$scope.select_category = ''*/
        $scope.selected_operators = [];
        $scope.selected_operands = [];
        $scope.test = ['sd', '+', 'dg'].join(' ');
    }
    $scope.change_type = function(type){
        if(type == 1)
        {
         $scope.show_general = true;
         $scope.show_continuity = false;
         $scope.show_consistency = false;
         $scope.reset_continuity();
         $scope.reset_consistency();
         /*$scope.select_category = ''*/
         $scope.msg = '';
        }
       if(type == 2)
        {
         $scope.show_general = false;
         $scope.show_continuity = true;
         $scope.show_consistency = false;
         $scope.reset_general();
         $scope.reset_consistency();
         /*$scope.select_category = ''*/
         $scope.msg = '';
        }       
       if(type == 3)
        {
         $scope.show_general = false;
         $scope.show_continuity = false;
         $scope.show_consistency = true;
         $scope.reset_general();
         $scope.reset_continuity();
         /*$scope.select_category = ''*/
         $scope.msg = '';
        }       
    }
    $scope.add_periods_continuity = function(new_continuity){       
        var no_of_periods = new_continuity.no_of_periods;
        $scope.msg = '';
        if(no_of_periods > $scope.fields.length)
            $scope.msg = "No of periods should not be greater than number of fields";
        else if (no_of_periods > 0){
            for(var i = 0; i < no_of_periods; i++){
                new_continuity.periods.push({
                    'count': i+1,
                    'period' : '',
                });
            }
        }  else {
            var diff = new_continuity.periods.length - no_of_periods ;
            for (i=diff; i >0; i--){
                last_index = new_continuity.periods.indexOf(new_continuity.periods[new_continuity.periods.length - 1]);
                new_continuity.periods.splice(last_index, 1);
            }
        }      
    }

    $scope.add_periods_consistency = function(new_consistency){        
        var no_of_periods = new_consistency.no_of_periods;
        $scope.msg = '';
        if(no_of_periods > $scope.fields.length)
            $scope.msg = "No of periods should not be greater than number of fields";
        else if (no_of_periods > 0){
            for(var i = 0; i < no_of_periods; i++){
                new_consistency.periods.push({
                    'count': i+1,
                    'period' : '',
                });
            }
        }  else {
            var diff = new_consistency.periods.length - no_of_periods ;
            for (i=diff; i >0; i--){
                last_index = new_consistency.periods.indexOf(new_consistency.periods[new_consistency.periods.length - 1]);
                new_consistency.periods.splice(last_index, 1);
            }
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
        } else if($scope.formula == '' ) {
            $scope.msg = "Please enter Formula";
            return false;
        } else if($scope.new_general.select_head == '' ) {
            $scope.msg = "Please select analytical head";
            return false;
        } /*else if($scope.select_category == '' ) {
            $scope.msg = "Please select category";
            return false;
        }*/ else {
            return true;
        }  
    }
    $scope.validate_field_continuity = function(){
        $scope.msg = '';
        $scope.flag = 1;
        if($scope.new_continuity.function_name == '') {
            $scope.msg = "Please enter Function Name";
            return false;
        } else if($scope.new_continuity.function_description == '' ) {
            $scope.msg = "Please enter Function Description";
            return false;
        } else if($scope.new_continuity.no_of_periods == '' ) {
            $scope.msg = "Please enter Number of periods";
            return false;
        } else if(!Number($scope.new_continuity.no_of_periods) ) {
            $scope.msg = "Invalid entry in field No of Periods";
            return false;
        } else if($scope.new_continuity.select_head == '' ) {
            $scope.msg = "Please select analytical head";
            return false;
        } else if($scope.new_continuity.no_of_periods > $scope.fields.length){
            $scope.msg = "No of periods should not be greater than number of fields";
            return false;
        } else if($scope.new_continuity.no_of_periods > 0){
            for(var i = 1; i <= $scope.new_continuity.no_of_periods; i++){
                if($scope.new_continuity.periods[i-1].period == ''){
                    $scope.flag = 0;
                    $scope.msg = "please choose the value for period "+ i;
                    break;
                }
                for(var j = i+1; j <= $scope.new_continuity.no_of_periods; j++){
                    if($scope.new_continuity.periods[i-1].period == $scope.new_continuity.periods[j-1].period){
                        $scope.flag = 0;
                        $scope.msg = "Duplicate values in periods is not allowed";
                        break;
                    }                        
                }
            }  
        }
        if($scope.flag == 1) 
            return true;         
        else
            return false;
    }
    $scope.validate_field_consistency = function(){
        $scope.msg = '';
        $scope.flag = 1;
        if($scope.new_consistency.function_name == '') {
            $scope.msg = "Please enter Function Name";
            return false;
        } else if($scope.new_consistency.function_description == '' ) {
            $scope.msg = "Please enter Function Description";
            return false;
        } else if($scope.new_consistency.no_of_periods == '' ) {
            $scope.msg = "Please enter Number of periods";
            return false;
        } else if(!Number($scope.new_consistency.no_of_periods) ) {
            $scope.msg = "Invalid entry in field No of Periods";
            return false;
        } else if($scope.new_consistency.mean == '' ) {
            $scope.msg = "Please enter Mean";
            return false;
        } else if(!Number($scope.new_consistency.mean) ) {
            $scope.msg = "Invalid entry in field mean";
            return false;
        } else if($scope.new_consistency.select_head == '' ) {
            $scope.msg = "Please select analytical head";
            return false;
        } else if($scope.new_consistency.no_of_periods > $scope.fields.length){
            $scope.msg = "No of periods should not be greater than number of fields";
            return false;
        } else if($scope.new_consistency.no_of_periods > 0){
            for(var i = 1; i <= $scope.new_consistency.no_of_periods; i++){
                if($scope.new_consistency.periods[i-1].period == ''){
                    $scope.flag = 0;
                    $scope.msg = "please choose the value for period "+ i;
                    break;
                }
                for(var j = i+1; j <= $scope.new_consistency.no_of_periods; j++){
                    if($scope.new_consistency.periods[i-1].period == $scope.new_consistency.periods[j-1].period){
                        $scope.flag = 0;
                        $scope.msg = "Duplicate values in periods is not allowed";
                        break;
                    }                        
                }
            }
        }
        if($scope.flag == 1) 
            return true;         
        else
            return false; 
    }
    $scope.save_new_general = function(){
        if($scope.validate_field_general()){
            show_loader();
            params = { 
                'function_details': angular.toJson($scope.new_general),
                'function_type' : angular.toJson($scope.select_type),
                /* 'function_category' : angular.toJson($scope.select_category),*/  
                'formula_operands': angular.toJson($scope.selected_operands),
                'formula_operators': angular.toJson($scope.selected_operators),
                'formula_string': $scope.formula,
                "csrfmiddlewaretoken" : $scope.csrf_token,
            }
            $http({
                method : 'post',
                url : "/function_settings/",
                data : $.param(params),
                headers : {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data, status) {  
                hide_loader();
                if(data.result == 'error'){
                    $scope.msg = "Function already exists";
                }
                else{
                    document.location.href = "/function_settings/";
                }
            }).error(function(data, status){
                $scope.message = data.message;
            });
        }        
    }
    $scope.save_new_continuity = function(){        
        if($scope.validate_field_continuity()){            
            show_loader();
            params = { 
                'function_details': angular.toJson($scope.new_continuity),
                'function_type' : angular.toJson($scope.select_type),
                /*'function_category' : angular.toJson($scope.select_category),*/
                "csrfmiddlewaretoken" : $scope.csrf_token,
            }
            $http({
                method : 'post',
                url : "/function_settings/",
                data : $.param(params),
                headers : {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data, status) {  
                hide_loader();
                if(data.result == 'error'){
                     $scope.msg = "Function already exists";
                    }
                else
                    $scope.reset_continuity ();
                $scope.get_functions();    
            }).error(function(data, status){
                $scope.message = data.message;
            });
        }        
    }
    $scope.save_new_consistency = function(){
        if($scope.validate_field_consistency()){            
            show_loader();
            params = { 
                'function_details': angular.toJson($scope.new_consistency),
                'function_type' : angular.toJson($scope.select_type),
                /*'function_category' : angular.toJson($scope.select_category),*/
                "csrfmiddlewaretoken" : $scope.csrf_token,
            }
            $http({
                method : 'post',
                url : "/function_settings/",
                data : $.param(params),
                headers : {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data, status) {  
                hide_loader();
                if(data.result == 'error'){
                     $scope.msg = "Function already exists";
                    }
                else
                    $scope.reset_consistency();
                $scope.get_functions();   
            }).error(function(data, status){
                $scope.message = data.message;
            });
        }        
    }
    $scope.reset_general = function(){
        $scope.msg = "";
        $scope.new_general = {
            'id': '',
            'function_name': '',
            'function_description': '',
            'function_formula': '',            
            'select_head': '',
        } 
    }
    $scope.reset_continuity = function(){
        $scope.msg = "";
        $scope.new_continuity = {
            'id': '',
            'function_name': '',
            'function_description': '',
            'no_of_periods': '',          
            'periods': [],
            'select_head': '',
        }         
    }
    $scope.reset_consistency = function(){
        $scope.msg = "";
        $scope.new_consistency = {
            'id': '',
            'function_name': '',
            'function_description': '',
            'no_of_periods': '',
            'mean': '',
            'periods': [],
            'select_head': '',
        }  
    }
    $scope.edit_function = function(field){
        if(field.function_type == 'general'){
            $scope.change_type('1');
            $scope.edit_general(field.id);          
        }
        else if(field.function_type == 'continuity'){
            $scope.change_type('2');
            $scope.edit_continuity(field.id);          
        }
        else if(field.function_type == 'consistency'){
            $scope.change_type('3');
            $scope.edit_consistency(field.id);             
        }   
    }
    $scope.edit_general = function(id){
        var url = '/general_function/?id='+id;
        $http.get(url).success(function(data) {
            $scope.selected_general_function = data.general_function;
            $scope.select_type = 1;
            $scope.new_general.id = $scope.selected_general_function.id;
            $scope.new_general.function_name = $scope.selected_general_function.name;
            $scope.new_general.function_description = $scope.selected_general_function.description;
            $scope.formula = $scope.selected_general_function.formula;
            /*$scope.select_category = $scope.selected_general_function.category;*/
            $scope.new_general.select_head = $scope.selected_general_function.head;
            $scope.selected_operands = data.general_function.formula_operands;
            $scope.selected_operators = data.general_function.formula_operators;
        })
    }
    $scope.edit_continuity = function(id){
        var url = '/continuity_function/?id='+id;
        $http.get(url).success(function(data) {         
            $scope.continuity_list = data.continuity_objects;
            $scope.periods_list = data.continuity_objects[0].periods;           
            $scope.select_type = 2;
            $scope.new_continuity.id = $scope.continuity_list[0].id;
            $scope.new_continuity.function_name = $scope.continuity_list[0].name;
            $scope.new_continuity.function_description = $scope.continuity_list[0].description;
            $scope.new_continuity.no_of_periods = $scope.continuity_list[0].no_of_periods;            
            for(var i = 0; i < $scope.periods_list.length ; i++){
                $scope.new_continuity.periods.push({
                    'count': i+1,
                    'period' : $scope.periods_list[i].id,
                });
            }         
            $scope.new_continuity.select_head = $scope.continuity_list[0].head;
        })
    }
    $scope.edit_consistency = function(id){
        var url = '/consistency_function/?id='+id;
        $http.get(url).success(function(data) {
            $scope.consistency_list = data.consistency_objects;
            $scope.periods_list = data.consistency_objects[0].periods; 
            $scope.select_type = 3;
            $scope.new_consistency.id = $scope.consistency_list[0].id;
            $scope.new_consistency.function_name = $scope.consistency_list[0].name;
            $scope.new_consistency.function_description = $scope.consistency_list[0].description;
            $scope.new_consistency.no_of_periods = $scope.consistency_list[0].no_of_periods;            
            for(var i = 0; i < $scope.periods_list.length ; i++){
                $scope.new_consistency.periods.push({
                    'count': i+1,
                    'period' : $scope.periods_list[i].id,
                });
            } 
            $scope.new_consistency.mean = $scope.consistency_list[0].mean;
            /*$scope.select_category = $scope.consistency_list[0].category;*/
            $scope.new_consistency.select_head = $scope.consistency_list[0].head;
        })
    }
    /*$scope.get_category = function(){
        var url = '/category/';
        $http.get(url).success(function(data) {
            $scope.category_set = data.category_objects;
        })
    }*/
    $scope.get_fields = function(){
        var url = '/field_settings/';
        $http.get(url).success(function(data) {
            $scope.fields = data.fields;
        })
    }
    $scope.get_analytical_head = function(){
        var url = '/analytical_heads/';
        $http.get(url).success(function(data) {
            $scope.anly_heads = data.head_objects;
        })
    }
    $scope.get_functions = function(){
        var url = '/function_settings/';
        $http.get(url).success(function(data) {
            $scope.functions = data.functions;
        })
    }
    $scope.get_operands = function(){
        var url = '/field_settings/';
        $http.get(url).success(function(data) {
            $scope.operands = data.fields;
        })  
    }
    $scope.get_operators = function(){
        var url = '/operators/';
        $http.get(url).success(function(data) {
            $scope.operators = data.operators;
        })  
    }
    $scope.add_operand = function(){
        $scope.error_msg = '';
        if($scope.new_general.function_formula.length == 0) {
            $scope.selected_operands = [];
            $scope.selected_operators = [];
        }

        if($scope.operator_added || ($scope.new_general.function_formula.length == 0)){
            $scope.new_general.function_formula.push($scope.selected_operand.name);
            $scope.operator_added = false;
            $scope.operand_added = true;
            $scope.selected_operands.push($scope.selected_operand);
            $scope.formula = $scope.new_general.function_formula.join(' ')
            console.log('$scope.formula', $scope.formula);
        } else {
            $scope.error_msg = "Please add an operator";
        }
    }
    $scope.select_operator = function(operator){
        $scope.selected_operator = operator;
    }
    $scope.select_operand = function(operand){
        $scope.selected_operand = operand;
    }
    $scope.add_operator = function(){
        if($scope.new_general.function_formula.length == 0) {
            $scope.selected_operands = [];
            $scope.selected_operators = [];
        }
        $scope.error_msg = '';
        if($scope.operand_added || ($scope.new_general.function_formula.length == 0 && $scope.selected_operator.symbol == "(")){
            $scope.new_general.function_formula.push($scope.selected_operator.symbol);
            $scope.operand_added = false;
            $scope.operator_added = true;
            $scope.selected_operators.push($scope.selected_operator);
            $scope.formula = $scope.new_general.function_formula.join(' ')
        } else {
            $scope.error_msg = "Please add an operand";
        }
    }
    $scope.clear = function(){
        $scope.error_msg = '';
        $scope.new_general.function_formula.pop();
        $scope.formula = $scope.new_general.function_formula.join(' ')
        if($scope.operator_added){
            $scope.selected_operators.pop();
            $scope.operator_added = false;
            $scope.operand_added = true;
        }
        if($scope.operand_added){
            $scope.selected_operands.pop();
            $scope.operand_added = false;
            $scope.operator_added = true;
        }
    }
    $scope.add_digits = function(){
        if($scope.new_general.function_formula.length == 0) {
            $scope.selected_operands = [];
            $scope.selected_operators = [];
        }
        $scope.error_msg = '';        
        if($scope.operator_added || ($scope.new_general.function_formula.length == 0)){
            if(!Number($scope.digits)){
                $scope.error_msg = "Please Enter Digits";
                return;
            }
            $scope.new_general.function_formula.push($scope.digits);
            $scope.operator_added = false;
            $scope.operand_added = true;
            $scope.formula = $scope.new_general.function_formula.join(' ')
        } else {
            $scope.error_msg = "Please add an operator";
        }
    }
}

function ModelController($scope, $element, $http, $timeout, $location)
{
    $scope.new_model = {
        'model_name': '',
        'model_description': '',
        'industry_select': '',
        'industry_list': '',
        'id': '',
    }
    $scope.model = {
        'parameter_set': [
            {
                "analytical_head_name": "", 
                "function_set": [
                    {
                        "function_id": '', 
                        "parameter_set": {
                            'neutral_max': '',    
                            'neutral_min': '',                                    
                            'neutral_points': '',                                    
                            'parameter_id': '',                                    
                            'strong_max': '',                                    
                            'strong_min': '',                                    
                            'strong_points': '',                                    
                            'weak_max': '',                                    
                            'weak_min': '',                                    
                            'weak_points': '',
                            'strong_comment': '',
                            'weak_comment': '',
                            'neutral_comment': '',
                        },        
                        "function_name": " "
                    }
                ]
            }
        ],
       
    }
    $scope.selected_data = [];
    $scope.init = function(csrf_token){
        $scope.csrf_token = csrf_token;
        $scope.hide_dropdown();
        $scope.get_industries();
        $scope.get_models();
        $scope.create_model = true; 
        $scope.get_analytical_head();
        $scope.rightSelect = [];
        $scope.industry_selected = [];    
        $scope.show_table = false;
        $scope.editorEnabled = true;
        $scope.function_row = [];
        $scope.edit_parameters = false;
        $scope.selected_model = '';
    }
    $scope.show_create_model = function(){
        $scope.create_model = true; 
        $scope.define_model = false; 
        $scope.msg = "";
    }
    $scope.show_define_model = function(){
        $scope.create_model = false; 
        $scope.define_model = true; 
        $scope.msg = "";
    }
    $scope.get_industries = function(){
        var url = '/industry/';
        $http.get(url).success(function(data) {
            $scope.industry_list = data.industry_list;
            $scope.industry_select = '';
        }) 
    }
    $scope.get_models = function(){
        var url = '/models/';
        $http.get(url).success(function(data) {
            $scope.model_list = data.model_list;
        })
    }
    $scope.calculate_star_rating = function(){
        $scope.msg = '';
        if($scope.selected_model){
            var url = '/model/'+$scope.selected_model+'/star_rating/';
            $http.get(url).success(function(data) {
                $scope.model_list = data.model_list;
            })
        } else {
            $scope.msg = "Please select a model";
        }
    }
    $scope.get_analytical_head = function(){
        var url = '/analytical_heads/';
        $http.get(url).success(function(data) {
            $scope.anly_heads = data.head_objects;           
        })
    }
    $scope.get_model_details = function(id){
        $scope.msg = "";
        $scope.show_table = true;
        $scope.function_row = [];
        $scope.parameter_set = [];
        $scope.function_set = [];
        $scope.function_view = [];
        $scope.edit_parameters = false;
        $scope.flag = 0;
        show_loader();
        var url = '/model_details/?id='+id;
        $http.get(url).success(function(data) {
            hide_loader();
            $scope.analytical_heads = data.analytical_heads;           
            for(i = 0; i< $scope.analytical_heads.length; i++) {
                if($scope.analytical_heads[i].empty_functions.length > 0) {
                    $scope.analytical_heads[i].function_set.push({
                        "function_id": '', 
                        "parameter_set": {
                            'neutral_max': '',    
                            'neutral_min': '',                                    
                            'neutral_points': '',                                    
                            'parameter_id': '',                                    
                            'strong_max': '',                                    
                            'strong_min': '',                                    
                            'strong_points': '',                                    
                            'weak_max': '',                                    
                            'weak_min': '',                                    
                            'weak_points': '',
                            'strong_comment': '',
                            'weak_comment': '',
                            'neutral_comment': '',
                        },        
                        "function_name": " "
                    })
                }
            }
            
            $scope.star_ratings = data.star_ratings;
            $scope.star_ratings.push({
                'id': '',
                'star_count': '',
                'min_score': '',
                'max_score': '',
                'comment': '',
                'editorEnabled': true,
            })
         })
    }
    $scope.add_function = function(model_id, function_id, parameters,entry){ 
        $scope.edit_parameters = false;
        $scope.save_parameters(model_id, function_id, parameters);
        var count = 0;
        for(var i = 0; i < $scope.analytical_heads.length; i++ ){
            if($scope.model_details[i].analytical_head_id == entry.head_id)
                var count = $scope.model_details[i].function_set.length;
        }
        if(count > entry.function_set.length) {
            entry.function_set.push({
                'editorEnabled': true,
                'dropdown_enabled': true,
            }); 
        }                       
    }

    $scope.save_parameters = function(model_id, function_id, parameters){ 
        if($scope.validate_parameters(function_id, parameters)){
            show_loader();
            params = { 
                'model_id': angular.toJson(model_id),
                'function_id': angular.toJson(function_id),
                'parameters' : angular.toJson(parameters),
                "csrfmiddlewaretoken" : $scope.csrf_token,
            }
            $http({
                method : 'post',
                url : "/model_details/",
                data : $.param(params),
                headers : {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data, status) {  
                hide_loader();
                $scope.edit_parameters = false;
                $scope.get_model_details(model_id);
                }).error(function(data, status){
                $scope.message = data.message;
            });
        }  
       
    }
    
    $scope.edit_function = function(model_function){
       if(model_function.parameter_set){
            $scope.edit_parameters = true;
            model_function.editorEnabled = true;
       }
    }
    $scope.edit_rating = function(rating){
        $scope.edit_rating = true;
        rating.editorEnabled = true;
    }
    $scope.delete_parameters = function(model_id, parameters){
        show_loader();
        var url = '/delete_parameters/?id='+parameters.parameter_id;
        $http.get(url).success(function(data){
            hide_loader();
            if(data.result == 'ok')
                $scope.msg = "Parameters deleted";
            else 
                $scope.msg = "Error";
            $scope.get_model_details(model_id);              
        })
     }
    $scope.moveRight = function(){
        $scope.flag = 1;
        for(var i = 0; i < $scope.industry_list.length; i++)
            $scope.industry_list[i].selected = false;
        for(var i = 0; i < $scope.industry_list.length; i++){
            $scope.selected_data.push({
                'id': $scope.industry_list[i].id,
                'name': $scope.industry_list[i].name});
        }
        for(var i = 0; i < $scope.selected_data.length; i++){
            for(var j = 0; j < $scope.new_model.industry_list.length; j++) {
                if($scope.selected_data[i].id == $scope.new_model.industry_list[j])
                {
                    if($scope.rightSelect.length == 0)
                    {
                        $scope.rightSelect.push($scope.selected_data[i]);
                        $scope.flag = 0;
                    }
                else
                    for(var k = 0; k < $scope.rightSelect.length; k++)
                    {
                        if($scope.rightSelect[k].id == $scope.new_model.industry_list[j])
                            $scope.flag = 0;
                    }
                    if($scope.flag == 1)
                        $scope.rightSelect.push($scope.selected_data[i]);
                    $scope.flag = 1;
                }
            }
        }$scope.flag = 1;
        for(var i = 0; i < $scope.rightSelect.length; i++)
            $scope.rightSelect[i].selected = false;
    }
    $scope.moveLeft = function(){
        for(var i = 0; i < $scope.new_model.industry_select.length; i++) 
        {   
            for(var j = 0; j < $scope.rightSelect.length; j++)
            {
                if(($scope.rightSelect[j].id == $scope.new_model.industry_select[i]))
                   $scope.rightSelect.splice($scope.rightSelect.indexOf($scope.rightSelect[j]), 1)
            }
        }

       
    }
    $scope.selectallLeft = function(){
        for(var i = 0; i < $scope.industry_list.length; i++){
            if($scope.industry_list[i].selected == true)
                $scope.industry_list[i].selected = false;
            else
                $scope.industry_list[i].selected = true;
        }
        $scope.select = [];
        for(var i = 0; i < $scope.industry_list.length; i++)
            $scope.select.push($scope.industry_list[i].id);
        $scope.new_model.industry_list = $scope.select; 
    }
    $scope.selectallRight = function(){
        for(var i = 0; i < $scope.rightSelect.length; i++)
            if($scope.rightSelect[i].selected == true)
                $scope.rightSelect[i].selected = false;
            else
                $scope.rightSelect[i].selected = true;
        $scope.select = [];
        for(var i = 0; i < $scope.rightSelect.length; i++)
            $scope.select.push($scope.rightSelect[i].id)
        $scope.new_model.industry_select = $scope.select;     
    }
    $scope.validate_model = function(){
        $scope.msg = '';
        $scope.flag = 0;
        for(var i = 0; i < $scope.anly_heads.length; i++){
            if($scope.anly_heads[i].selected == true)
                $scope.flag = 1;
        }
        if($scope.new_model.model_name == '') {
            $scope.msg = "Please enter Model Name";
            return false;
        } else if($scope.new_model.model_description == '' ) {
            $scope.msg = "Please enter Model Description";
            return false;
        } else if($scope.rightSelect.length == 0 ) {
            $scope.msg = "Please select atleast one industry";
            return false;
        } else if($scope.flag == 0){
            $scope.msg = "Please select atleast one Analytical Head";
            return false;
        } else {
            return true;
        }  
    }
    $scope.validate_parameters = function(function_id, parameters){
        $scope.msg = '';
        if(angular.isUndefined(function_id) && !$scope.edit_parameters) {
            $scope.msg = "Please select a function";
            return false;
        } else if(angular.isUndefined(parameters) || parameters.strong_min == ''){
            $scope.msg = "Please enter Strong Minimum";
            return false;
        } else if(!Number(parameters.strong_min) ) {
            $scope.msg = "Invalid entry in Strong Minimum";
            return false;
        } else if(angular.isUndefined(parameters.strong_max) || parameters.strong_max == ''){
            $scope.msg = "Please enter Strong Maximum";
            return false;
        } else if(!Number(parameters.strong_max) ) {
            $scope.msg = "Invalid entry in Strong Maximum";
            return false;
        } else if(angular.isUndefined(parameters.strong_points) || parameters.strong_points == ''){
            $scope.msg = "Please enter Strong Points";
            return false;
        } else if(!Number(parameters.strong_points) ) {
            $scope.msg = "Invalid entry in Strong Points";
            return false;
        } else if(angular.isUndefined(parameters.neutral_min) || parameters.neutral_min == ''){
            $scope.msg = "Please enter Neutral Minimum";
            return false;
        } else if(!Number(parameters.neutral_min) ) {
            $scope.msg = "Invalid entry in Neutral Minimum";
            return false;
        } else if(angular.isUndefined(parameters.neutral_max) || parameters.neutral_max == ''){
            $scope.msg = "Please enter Neutral Maximum";
            return false;
        } else if(!Number(parameters.neutral_max) ) {
            $scope.msg = "Invalid entry in Neutral Maximum";
            return false;
        } else if(angular.isUndefined(parameters.neutral_points) || parameters.neutral_points == ''){
            $scope.msg = "Please enter Neutral Points";
            return false;
        } else if(!Number(parameters.neutral_points) ) {
            $scope.msg = "Invalid entry in Neutral Points";
            return false;
        } else if(angular.isUndefined(parameters.weak_min) || parameters.weak_min == ''){
            $scope.msg = "Please enter Weak Minimum";
            return false;
        }  else if(!Number(parameters.weak_min) ) {
            $scope.msg = "Invalid entry in Weak Minimum";
            return false;
        } else if(angular.isUndefined(parameters.weak_max) || parameters.weak_max == ''){
            $scope.msg = "Please enter Weak Maximum";
            return false;
        } else if(!Number(parameters.weak_max) ) {
            $scope.msg = "Invalid entry in Weak Maximum";
            return false;
        } else if(angular.isUndefined(parameters.weak_points) || parameters.weak_points == ''){
            $scope.msg = "Please enter Weak Points";
            return false;
        } else if(!Number(parameters.weak_points) ) {
            $scope.msg = "Invalid entry in Weak Points";
            return false;
        } else if(Number(parameters.strong_min) >= Number(parameters.strong_max)) {
            $scope.msg = "Strong Minimum should be less than Strong Maximum";
            return false;
        } else if(Number(parameters.neutral_min) >= Number(parameters.neutral_max)) {
            $scope.msg = "Neutral Minimum should be less than Neutral Maximum";
            return false;
        } else if(parameters.weak_min >= parameters.weak_max) {
            $scope.msg = "Weak Minimum should be less than Weak Maximum";
            return false;
        } if(angular.isUndefined(function_id) && angular.isUndefined(parameters.parameter_id)) {
            $scope.msg = "Please select a function";
            return false;
        } if(angular.isUndefined(function_id) && angular.isUndefined(parameters.parameter_id)) {
            $scope.msg = "Please select a function";
            return false;
        } else {
            return true;
        }

    }
    $scope.validate_rating = function(rating){
        $scope.rating_msg = '';
        if(!Number(rating.star_count) ) {
            $scope.rating_msg = "Invalid entry in Star Count";
            return false;
        } else if(!Number(rating.min_score) ){
            $scope.rating_msg = "Please enter in Min Score";
            return false;
        } else if(!Number(rating.max_score) ) {
            $scope.rating_msg = "Invalid entry in Max Score";
            return false;
        } else if(rating.comment == ''){
            $scope.rating_msg = "Please enter Comment";
            return false;
        } else {
            return true;
        }
    }
    $scope.save_model = function(){
        if($scope.validate_model()){
            show_loader();
            for(var i = 0; i < $scope.anly_heads.length; i++)
                $scope.anly_heads[i].selected = String($scope.anly_heads[i].selected);
            for(var i = 0; i < $scope.rightSelect.length; i++)
                $scope.industry_selected.push($scope.rightSelect[i].id);
            params = { 
                'model_details': angular.toJson($scope.new_model),
                'analytical_heads': angular.toJson($scope.anly_heads),
                'industry_selected': angular.toJson($scope.industry_selected),
                "csrfmiddlewaretoken" : $scope.csrf_token,
            }
            $http({
                method : 'post',
                url : "/models/",
                data : $.param(params),
                headers : {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data, status) { 
                hide_loader();
                if(data.result == 'error'){
                     $scope.msg = "Model already exists";
                    }
                else
                    $scope.reset_model(); 
                    $scope.get_models();        
             
              }).error(function(data, status){
                $scope.message = data.message;
            });
        } 

    }
    $scope.save_rating = function(rating){
        if($scope.validate_rating(rating)){
            show_loader();
            rating.editorEnabled = String(rating.editorEnabled);
            params = { 
                'rating': angular.toJson(rating),
                "csrfmiddlewaretoken" : $scope.csrf_token,
            }
            $http({
                method : 'post',
                url : "/model/"+$scope.selected_model+"/save_star_rating/",
                data : $.param(params),
                headers : {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data, status) { 
                hide_loader();
                if(data.result == 'error'){
                     $scope.msg = "Model already exists";
                    }
                else
                    $scope.reset_model(); 
                    $scope.get_models();        
             
              }).error(function(data, status){
                $scope.message = data.message;
            });
        } 

    }
    $scope.edit_field = function(model){
        $scope.reset_model(); 
        $scope.rightSelect = []
        $scope.new_model.model_name = model.name;
        $scope.new_model.model_description = model.description;
        $scope.new_model.id = model.id;
        for(var i=0; i < model.industry.length; i++){
            $scope.rightSelect.push(model.industry[i])
        }           
        for(var i=0; i < model.analytical_heads.length; i++){   //2
            for(var j=0; j < $scope.anly_heads.length; j++){    //3
                if(model.analytical_heads[i].id == $scope.anly_heads[j].id)
                    $scope.anly_heads[j].selected = true;
            }
        }
    }
    $scope.reset_model = function(){
        $scope.msg = '';
        $scope.new_model = {
            'model_name': '',
            'model_description': '',
            'id': ''
        }
        $scope.rightSelect = [];
        $scope.select = [];
        $scope.industry_selected = [];
        for(var i = 0; i < $scope.industry_list.length; i++)
            $scope.industry_list[i].selected = false;
        for(var i = 0; i < $scope.anly_heads.length; i++){
            $scope.anly_heads[i].selected = false;
        }
    }
    $scope.delete_model = function(field){
        show_loader();
        var url = '/delete_model/?id='+field.id;
        $http.get(url).success(function(data){
            hide_loader();
            if(data.result == 'ok'){
                $scope.msg = "Model deleted";
               }
            $scope.get_models();                    
        })
    }
    $scope.show_dropdown = function(){
        $('#dropdown_menu').css('display', 'block');
    }
    $scope.hide_dropdown = function(){
        $('#dropdown_menu').css('display', 'none');
    }
}

function DataUploadController($scope, $element, $http, $timeout, $location)
{
    $scope.init = function(csrf_token){
        $scope.csrf_token = csrf_token;
        $scope.hide_dropdown();
        $scope.data_file = {};
        $scope.data_file.src = "";
    }
    $scope.show_dropdown = function(){
        $('#dropdown_menu').css('display', 'block');
    }
    $scope.hide_dropdown = function(){
        $('#dropdown_menu').css('display', 'none');
    }
    $scope.submit_file = function(){
        $scope.error_msg = '';
        if($scope.data_file.src){
            var split_name = $scope.data_file.src.name.split('.');
            split_name = split_name[split_name.length - 1];
            var extensions = ['xlsx', 'xlsm', 'xlsb', 'xltm', 'xlam', 'xls', 'xla', 'xlb', 'xlc', 'xld', 'xlk', 'xll', 'xlm', 'xlt', 'xlv', 'xlw']
            var index = extensions.indexOf(split_name);
            if(index == -1){
                $scope.error_msg = "Please upload an excel file";
                return false;
            }
            var fd = new FormData();
            fd.append('data_file', $scope.data_file.src);
            fd.append('csrfmiddlewaretoken', $scope.csrf_token);
            show_loader();

            var url = '/data_upload/';
            $http.post(url, fd, {
                transformRequest: angular.identity,
                headers: {'Content-Type': undefined
                }
            }).success(function(data, status){ 
                hide_loader(); 
            }).error(function(data, status){           

            });
        } else {
            $scope.error_msg = "Please upload an excel file";
        }
        
    }
}
function FieldMappingController($scope, $element, $http, $timeout, $location)
{
    $scope.init = function(csrf_token, mapping_status){
        $scope.csrf_token = csrf_token;
        $scope.hide_dropdown();
        if(mapping_status == 'empty'){
            $scope.get_file_fields();
            $scope.get_system_fields(); 
            $scope.edit_flag = false; 
        } else {
            $scope.get_mapping();
            $scope.edit_flag = true;
        }              
    }
    $scope.fill_fields = function(){
        var diff = Math.abs($scope.file_fields.length - $scope.system_fields.length);
        if(diff > 0) {
            if($scope.system_fields.length > $scope.file_fields.length){
                for(i=1; i<=diff; i++){
                    $scope.file_fields.push(' ');
                }
            } else {
                for(i=1; i<=diff; i++){
                    $scope.system_fields.push({
                        "status": "", 
                        "date": "", 
                        "description": "", 
                        "id": '', 
                        "name": ""
                    });
                }
            }
        }
    }
    $scope.onDropComplete = function (index, obj, evt) {
        var otherObj = $scope.system_fields[index];
        var otherIndex = $scope.system_fields.indexOf(obj);
        $scope.system_fields[index] = obj;
        $scope.system_fields[otherIndex] = otherObj;
    }
    $scope.show_dropdown = function(){
        $('#dropdown_menu').css('display', 'block');
    }
    $scope.hide_dropdown = function(){
        $('#dropdown_menu').css('display', 'none');
    }
    $scope.get_file_fields = function(){
        $scope.error_msg = '';  
        var url = '/file_fields/';
        $http.get(url).success(function(data) {
            $scope.file_fields = data.fields;
            if($scope.system_fields)
                $scope.fill_fields();
        })       
    }
    $scope.get_system_fields = function(){
        $scope.error_msg = '';  
        var url = '/field_settings/';
        $http.get(url).success(function(data) {
            $scope.system_fields = data.fields;
            if($scope.file_fields)
                $scope.fill_fields();
        })     
    }
    $scope.get_mapping = function(){
        var url = '/field_mapping/';
        $http.get(url).success(function(data) {
            $scope.file_fields = data.file_fields;
            $scope.system_fields = data.system_fields;
            if($scope.system_fields)
                $scope.fill_fields();
        })  
    }
    $scope.save_mapping = function(){
        show_loader();
        params = { 
            'system_fields': angular.toJson($scope.system_fields),
            'file_fields': angular.toJson($scope.file_fields),
            "csrfmiddlewaretoken" : $scope.csrf_token,
        }
        $http({
            method : 'post',
            url : "/field_mapping/",
            data : $.param(params),
            headers : {
                'Content-Type' : 'application/x-www-form-urlencoded'
            }
        }).success(function(data, status) {  
            hide_loader();
            document.location.href = '/field_mapping/';
        }).error(function(data, status){
            $scope.message = data.message;
        });
    }
}

function AnalyticalHeadController($scope, $element, $http, $timeout, $location)
{
    $scope.new_head = {
        'head_name': '',
        'head_description': '',
        'id': '',
    }
    $scope.init = function(csrf_token){
        $scope.csrf_token = csrf_token;
        $scope.hide_dropdown();
        $scope.get_analytical_head();
       }
    $scope.show_dropdown = function(){
        $('#dropdown_menu').css('display', 'block');
    }
    $scope.hide_dropdown = function(){
        $('#dropdown_menu').css('display', 'none');
    }
    $scope.get_analytical_head = function(){
        var url = '/analytical_heads/';
        $http.get(url).success(function(data) {
            $scope.anly_heads = data.head_objects;
        })
    }
    $scope.validate_head = function(){
        $scope.msg = '';
        if($scope.new_head.head_name == '') {
            $scope.msg = "Please enter Analytical Head Name";
            return false;
        } else if($scope.new_head.head_description == '' ) {
            $scope.msg = "Please enter Analytical Head Description";
            return false;
        } else {
            return true;
        }
    }
    $scope.save_new_head = function(){
        if($scope.validate_head()){
            show_loader();
            params = { 
                'head_details': angular.toJson($scope.new_head),
                "csrfmiddlewaretoken" : $scope.csrf_token,
            }
            $http({
                method : 'post',
                url : "/analytical_heads/",
                data : $.param(params),
                headers : {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data, status) {  
                hide_loader();
                if(data.result == 'error')
                     $scope.msg = "Head already exists";
                else
                    $scope.reset_head();
                $scope.get_analytical_head();                    
            }).error(function(data, status){
                $scope.message = data.message;
            });
        }        
    }
    $scope.edit_head = function(head){
        $scope.new_head.head_name = head.title;
        $scope.new_head.head_description = head.description;
        $scope.new_head.id = head.id;
    }
    $scope.delete_head = function(head){
        show_loader();
        var url = '/delete_head/?id='+head.id;
        $http.get(url).success(function(data){
            hide_loader();
            if(data.result == 'ok')
                $scope.msg = "Analytical Head deleted";
            $scope.get_analytical_head();                    
        })
    }
    $scope.reset_head = function(){
        $scope.msg = '';
        $scope.new_head = {
         'head_name': '',
         'head_description': '',
         'id': '',
         }         
    }
}

function CompanyController($scope, $element, $http, $timeout, $location)
{
    $scope.init = function(csrf_token){
        $scope.csrf_token = csrf_token;
        $scope.hide_dropdown();
        $scope.data_file = {};
        $scope.data_file.src = "";
        $scope.range(5);
        $scope.get_companies();
        $scope.visible_list = [];
        $scope.page_interval = 30;
    }
    $scope.show_dropdown = function(){
        $('#dropdown_menu').css('display', 'block');
    }
    $scope.hide_dropdown = function(){
        $('#dropdown_menu').css('display', 'none');
    }
    $scope.submit_file = function(){
        $scope.error_msg = '';
        if($scope.data_file.src){
            var split_name = $scope.data_file.src.name.split('.');
            split_name = split_name[split_name.length - 1];
            var extensions = ['xlsx', 'xlsm', 'xlsb', 'xltm', 'xlam', 'xls', 'xla', 'xlb', 'xlc', 'xld', 'xlk', 'xll', 'xlm', 'xlt', 'xlv', 'xlw']
            var index = extensions.indexOf(split_name);
            if(index == -1){
                $scope.error_msg = "Please upload an excel file";
                return false;
            }
            var fd = new FormData();
            fd.append('data_file', $scope.data_file.src);
            fd.append('csrfmiddlewaretoken', $scope.csrf_token);
            show_loader();

            var url = '/companies/';
            $http.post(url, fd, {
                transformRequest: angular.identity,
                headers: {'Content-Type': undefined
                }
            }).success(function(data, status){ 
                hide_loader(); 
            }).error(function(data, status){           

            });
        } else {
            $scope.error_msg = "Please upload an excel file";
        }
        
    }
    $scope.get_companies = function(){
        var url = '/companies/';
        show_loader();
        $http.get(url).success(function(data) {
            $scope.companies = data.companies;
            paginate($scope.companies, $scope, $scope.page_interval);
            hide_loader();
        })
    }
    $scope.select_page = function(page){
        select_page(page, $scope.companies, $scope, $scope.page_interval);
    }
    $scope.select_next_page = function(){
        var page = $scope.current_page + 1;
        if(page != $scope.pages + 1)
            select_page(page, $scope.companies, $scope, $scope.page_interval);
    }
    $scope.select_previous_page = function(){
        var page = $scope.current_page - 1
        if(page != 0)
            select_page(page, $scope.companies, $scope, $scope.page_interval);
    }
    $scope.range = function(n) {
        return new Array(n);
    }
}

function RatingReportController($scope, $element, $http, $timeout, $location)
{
    $scope.init = function(csrf_token){
        $scope.csrf_token = csrf_token;
        hide_dropdown();
        $scope.visible_list = [];
        $scope.page_interval = 30;
        $scope.ratings = [];
        $scope.companies = [];
        $scope.search_keys = [];
    }
    $scope.show_dropdown = function(){
        $('#dropdown_menu').css('display', 'block');
    }
    $scope.hide_dropdown = function(){
        $('#dropdown_menu').css('display', 'none');
    }
    $scope.show_suggestions = function() {
        if($scope.companies.length > 0){
            $('#suggestions').css('display', 'block');
        } else {
            $('#suggestions').css('display', 'none');
        }
    }
    $scope.hide_suggestions = function(company){
        $('#suggestions').css('display', 'none');
        $scope.companies = [];
        $scope.search_keys.push(company.isin_code);
        $scope.search_text = $scope.search_keys.join(', ');
        $scope.search_key = '';
    }
    $scope.search_companies = function(){ 
        if($scope.search_key.length >= 3){
            var url = '/companies/?search_key='+$scope.search_key;
            show_loader();
            $http.get(url).success(function(data) {
                $scope.companies = data.companies;
                paginate($scope.companies, $scope, $scope.page_interval);
                hide_loader();
                $scope.show_suggestions();
            })
        }        
    }
    $scope.search_rating = function(){
       if($scope.search_keys.length > 0) {
            show_loader();
            var url = '/rating_report/';
            params = { 
                'search_keys': angular.toJson($scope.search_keys),
                "csrfmiddlewaretoken" : $scope.csrf_token,
            }
            $http({
                method : 'post',
                url : url,
                data : $.param(params),
                headers : {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data, status) {  
                hide_loader();
                $scope.star_ratings = data.star_ratings;                    
            }).error(function(data, status){
                $scope.message = data.message;
            });
       }
    }
}