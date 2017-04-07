<!-- svg js  -->
var width = 795,
    height = 500;

var svg = d3.select("svg")
radius = 20;

var nb_column = 5;
var nb_line = 5;

var x_array = Array.apply(null, {length: nb_column + 2}).map(Number.call, Number)
var y_array = Array.apply(null, {length: nb_line}).map(Number.call, Number)

var x = d3.scale.ordinal().domain(x_array).rangePoints([0, width])
var y = d3.scale.ordinal().domain(y_array).rangePoints([height, 0])

var x_axis = d3.svg.axis()
    .scale(x)
    .orient("bottom")
    .innerTickSize(-height)
    .outerTickSize(0)

var y_axis = d3.svg.axis()
    .scale(y)
    .orient("left")
    .innerTickSize(-width)
    .outerTickSize(0)

svg.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + height + ")")
    .call(x_axis)

svg.append("g")
    .attr("class", "y axis")
    .call(y_axis)


var lastNodeId = 1
var node_class = null;
var circles = d3.range(3).map(function (id) {
    return {
	id: id,
        l: Math.round(nb_line/2)-1,
        c: id+1,
	x: x(id+1),
	y: y(Math.round(nb_line/2)-1),
	type : "in",
	linput: 0, // limit of inputs for "in" 
	weight:-1,
	reward:-1,
	punishement:-1,
	inner_sizes:[]


};
});

circles[1].type = "mlp";
circles[2].id= -1;
circles[2].x = x(nb_column);
circles[2].c = nb_column;
circles[2].type = "out";


var links = [
    {source: circles[0], target: circles[1]}
]

function hide_disable(){

    var type = document.getElementById("id_type");
    tmp=[];
    tmp[0]=document.getElementById("id_weight");
    tmp[1]=document.getElementById("id_victory");
    tmp[2]=document.getElementById("id_defeat");
    tmp[3]=document.getElementById("id_network_layers");

    var fieldform = document.getElementsByClassName("fieldform");
    if(selected_node.type != "mlp" && selected_node.type != "elman" && selected_node.type != "jordan"){

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
	
    }

    for ( var i = 1 ; i< fieldform.length ; i++){   
	
	fieldform[i].removeAttribute("hidden");
    }
    
}





function update_f(d){
    obj = d;
    node = selected_node;
    var trans = {weight:"weight", victory:"reward", defeat:"punishement"};
    if (node && node.type != "in" && node.type != "out"){
	for (var key in obj){
	    test2 = obj
	    if (obj[key] != ""){   
		if (key == "type"){
		    circles[circles.indexOf(node)][key] = obj[key];
		}
		if (key == "weight" || key != "victory" || key != "defeat"){
		    circles[circles.indexOf(selected_node)][trans[key]] = parseFloat(obj[key]);
		}
		if  (key == "network_layers"){
		    array_test =  obj[key].split(",");
		    var array = obj[key].split(",")
		    if (array[array.length-1] == "")
			array.pop();
		    array.map(function(d) {return parseInt(d);});
		    array_test = array;
		    circles[circles.indexOf(selected_node)]["inner_sizes"] = array;
		}
	    }
	}
    }
    nb_epochs =  parseInt(d.epochs);
    nb_simulations = parseInt(d.simulations);
    selected_node =  circles[circles.indexOf(selected_node)];
    restart();
}

function add_column() {
    nb_column = nb_column + 1;
    reset_axis();
    circles.forEach(function (d) {
        if (d.id == -1) {
            d.c = d.c + 1;
        }
    });
    edges = links.filter(function(l) {
	return (l.target.id == -1);})
    edges.map(function(l) {
	links.splice(links.indexOf(l), 1);
    });
    restart();
}

function add_line() {
    nb_line = nb_line + 1;
    reset_axis();
    restart();
}


