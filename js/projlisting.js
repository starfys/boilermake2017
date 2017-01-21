hackIdeasApp.controller("projListing",function($scope, $rootScope,$http){
  $scope.enteredHackIdea = "Enter Idea";
  $scope.hackProjects = [];
  $scope.generatedIdeas = [];
  $scope.selectedProjects = [];
  $scope.checkedFlag = false;

  // Send the user's selections to the server for processing
  $scope.requestSelectMarkovProc = function(){
    var allUserInput = [];
    allUserInput.push($scope.selectedProjects);
    allUserInput.push($scope.hackProjects);
    allUserInput.push($scope.hackProjects);
    /*$http({
      method: "GET",
      url: "<<DBLOC>>"
      data: []
    }).then(function success(response){
      //console.log(response.data);
      //var myArray = JSON.parse(response.data);
      $scope.hackProjects = response.data;
    },function error(response){
      alert(response.statusText);
    });*/
  }

  $scope.refreshProjectList = function(){
      /*$http({
        method: "GET",
        url: "<<DBLOC>>"
      }).then(function success(response){
        //console.log(response.data);
        //var myArray = JSON.parse(response.data);
        $scope.hackProjects = response.data;
      },function error(response){
        alert(response.statusText);
      });*/

      $scope.hackProjects = [{"projName":"Hack Project 1","projDesc":"This is the description of project 1"},{"projName":"Hack Project 2","projDesc":"This is the description of project 2"}];
    };

    $scope.refreshGenProjectList = function(){
        /*$http({
          method: "GET",
          url: "<<DBLOC>>"
        }).then(function success(response){
          //console.log(response.data);
          //var myArray = JSON.parse(response.data);
          $scope.hackProjects = response.data;
        },function error(response){
          alert(response.statusText);
        });*/

        $scope.generatedIdeas = [{"projName":"Hack Project 1 -- Gen","projDesc":"This is the description of project 1"},{"projName":"Hack Project 2 -- Gen","projDesc":"This is the description of project 2"}];
      };


  /*$scope.$on("requestProjectList", function(event, args){
    $scope.hackProjects = args.projectList;
  });*/

  $scope.toggleSelectedProject = function(projName, projID){
    var compressedName = projName.split(' ').join('');
    var projIndex = $scope.selectedProjects.indexOf(projID);
    var includeProj = $("#"+compressedName+"_check").is(':checked');

    if(includeProj){
      if(projIndex <= -1){
        $scope.selectedProjects.push(projID);
      }
    }
    else{
      if(projIndex >= 0){
        $scope.selectedProjects.splice(projIndex,1);
      }
    }
    alert($scope.selectedProjects);

    $rootScope.$broadcast("selectedHacksChanged",
    {
      selectedList:$scope.selectedProjects
    });
  }


  // Default init runs
  $scope.refreshProjectList();
  $scope.refreshGenProjectList();
});
