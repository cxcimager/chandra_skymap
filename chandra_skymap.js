/** Chandra Skymap: Visualizing the X-ray Universe
 *  NAME: chandra_skymap.js
 *  Purpose: a javascript program that generates the skymap and associated control and filtering tools. 
 *
 *  LICENSE: Copyright (C) 2013 - 
 *   NASA/Smithsonian Astrophysical Observatory/Chandra X-ray Center/Joseph DePasquale

 *   This program is free software; you can redistribute it and/or 
 *   modify it under the terms of version 2 of the GNU General
 *   Public License as published by the Free Software Foundation. 

 *   This program is distributed in the hope that it will be useful,
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *   GNU General Public License for more details.

 *   You should have received a copy of the GNU General Public License
 *   along with this program; if not, write to the Free Software
 *   Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

**/

//main skymap generator
var margin = {top: 0, right: 0, bottom: 0, left: 0},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom,

    extent0=0,
    extent1=0,
    currentZoom = 1,
    flag = 0,
    check = 0,
    drawingData,
    processedData,
    rawData,
    projection,
    zoom, 
    div, 
    path, 
    graticule,
    svg,
    g;
    
    colors = [
    "#aa4499", //Nebulas
    "#ee7788", //Galaxies
    "#5566aa", //Stars 
    "#ddcccc", //Misc
    "#db9736"  //Exoplanets
    ];
    circle_size = [
	6,     // LU
	10,    // MW
	4      // EU
    ];

function update() {
    if (check === 0) {
	d3.csv("./cxc_sources.csv", function(error, data) { 
	    rawData = data;
	    processedData = processData(rawData)
	    tempData = cullUnwantedCats(processedData)
	    tempData2 = cullUnwantedDist(tempData)
	    drawingData = cullUnwantedTime(tempData2)
	    tFilt(0)
	    draw();
	    d3.select('#count').html("object count:<span class=obj> " + drawingData.length );
	})
	check = 1;
    } else if (check === 1){
	processedData = processData(rawData)
	tempData = cullUnwantedCats(processedData)
	tempData2 = cullUnwantedDist(tempData)
	drawingData = cullUnwantedTime(tempData2)
	draw();	
	d3.select('#count').html("object count:<span class=obj>  " + drawingData.length );
    }
}

function init() {
    projection = d3.geo.aitoff()
	.scale(width / 2.02 / Math.PI)
	.translate([0,0])
	.precision(.1);

    zoom = d3.behavior.zoom()
	.scaleExtent([1, 50])
	.on("zoom", move);

    div = d3.select("body").append("div")   
	.attr("class", "tooltip")               
	.style("opacity", 0);

    path = d3.geo.path()
	.projection(projection)

    graticule = d3.geo.graticule();

    svg = d3.select("#circles")
	.append("svg:g")
	.attr("transform", "translate(" + width / 2 + "," + height / 2 + ")")
	.call(zoom);

    g = svg.append("g")
    
    g.append("defs").append("path")
	.datum({type: "Sphere"})
	.attr("id", "sphere")
	.attr("d", path)

    g.append("use")
	.attr("class", "stroke")
	.attr("xlink:href", "#sphere");

    g.append("use")
	.attr("class", "fill")
	.attr("xlink:href", "#sphere");

    g.append("path")
	.datum(graticule)
	.attr("class", "graticule")
	.attr("d", path)
	.call(zoom);

    tooltip = d3.select("body")
	.append("div")
	.style("position", "absolute")
	.style("z-index", "10")
	.style("visibility", "hidden")
    
}