function remove_column() {
    if (nb_column > 2) {
        nb_column = nb_column - 1;
        reset_axis();

        circle_to_remove = circles.filter(function (d) {
            return (d.c == nb_column);
        });


        circle_to_remove.map(function (c) {
            circles.splice(circles.indexOf(c), 1);
        });

        circle_to_remove.forEach(function (d) {
            edges = links.filter(function (l) {
                return (l.source == d || l.target == d);
            })
            edges.map(function (l) {
                links.splice(links.indexOf(l), 1);
            });
        })

        circles.forEach(function (d) {
            if (d.id == -1) {
                d.c = d.c - 1;
            }
        });
        restart();
    }
}

function remove_line() {
    if (nb_line > 4) {
        nb_line = nb_line - 1;
        reset_axis();

        circle_to_remove = circles.filter(function (d) {
            return (d.l == nb_line - 1);
        });

        circle_to_remove.map(function (c) {
            circles.splice(circles.indexOf(c), 1);
        });
        bla = circle_to_remove;
        circle_to_remove.forEach(function (d) {
            edges = links.filter(function (l) {
                return (l.source == d || l.target == d);
            })
            edges.map(function (l) {
                links.splice(links.indexOf(l), 1);
            });
        })
        restart();
    }
}

function reset_axis() {
    x_array = Array.apply(null, {length: nb_column + 2}).map(Number.call, Number)
    y_array = Array.apply(null, {length: nb_line}).map(Number.call, Number)
    x = d3.scale.ordinal().domain(x_array).rangePoints([0, width])
    y = d3.scale.ordinal().domain(y_array).rangePoints([height, 0])
    x_axis = d3.svg.axis()
        .scale(x)
        .orient("bottom")
        .innerTickSize(-height)
        .outerTickSize(0)
    y_axis = d3.svg.axis()
        .scale(y)
        .orient("left")
        .innerTickSize(-width)
        .outerTickSize(0)

    svg.select(".x.axis").call(x_axis);
    svg.select(".y.axis").call(y_axis);

}


// define arrow markers for graph links
svg.append('svg:defs').append('svg:marker')
    .attr('id', 'end-arrow')
    .attr('viewBox', '0 -5 10 10')
    .attr('refX', 26)
    .attr('markerWidth', 3)
    .attr('markerHeight', 3)
    .attr('orient', 'auto')
    .append('svg:path')
    .attr('d', 'M0,-5L10,0L0,5')
    .attr('fill', '#000');


var path = svg.append('svg:g').selectAll('path'),
    circle = svg.append('svg:g').selectAll('g');

var mouseon_node = null,
    selected_node = null,
    mouseon_edge = null,
    selected_edge = null;
var selected_node_1 = null,
    selected_node_2 = null;


function reset_var() {
    mouseon_node = null;
    selected_node = null;
    mouseon_edge = null;
    selected_edge = null;
    selected_node_1 = null;
    selected_node_2 = null;
}


