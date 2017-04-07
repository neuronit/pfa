// fill form with selected node parameters

var test_hidden;
function update_param(node){ 
    var type=document.getElementById("id_type");
    var weight=document.getElementById("id_weight");
    var victory=document.getElementById("id_victory");
    var defeat=document.getElementById("id_defeat");
    var hidden_layers=document.getElementById("id_network_layers");
    
    type.value = node.type;
    if ( node.type == "mlp" || node.type == "elman" || node.type == "jordan"){
	weight.value = node.weight;
	victory.value = node.reward;
	defeat.value = node.punishement;
	hidden_layers.value = node.inner_sizes.toString();
}
    if ( node.type == "in" || node.type == "out")  {
	type.value = "select_type" ;	
    }
}