function draw(){
 var coordinate = document.querySelector("#coords input:checked").value;
 var points = g.selectAll("circle").data(drawingData, function (d) { return d.id;})
	points.enter()
	.append("a")
	.attr("xlink:href", function(d) {return d.link})
	.attr("xlink:show", "new")
        .insert("svg:circle")
	.attr("cx", function(d) {
	    if (coordinate === "Galactic") { return projection([d.Xgal, d.Ygal])[0];
            } else if (coordinate === "Equatorial") { return projection([d.Xeq, d.Yeq])[0]; }
	})
	.attr("cy", function(d) {
	    if (coordinate === "Galactic") { return projection([d.Xgal, d.Ygal])[1];
            } else if (coordinate === "Equatorial") { return projection([d.Xeq, d.Yeq])[1]; }
	})
        .attr("r", 0)
        .style("fill", function(d) { return d.type.color; })
	      .style("opacity", 0)

    //transition points in
    g.selectAll("circle").transition().duration(800).ease("exp-in-out")
        .attr("r", function(d) { return d.dist.CirSize/currentZoom;})
        .style("fill", function(d) { return d.type.color; })
	.attr("cx", function(d) {
	    if (coordinate === "Galactic") { return projection([d.Xgal, d.Ygal])[0];
            } else if (coordinate === "Equatorial") { return projection([d.Xeq, d.Yeq])[0]; }
	})
	.attr("cy", function(d) {
	    if (coordinate === "Galactic") { return projection([d.Xgal, d.Ygal])[1];
            } else if (coordinate === "Equatorial") { return projection([d.Xeq, d.Yeq])[1]; }
	})
	.style("opacity", 0.7)

    //remove unwanted points
    points.exit()
	.transition().duration(500).ease("exp-in-out")
	.attr("cx", function(d) {
	    if (coordinate === "Galactic") { return projection([d.Xgal, d.Ygal])[0];
	    } else if (coordinate === "Equatorial") { return projection([d.Xeq, d.Yeq])[0]; }
	})
	.attr("cy", function(d) {
	    if (coordinate === "Galactic") { return projection([d.Xgal, d.Ygal])[1];
            } else if (coordinate === "Equatorial") { return projection([d.Xeq, d.Yeq])[1]; }
	})
        .attr("r", 0)
        .style("opacity", 0)
        .remove()

    g.selectAll("circle")
	.on("mouseover", function(d){
	      d3.select(this).style("opacity", 1).style("stroke-opacity", 1).style("stroke", "#fff")
	      div.transition()        
		  .duration(200)      
		  .style("opacity", 1);
	      if (coordinate==="Galactic") {
		  div.html("<b>" + d.source + "</b><br/><br/><i>" + d.title + "</i><br/><br/>" + d.headline + "<br/><br/>" + "<img src=" + d.img + " alt='Image preview' width='150' height='150' /><br/><br/><i>RA: " + d.pRA + " Dec: " + d.pDEC +"<br>Release Date: " + d.date)
		      .style("left", function(x) {
			  var tipX;
			  if (d.Xgal < 100){ tipX = d3.event.pageX + 20;
			  } else { tipX = d3.event.pageX - 250; } 
			  return tipX + "px";})
		      .style("top", function(y) {
			  var tipY;
			  if (d.Ygal > 45) { tipY = d3.event.pageY - 20;
			  } else if (d.Ygal < -25) { tipY = d3.event.pageY - 240;
			  } else { tipY = d3.event.pageY - 95; }
			  return tipY + "px";})
		  
              } else if (coordinate==="Equatorial") {           
		  div.html("<b>" + d.source + "</b><br/><br/><i>" + d.title + "</i><br/><br/>" + d.headline + "<br/><br/>" + "<img src=" + d.img + " alt='Image preview' width='150' height='150' /><br/><br/><i>RA: " + d.pRA + " Dec: " + d.pDEC +"<br>Release Date: " + d.date)
		      .style("left", function(x) {
			  var tipX;
			  if (d.Xeq < 100){ tipX = d3.event.pageX + 20;
			  } else { tipX = d3.event.pageX - 250; } 
			  return tipX + "px";})
		      .style("top", function(y) {
			  var tipY;
			  if (d.Yeq > 45) { tipY = d3.event.pageY - 20;
			  } else if (d.Yeq < -25) { tipY = d3.event.pageY - 240;
			  } else { tipY = d3.event.pageY - 95; }
			  return tipY + "px";}) }
	  })
	  .on("mouseout", function(d) {       
              d3.select(this).style("opacity", 0.7).style("stroke-opacity", 0)
              div.transition()        
		  .duration(500)      
		  .style("opacity", 0);
	  });

      g.append("path")
	  .attr("d", path);
    
};
init();
update();