function restart() {

    path = path.data(links);

    path.style('marker-end', 'url(#end-arrow)')
        .attr("d", function (d) {
            return 'M' + x(d.source.c) + ',' + y(nb_line - 1 - d.source.l) + 'L' + x(d.target.c) + ',' + y(nb_line - 1 - d.target.l);
        });

    path.enter().append('svg:path')
        .attr('class', 'link')
        .style('marker-end', 'url(#end-arrow)')
        .classed('link', true)
        .attr('d', function (d) {
            return 'M' + x(d.source.c) + ',' + y(nb_line - 1 - d.source.l) + 'L' + x(d.target.c) + ',' + y(nb_line - 1 - d.target.l);
        })
        .on("mouseover", function (d) {
            mouseon_edge = d;
            svg.classed("over", true);
        })
        .on("mouseout", function () {
            mouseon_edge = null;
            svg.classed("over", false);
        })
        .on("mousedown", function (d) {
	    selected_edge = d;
            if (selected_edge && delete_edge) {
                links.splice(links.indexOf(selected_edge), 1);
                selected_edge = null;
                restart();

            }
        });

    path.exit().remove();
    circles.forEach(function(d){
	if ( d.type == "mlp" || d.type == "out" || d.type == "elman" || d.type == "jordan" || d.type == "decomp" || d.type == "tempo")
	    d.linput = 1;
	if ( d.type == "minus" || d.type == "divide")
	    d.linput = 2;
        if ( d.type == "in")
	    d.linput = 0;
        if ( d.type == "avg" || d.type == "mult" ||  d.type == "plus" || d.type == "recomp")
	    d.linput = nb_line;
    });

    circle = circle.data(circles, function (d) {
        return d.id;
    });
    circle.selectAll('circle')
        .attr("cx", function(d) {return x(d.c);})   
        .attr("cy", function(d) {return y(nb_line -d.l-1);})     
         .style("fill", function(d) {
            if ( d.type == "mlp")
		return "url(#mlp)";
            if ( d.type == "in")
		return "url(#in)";
	    if ( d.type == "out")
		return "url(#out)";
            if ( d.type == "elman")
		return "url(#elman)";
            if ( d.type == "jordan")
		return "url(#jordan)";
            if ( d.type == "op_avg")
		return "url(#avg)";
	    if ( d.type == "op_decomp")
		return "url(#decomp)";
            if ( d.type == "op_minus")
		return "url(#minus)";
            if ( d.type == "op_mult")
		return "url(#mult)";
	    if ( d.type == "op_divide")
		return "url(#divide)";
	     if ( d.type == "op_plus")
		return "url(#plus)";
            if ( d.type == "op_recomp")
		return "url(#recomp)";
            if ( d.type == "op_tempo")
		return "url(#tempo)";
            return "url(#mlp)";
	})
    var container = circle.enter().append('svg:g');
    container.append("svg:circle")
	.attr("cx", function(d) {return x(d.c);})
        .attr("cy", function(d) {return y(nb_line -d.l-1); })
	.attr("r", radius)
        .style("fill", function(d) {
            if ( d.type == "mlp"){
		return "url(#mlp)";
	    }
            if ( d.type == "in"){
		return "url(#in)";
	    }        
	    if ( d.type == "out"){
		return "url(#out)";
	    }
            if ( d.type == "elman"){
		return "url(#elman)";
	    }
            if ( d.type == "jordan"){
		return "url(#jordan)";
	    }
            if ( d.type == "op_avg"){
		return "url(#avg)";
	    }            
	    if ( d.type == "op_decomp"){
		return "url(#decomp)";
	    }
            if ( d.type == "op_minus"){
		return "url(#minus)";
	    }
            if ( d.type == "op_mult"){
		return "url(#mult)";
            }
	    if ( d.type == "op_divide"){
		return "url(#divide)";
            }
	    if ( d.type == "op_plus"){
		return "url(#plus)";
	    }
            if ( d.type == "op_recomp"){
		return "url(#recomp)";
	    }
            if ( d.type == "op_tempo"){
		return "url(#tempo)";
	    }
            return "url(#mlp)";
        })
        .classed("over", false)
        .classed("circles", true)
        .classed("active", false)
        .on("mouseover", function (d) {
            mouseon_node = d;
            svg.classed("over", true);
        })
        .on("mouseout", function () {
            mouseon_node = null;
            svg.classed("over", false);
        })
        .on("mousedown", function (d) {
	    if (node_class)
		d3.select(node_class).classed("active", false);
            selected_node = d;
	    node_class = this;
	     d3.select(node_class).classed("active", true);
	    update_param(d);
	    
	    hide_disable();
            if (add_edge) {
                if (!selected_node_1) {
                    selected_node_1 = d;
                    return;
                }
                if (selected_node_1 && !selected_node_2 && (d !== selected_node_1)) {
                    selected_node_2 = d;
                    edge_distinct = links.filter(function(l) {
			return (l.source == selected_node_1 && l.target == selected_node_2);})
                    edge_input = links.filter(function(l) {
			return (l.target == selected_node_2);})
                    if ( (edge_distinct.length == 0)  && (selected_node_2.c == selected_node_1.c+1) && ( edge_input.length < selected_node_2.linput )){
			edge = {source : selected_node_1,
				target : selected_node_2}
			
			links.push(edge);
                    }
		    reset_var(); 
                }
		
            }
            if (selected_node && delete_vertex && ( d.id != -1 && d.id != 0) ) {
		circles.splice(circles.indexOf(selected_node),1);
		edges = links.filter(function(l) {
		    return (l.source == selected_node || l.target == selected_node);})
		edges.map(function(l) {
		    links.splice(links.indexOf(l), 1);
		});
		selected_node = null;
		reset_var(); 
	    }
            	    
            restart();

        })
        .on("mouseup", function () {
            if (!selected_node) {
                return;
            }
        })

    circle.exit().remove();
}

