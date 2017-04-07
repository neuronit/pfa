<!-- svg js  -->
var width = 795,
    height = 500;

var svg = d3.select("svg")
radius = 20;

var nb_column = 3;
var nb_line = 3;

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
var circle_tst = circles[1]
circles.splice(circles.indexOf(circles[1]),1)
var links = []


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
            restart();

        })
        .on("mouseup", function () {
            if (!selected_node) {
                return;
            }
        })

    circle.exit().remove();
}

function start(){
    restart();
}

start();
