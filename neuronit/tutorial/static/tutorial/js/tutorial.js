
var buttons;
var close;
$(document).ready(function(){
    buttons = document.getElementsByClassName("btn btn-primary btn-lg");
    close = document.getElementsByClassName("close");
    console.log(buttons,close);
    buttons[0].click();    

    
    
});



function step2(){
    buttons[1].click();
    close[0].click();

}


function step3(identifier){
    game=identifier;
    console.log(identifier)
    
    buttons[2].click();
    close[1].click();
}
// disable options step3
$(document).ready(function(){

    var type = document.getElementById("id_type");
    for (var i = 4; i<type.options.length ; i++){
	type.options[i].setAttribute("disabled","True");
    }
    
});

function step4(type){

  //   node = {id: ++lastNodeId,
//             type : type,
//             linput:1,
// 	    weight:-1,
// 	    reward:-1,
// 	    punishement:-1,
// 	    inner_sizes:[],
// 	    l:1,
// 	    c:2
// 	   }
//     circles.push(node);
//     links = [
// 	 {source: circles[0], target: circles[2]},
// 	 {source: circles[2], target: circles[1]},
// ]
//     restart();
    buttons[3].click();
    close[2].click();
}

function step5(){
    buttons[4].click();
    close[3].click();
}

function finish_tutorial(){
    //ajax call server

}
