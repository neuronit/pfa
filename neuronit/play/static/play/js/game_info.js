

var game 
function network_parameters(network_type){
    //select TYPE name depending on network_type
    //select parameters depending on network_type
    var tmp = document.querySelectorAll(".network");
     for (var i = 0 ; i< tmp.length; i++){
         var x = document.getElementById(network_type);
         
	 
         if (tmp[i].id == x.getAttribute("id"))
             x.style.display='block';
         else
             tmp[i].style.display='none';
     }
    
}



function getname(identifier){     
    var tmp=identifier.getAttribute("name");
    info=identifier.getAttribute("info");
    currentGame.innerHTML=tmp;
    Gamecontent.innerHTML=info;
    game=tmp;
    // currentGame.setAttribute("name",tmp);
    
    
    $.ajax({
        type: 'GET',
	url: '/play/result',
        data: {'name': tmp},
	dataType: 'json',
        success: function (data) {


            
            // currentGame.setAttribute("name",tmp);
        },
        error: function (data) {
            alert("it didnt work");
        }
    });
 
    
    return tmp 
    
    
}

var graph2;
function send(){

    graph=send_to_backend();
    console.log(graph);
    $.ajax({
        type: 'GET',
	url: '/play/result_network',
        //data: graph, //{'graph': JSON.stringify(graph)},
	data: JSON.stringify(graph),
	//dataType: 'json',
	error: function (data) {
            alert("It didn't work !");
        },
 
        success: function (data) {
            ;//alert("yes !");

            
            //     // currentGame.setAttribute("name",tmp);
        }// ,
        // error: function (data) {
        //     alert("It didn't worked !");
        // }
    });
 
}  
