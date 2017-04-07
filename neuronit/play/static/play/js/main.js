
// global var used by graph
var weight // form: {name : "weight", value: "x" }
var victory
var defeat
var type
var result= {};



//TODO: ReferenceError in console.log, unknown error
$(document).ready(function(){
    
    $( "form" ).submit(function( event ) {

	 $.each($( this ).serializeArray(),function(){
	     result[this.name] = this.value;
	     
	 });

	var modifyParam=document.getElementById("modifyParam");
	modifyParam.setAttribute("value","Done !");
	
	// update selected node with parameters
	update_f(result);
	console.log(result);
	
	event.preventDefault(); // no refresh
	// send data as if it was a regular submit
	$.ajax({
	    url: '/play/',
	    type: "POST",
	    data: $(this).serializeArray(),
	    dataType: 'json',
	    success: function(data){


	    },
	    error: function(data){
		
	    }

	    
	});

	setTimeout(function(){
	    modifyParam.setAttribute("value","Modify");
	},2000);

    });
});




$(document).ready(function(){

//<!-- change info on network onclick -->
var element = document.getElementById("id_type");
element.addEventListener('change',function(){
var tmp=document.getElementById(element.options[element.selectedIndex].innerHTML); <!-- get span id {{reseau_info}} -->
var network_info=document.getElementById("network_info");

network_info.innerHTML=tmp.getAttribute("info");

});


var hidden_layers = document.getElementById("id_network_layers");

//<!-- only allow a form of input -->


var allowed_length=1;
hidden_layers.addEventListener('keypress',function(evt){

//<!-- do not allow anything if caret isn't at the end -->
if (evt.target.selectionStart != evt.target.value.length){
evt.preventDefault();


}

//<!-- do proper backspace : condition with "," for hidden_layers-->

if( evt.keyCode == 8 && allowed_length > 1){

   allowed_length = allowed_length - 1;
   console.log(allowed_length);
   //evt.target.value= evt.target.value.substr(0,evt.target.value.length -1);

}

//<!-- allow number and backspace -->
if ( evt.target.value.length >= allowed_length && evt.keyCode != 8){
evt.preventDefault();
}

if (( evt.charCode < 49 || evt.charCode >= 58) && evt.keyCode != 8){
    evt.preventDefault();

    }   
    
});

hidden_layers.addEventListener('keyup',function(evt){
  var max_length = 16;




 //<!-- allowed_length condition here : no print "," --> 
  if (evt.target.value.length < max_length && evt.keyCode != 8 && evt.target.value.length == allowed_length ){	
	allowed_length = allowed_length + 2;

				
	evt.target.value=evt.target.value + ",";			
}

  

});

//<!-- put caret at the end -->
hidden_layers.addEventListener('click',function(evt){
  console.log(evt.target.selectionStart);
  evt.target.selectionStart=evt.target.value.length;

});


});

// initialize popover
$(document).ready(function(){
  $('[data-toggle="popover"]').popover()

 
});

// depending on types, hide some parameters
$(document).ready(function(){

    var type = document.getElementById("id_type");
    tmp=[];
    tmp[0]=document.getElementById("id_weight");
    tmp[1]=document.getElementById("id_victory");
    tmp[2]=document.getElementById("id_defeat");
    tmp[3]=document.getElementById("id_network_layers");

    var fieldform = document.getElementsByClassName("fieldform");

    // TODO BETTER, get hidden layers and modify its name and help text if is decomposite
    var buttons= document.getElementsByTagName("button");
    var tmptext= buttons[6].getAttribute("data-content");
    // TODO BETTER

    
    for ( var i = 0 ; i< tmp.length ; i++){
	
	tmp[i].setAttribute("disabled","True");

	
    }
	    // hide input except type
    for ( var i = 1 ; i< fieldform.length ; i++){   
	
	
	fieldform[i].setAttribute("hidden","True");

    }	    


    type.addEventListener('change',function(evt){
	var value_type=evt.target.value;
	console.log(value_type);

	
	if(value_type != "mlp" && value_type != "elman" && value_type != "jordan" && value_type != "op_decomp"){
	    
	    
	    //disable input
	    for ( var i = 0 ; i< tmp.length ; i++){

		tmp[i].setAttribute("disabled","True");

	    }
	    // hide input except type
	    for ( var i = 1 ; i< fieldform.length ; i++){   
		

		fieldform[i].setAttribute("hidden","True");
	    }
	}

	else {
	    // enable input 
	    for ( var i = 0 ; i< tmp.length ; i++){
		
		tmp[i].removeAttribute("disabled");
	    }


	    for ( var i = 1 ; i< fieldform.length ; i++){   
		
		fieldform[i].removeAttribute("hidden");
	    }
	    
	}

	if (value_type == "op_decomp"){

	    for ( var i = 0 ; i< tmp.length-1 ; i++){

                tmp[i].setAttribute("disabled","True");

            }
            // hide input except type
            for ( var i = 1 ; i< fieldform.length-1 ; i++){


                fieldform[i].setAttribute("hidden","True");
            }

	    $('label[for=id_network_layers]').html('Decomposite:');

	    
	    buttons[6].setAttribute("data-content","Decomposite into *,*,...,* vector"); // TODO BETTER
	    console.log(buttons);
	    
        }
	else {
	    $('label[for=id_network_layers]').html('Hidden Layers:');
	    buttons[6].setAttribute("data-content",tmptext); //TODO BETTER
	}


    
	
	
    
	

	
});

});
