hackIdeasApp.controller("projListing",function($scope, $rootScope,$http){
  $scope.enteredHackIdea = "Enter Idea";
  $scope.hackProjects = [{"projName":"Hack Project 1","projDesc":"This is the description of project 1"},{"projName":"Hack Project 2","projDesc":"This is the description of project 2"}];
  $scope.generatedIdea = "Select projects to generate an idea.";
  $scope.selectedProjects = [];
  $scope.checkedFlag = false;

  $scope.refreshProjectList = function(){
      $http({
        method: "GET",
        url: "<<DBLOC>>"
      }).then(function success(response){
        //console.log(response.data);
        //var myArray = JSON.parse(response.data);
        $scope.hackProjects = response.data;
      },function error(response){
        alert(response.statusText);
      });
    };


  /*$scope.$on("requestProjectList", function(event, args){
    $scope.hackProjects = args.projectList;
  });*/

  $scope.toggleSelectedProject = function(projName){
    console.log(includeProj);
    var projIndex = $scope.selectedProjects.indexOf(projName);
    var includeProj = $("#"+projName+"_check").is(':checked');
    alert(includeProj);
    console.log($("#"+projName+"_check"));
    if(includeProj){
      if(projIndex <= -1){
        $scope.selectedProjects.push(projName);
      }
    }
    else{
      if(projIndex >= 0){
        $scope.selectedProjects.splice();
      }
    }
  }

});