//MORE FUNCTIONS!//
function processData (data) {
    var processed = [],
    objectTypes = [],
    objectDist = [],
    counter = 1,
    counter2 = 1;
    
    data.forEach (function (data, index) { 
	var object,
	object = {
	    id: index
	};
	for (var attribute in data) {
	    if (data.hasOwnProperty (attribute)) {
		object[attribute] = data[attribute];
	    }
	}
	if (typeof objectTypes[data.Type] == "undefined") { 
	    objectTypes[data.Type] = {
		Type_id: counter -1,
		color: colors[counter-1]
	    };
	    counter = counter+1;
	}
	if (typeof objectDist[data.Dist] == "undefined") { 
	    objectDist[data.Dist] = {
		Dist_id: counter2 -1,
		CirSize: circle_size[counter2-1]
	    };
	    counter2 = counter2 + 1;
	}
	object.type = objectTypes[data.Type];
	object.dist = objectDist[data.Dist];

	processed.push (object);
    });
    return processed;
}


// return a list of types which are currently selected
function plottableCats () {
    var selCat = [].map.call (document.querySelectorAll ("#categories input:checked"), function (checkbox) { return checkbox.value; });
    return selCat;
}
function plottableDist () {
    var selDist = [].map.call (document.querySelectorAll ("#distance input:checked"), function (checkbox) { return checkbox.value; });
    return selDist;
}

// remove categories whose type is not selected from a dataset
function cullUnwantedCats (data) {
	var typesToDisplay = plottableCats();
	return data.filter (function (d) {
	    return typesToDisplay.indexOf(d.Type) !== -1;
	});
}
// remove points whose distance is not selected from a dataset
function cullUnwantedDist (data) {
	var typesToDisplay = plottableDist();
	return data.filter (function (d) {
	    return typesToDisplay.indexOf(d.Dist) !== -1;
	});
}
function cullUnwantedTime (data) {
    if (extent1 != 0){
	return data.filter(function (d) { 
	    return (new Date(d.date) >= extent1[0] && new Date(d.date) <= extent1[1]);
	});
    } else { 
	return data; 
    };
}

//handles zoom/pan
function move() {
    var t = zoom.translate(),
    s = zoom.scale();
    t[0] = Math.min(width / 2 * (s - 1), Math.max(width / 2 * (1 - s), t[0]));
    t[1] = Math.min(height / 2 * (s - 1), Math.max(height / 2 * (1 - s), t[1]));
    zoom.translate(t);
    g.style("stroke-width", 1 / s).attr("transform", "translate(" + t + ")scale(" + s + ")");
    g.selectAll("circle").attr("r", function(d) { return d.dist.CirSize/s; });
    currentZoom = s;
    if (s > 1) {
	d3.selectAll("path").style("cursor", "move");
	d3.select("#recycle path").style("cursor", "default");
    } else if (s = 1) { 
	d3.selectAll("path").style("cursor", "default");
    }
}

// listen to the form fields changing
document.getElementById("categories").addEventListener ("click", update, false);
document.getElementById("distance").addEventListener ("click", update, false);
document.getElementById("coords").addEventListener ("click", draw, false);

