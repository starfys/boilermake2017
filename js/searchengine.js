var hackIdeasApp = angular.module('hackIdeasApp',[]);

hackIdeasApp.controller("searchEngine",function($scope, $rootScope,$http){
  $scope.enteredHackIdea = "This is a test sentence, and this test is a great test.";
  $scope.technologiesList = ["C/C++","PHP","Machine Learning","Javascript"];

  /*$scope.markovChain_test = [{"this":{"is":0.5,"test":0.5}},
                        {"is":{"a":1.0}},
                        {"test":{"is":0.5,"sentence":1.0}},
                        {"a":{"great":0.5,"test":0.5}},
                        {"great":{"test":1.0}},
                        {"sentence":{"and":1.0}},
                        {"and":{"this":1.0}},
    ];*/

  $scope.userMarkovChain = [];

  $scope.genMarkovChain = function(enteredHackIdea_cp){
    var modString = enteredHackIdea_cp.replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g,"").toLowerCase();
    var splitStr = modString.split(" ");
    var currWord = "";
    var nextWord = "";

    //console.log(splitStr);

    $scope.userMarkovChain = new Object();

    for(wordIndex in splitStr){
      currWord = splitStr[wordIndex];
      if(wordIndex < splitStr.length){
        nextWord = splitStr[parseInt(wordIndex,10) + 1];
        //console.log(currWord +" , "+nextWord);
        if(typeof $scope.userMarkovChain[currWord] !== 'undefined'){
          if(typeof $scope.userMarkovChain[currWord][nextWord] !== 'undefined'){
            $scope.userMarkovChain[currWord][nextWord]++;
            //console.log("NEXT: "+nextWord);
            //console.log($scope.userMarkovChain[currWord][nextWord]);
          }
          else{
            $scope.userMarkovChain[currWord][nextWord] = 1;
          }
        }
        else{
          $scope.userMarkovChain[currWord] = new Object();
          $scope.userMarkovChain[currWord][nextWord] = 1;
        }
      }
    }

    console.log($scope.userMarkovChain);

  }


  $scope.submitIdea = function(){
    /*$rootScope.$broadcast("requestProjectList",
      {
        projectList:$scope.hackProjects
      });*/
    $scope.genMarkovChain($scope.enteredHackIdea);
  }

  // Listen for user's selection of new hackathon projects
  $scope.$on("selectedHacksChanged",function(events,args)
  {
    $scope.selectedProjects = args.selectedList;
    console.log($scope.selectedProjects);
  });

});
