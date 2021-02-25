app.controller("homeController", function($scope,$http,$sce) {
    $scope.title="ITCS 6150/8150 - Fall 2020 - RS Method Project"
    $scope.teammates=[{'name':"Ashwin Katale", 'id':801135232},{'name': "Siddhesh Sarfare",'id':801134143},{'name':"Nikhil Mungara",'id':801101010} ];



    $scope.submit=function(goal){
        /*$http({
            method: "POST",
            url: "http://127.0.0.1:5000/submit",
            headers: {
                'Content-Type': 'text/javascript',
            },
            data: {
                'goal': goal,
            }
        }).then(function successCallback(response){
            console.log(response.data)
            
        });*/
        $http({
            method: "POST",
            url: "http://127.0.0.1:5000/submit",
            headers: {
                 'Content-Type': 'application/json' 
            },
            data:JSON.stringify({'goal':goal,'formulas':[]})
        }).then(function successCallback(response){
            console.log(response.data)
            $scope.responseData=$sce.trustAsHtml(response.data)
            
        });
    }


  });