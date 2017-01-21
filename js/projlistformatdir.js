/*$('div[name=hackProjects] input[type="checkbox"]').click(function(e) {
    e.stopPropagation();
});*/

function formatProjList(){
  $( "div[name=hackProjects]" ).accordion({collapsible: true, active: false});
};



hackIdeasApp.directive('projListFormat',function(){
  return function(scope, element, attrs){
    if(scope.$last){
      formatProjList();
    }
  }
});