function mousedown(d) {
    if (!add_vertex || d3.event.which != 1 || mouseon_node || mouseon_edge) {
        return;
    }
    var point = d3.mouse(this),
    node = {id: ++lastNodeId,
            type : "elman",
            linput:1,
	    weight:-1,
	    reward:-1,
	    punishement:-1,
	    inner_sizes:[]

	   }
    var domain_x = x.domain(); 
    var domain_y = y.domain();
    var c = domain_x[(d3.bisect(x.range(), point[0]) - 1)];
    point_ter = point[0]
    if (c + 1 != nb_column && x(c + 1) + x(c) < 2 * point[0]) {
        c = c + 1;
    }


    l_tbis = d3.bisect(y.range().reverse(), point[1]) - 1;
    var l = domain_y[l_tbis];
    if (l + 1 != nb_line && y(l + 1) + y(l) < 2 * point[1]) {
        l = l + 1;
    }
    y.range().reverse();
    node.c = c;
    node.l = l;
    node_ex = circles.filter(function (d) {
        return (d.c == c && d.l == l)
    })
    if (!node_ex.length && c <= nb_column - 1 && c >= 2 && l != 0 && l != nb_line - 1) {
        circles.push(node);
        reset_var();
        restart();
    }
}

function send_to_backend(){
    var nodes_tmp = new Array;
    var id = 0;
    for (var j = 1; j <= nb_column; j++){
	for (var i = 1; i < nb_line-1; i++){
	    node_array = circles.filter(function(d) {return (d.c == j && d.l == i)})
	    if (node_array.length == 1){
		node_array[0].id = id;
		nodes_tmp.push(node_array[0]);
		id++;
	   }
	} 
    }
    var nodes = nodes_tmp;
    var bObj = new Object;
    bObj.save_frequency = 100,
    bObj.rl_gamma = 0.6,
    bObj.rl_epsilon = 0.05,
    bObj.was_loaded = false;
    bObj.p_types_array = nodes.map(function(d) {return d.type;})
    bObj.p_weights_array = nodes.map(function(d) {return d.weight;})
    bObj.p_rewards_array = nodes.map(function(d) {return d.reward;})
    bObj.p_punishs_array = nodes.map(function(d) {return d.punishement;})
    bObj.p_inner_sizes_array = nodes.map(function(d) {return d.inner_sizes;})
    bObj.p_links_array = nodes.map(
	function(d)  
	    { var succ = links.filter(function(l) { return l.source.id == d.id })
	      return succ.map(function (d) {return d.target.id;});
});							 
    bObj.nb_epochs = nb_epochs
    bObj.nb_simulations = nb_simulations
    bObj.user_name = user_name;
    bObj.game_name = game_name;
    bObj.game_observation_size = game_observation_size;
    bObj.game_decision_size = game_decision_size;
    bObj.max_score = max_score
    return bObj
}

svg.on('mousedown', mousedown)


var user_name =  "toto";
var game_name =   "CartPole-v0";
var game_observation_size =  4;
var game_decision_size =  1;
var max_score =  200;
var nb_epochs =  10;
var nb_simulations = 10;

function start(){
    var epochs=document.getElementById("id_epochs");
    var simulations=document.getElementById("id_simulations");    
    epochs.value = nb_epochs;
    simulations.value = nb_simulations;
    restart();
}

start();
