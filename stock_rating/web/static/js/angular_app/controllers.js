
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
