hackIdeasApp.controller("projListing",function($scope, $rootScope,$http){
  $scope.enteredHackIdea = "Enter Idea";
  $scope.hackProjects = [];






  $scope.$on("requestProjectList", function(event, args){
    $scope.hackProjects = args.projectList;
  });


});
