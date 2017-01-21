var hackIdeasApp = angular.module('hackIdeasApp',[]);





hackIdeasApp.controller("searchEngine",function($scope, $rootScope,$http){
  $scope.enteredHackIdea = "test";
  $scope.technologiesList = ["C/C++","PHP","Machine Learning","Javascript"];
  $scope.hackProjects = [{"projName":"Hack Project 1","projDesc":"This is the description of project 1"},{"projName":"Hack Project 2","projDesc":"This is the description of project 2"}];


  $scope.submitIdea = function(){
    $rootScope.$broadcast("requestProjectList",
      {
        projectList:$scope.hackProjects
      });
  }


});