// zoom in and out using buttons
/*var svgRootP = document.getElementById('plus').getSVGDocument().documentElement;
d3.select(svgRootP).select("#zplusimg").on('dblclick', function() { 
    zoom.scale(zoom.scale()+(zoom.scale()*zoom.scale())/4)
    if (zoom.scale() > 50) {zoom.scale(50);}
    move();
});
var svgRootM = document.getElementById('minus').getSVGDocument().documentElement;
d3.select(svgRootM).select("#zmin").on('click', function() { 
    zoom.scale(zoom.scale()-zoom.scale()/1.5)
    if (zoom.scale() < 1) {zoom.scale(1);}
    move();
});
*/
// zoom in and out using buttons
// now using transparent full circles because the buttons didn't allow zooming function
//  if you pressed the actual + or -
d3.select("#zplus").on('click', function() {
    zoom.scale(zoom.scale()+(zoom.scale()*zoom.scale())/4)
    if (zoom.scale() > 50) {zoom.scale(50);}
    move();
    document.onselectstart = function() { return false; };
    event.target.ondragstart = function() { return false; };
    //return false;
});
d3.select("#zmin").on('click', function() {
    zoom.scale(zoom.scale()-zoom.scale()/1.5)
    if (zoom.scale() < 1) {zoom.scale(1);}
    move();
    document.onselectstart = function() { return false; };
    event.target.ondragstart = function() { return false; };
    //return false;
});

// reset the map to default view
d3.selectAll("#reset").on('click', function() { 
    document.getElementById("controls").reset();
    zoom.scale(1);
    zoom.translate([0, 0]);
    currentZoom = 1;
    s = 1;
    extent1=0;
    tFilt(1);
    g.transition().duration(650).style("stroke-width", 1 / 1).attr("transform", "translate(" + zoom.translate() + ")scale(" + zoom.scale() + ")");
    update();
    d3.selectAll("path").style("cursor", "default");
    tFilt(1);
});


/// Set up time filter brush
function tFilt(flag) {
    var width=956, 
        height=35;
    var x = d3.time.scale()
	.domain([new Date("1999-01-01"), d3.time.month.round(new Date(drawingData[drawingData.length-1].date))])
	.range([0, width]);

    var brush = d3.svg.brush()
	.x(x)
        .extent(0,0)
	.on("brush", brushed);

    if (flag === 1) {
	brush.clear();
	d3.time.scale().domain([new Date("1999-01-01"), d3.time.month.round(new Date(rawData[rawData.length-1].date))])
    };

    var svg = d3.select("#timeFilt")
	.attr("width", width)
	.attr("height", height)
	.append("g")

    svg.append("rect")
	.attr("class", "grid-background")
	.attr("width", width)
	.attr("height", height);

    svg.append("g")
	.attr("class", "x grid")
	.attr("transform", "translate(1," + 15 + ")")
	.call(d3.svg.axis()
              .scale(x)
              .orient("bottom")
              .ticks(d3.time.years, 1)
              .tickSize(-height)
              .tickFormat(d3.time.format("%Y"))
	      .tickPadding(4))
	.selectAll(".tick")
        .style("fill", "#b5b5b5")
        .style("text-shadow", "1px 1px 1px #000")
	.classed("minor", function(d) { return d.getYear(); });

    svg.append("g")
	.attr("class", "x axis")
	.attr("transform", "translate(0," + height + ")")
	.call(d3.svg.axis()
	      .scale(x)
	      .orient("bottom")
	      .ticks(d3.time.years)
	      .tickPadding(0))
	.selectAll("text")
	.attr("x", 6)
	.style("text-anchor", null)

    var gBrush = svg.append("g")
	.attr("class", "brush")
	.call(brush);
    
    gBrush.selectAll("rect")
	.attr("height", 32);
        
    function brushed() {
	extent0 = brush.extent(),
	extent1 = brush.extent();
	// if dragging, preserve the width of the extent
	if (d3.event.mode === "move") {
	    var d0 = d3.time.month.round(extent0[0]),
            d1 = d3.time.day.offset(d0, Math.round((extent0[1] - extent0[0]) / 864e5));
	    extent1 = [d0, d1];
	}
	
	// otherwise, if resizing, round both dates
	else {
	    extent1 = extent0.map(d3.time.year.round);
	    
	    // if empty when rounded, use floor & ceil instead
	    if (extent1[0] >= extent1[1]) {
		extent1[0] = d3.time.month.floor(extent0[0]);
		extent1[1] = d3.time.month.ceil(extent0[1]);
	    }
	}
	d3.select(this).call(brush.extent(extent1));
	update();
    }
}