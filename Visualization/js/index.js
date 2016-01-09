


			d3.csv("data/donation-sum.csv", function(data){

				var y = d3.scale.linear().domain([0, 40]).range([200, 0]);
				var x = d3.scale.ordinal().rangeRoundBands([0, 880], 0.2).domain( data.map(function(d){return d.Institution;}) );

				var yAxis = d3.svg.axis().scale(y).orient("left");

				var svg = d3.select("#svg").append("g")
					.attr("id", "bars-g")
					.attr("transform", function(d){
						return "translate(" + 30 + ",10)";
					});

				d3.select("svg").append("g")
					.attr("class", "y axis")
					.attr("transform", "translate(30,10)")
					.call(yAxis)
					.append("text")
				    // .attr("transform", "rotate(-90)")
				    .attr("y", 220)
				    .attr("dy", ".71em")
				    .style("text-anchor", "end")
				    .text("(%)");;

				var institutions = svg.selectAll(".institution")
						.data(data).enter()
					  .append("g")
					  	.attr("class", "institution");

				var institutionTip = d3.tip().attr("class", "institution-tip").html(function(d){
					return '<div class="tip-wrap">\
								<div class="intitution-name">Institution Name:<br>' + d["Institution"] + '</div>\
								<div class="crossgiving-percentage"> Percentage of cross-giving:<br>' + parseInt( parseFloat(d["Percentage"].trim() ) * 100) + '%</div>\
							</div>';
				});

				svg.call(institutionTip);

				institutions.append("rect")
					.attr("width", x.rangeBand() )
					.attr("height", function(d){
						return 200 - y( parseFloat(d["Percentage"].trim()) * 100 );
					})
					.style("fill", "rgb(46,132,133)")
					.style("stroke-width", 1)
					.on("mouseover", function(d){
						d3.select(this)
							.style("stroke-width", 3)
							.style("stroke", "rgb(102,22,18)");

						institutionTip.show(d);

						// console.log( d3.select(this).node().parentNode );
						d3.select( d3.select(this).node().parentNode ).select("text")
							.style("stroke", "rgb(102,22,18)").style("stroke-width", 1)
							.style("fill", "black");

					})
					.on("mouseout", function(d){
						d3.select(this)
							.style("stroke-width", 1)
							.style("stroke", "#333");

						institutionTip.hide(d);

						d3.select( d3.select(this).node().parentNode ).select("text")
							.style("stroke", "black").style("stroke-width", 0)
							.style("fill", "black");

					});

				institutions.append("text")
					.text(function(d){
						return d["Intitution_abrev"];
					})
					.attr("x", function(d){
						return x.rangeBand()/2;
					})
					.attr("y", function(d){
						return 200 - y( parseFloat(d["Percentage"].trim()) * 100 ) + 20 + ( (parseInt(d.rank) + 1)%2) * 15;
					})
					.style("font-size", 9)
					.style("text-anchor", "middle");

				institutions.attr("transform", function(d){
						return "translate(" + x( d.Institution ) + "," + y( parseFloat(d["Percentage"].trim()) * 100 ) + ")";
					});
			
			});



// chord Diagram 


var width = 720,
    height = 720,
    outerRadius = Math.min(width, height) / 2 - 10,
    innerRadius = outerRadius - 24;

var formatPercent = d3.format(".1%");

var arc = d3.svg.arc()
    .innerRadius(innerRadius)
    .outerRadius(outerRadius);

var layout = d3.layout.chord()
    .padding(.04)
    .sortSubgroups(d3.descending)
    .sortChords(d3.ascending);

var path = d3.svg.chord()
    .radius(innerRadius);

console.log(d3.select("#chord-svg"));



var chord_svg = d3.select("body").select("#chord-svg")
    .attr("width", width)
    .attr("height", height)
  .append("g")
    .attr("id", "circle")
    .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

chord_svg.append("circle")
    .attr("r", outerRadius);

queue()
    .defer(d3.csv, "cities.csv")
    .defer(d3.json, "matrix.json")
    .await(ready);

function ready(error, cities, matrix) {
  if (error) throw error;

  // Compute the chord layout.
  layout.matrix(matrix);

  function mouseover(d, i) {
    chord.classed("fade", function(p) {
      return p.source.index != i
          && p.target.index != i;
    });
  }

  // Add a group per neighborhood.
  var group = chord_svg.selectAll(".group")
      .data(layout.groups)
    .enter().append("g")
      .attr("class", "group");


  // Add a mouseover title.
  // group.append("title").text(function(d, i) {
  //   return cities[i].name + ": " + formatPercent(d.value) + " of origins";
  // });

  var chordInstitutionNameTip = d3.tip().attr("id", "chord-name-tip").html(function(d, i){

  	var institution_name = cities[parseInt(d["index"])].name;
  	return '<div class="tip-wrap">\
  		<div>' + institution_name + ": " + formatPercent(d.value) + ' of all cross-donations</div>\
  	</div>';
  });


  chord_svg.call(chordInstitutionNameTip);

  group.on("mouseover", function(d,i){
      	mouseover(d,i);
      	chordInstitutionNameTip.show(d);	
      })
  .on("mouseout", function(d){
  	chordInstitutionNameTip.hide(d);
  });


  // Add the group arc.
  var groupPath = group.append("path")
      .attr("id", function(d, i) { return "group" + i; })
      .attr("d", arc)
      .style("fill", function(d, i) { return cities[i].color; });

  // Add a text label.
  var groupText = group.append("text")
      .attr("x", 6)
      .attr("dy", 15);

  groupText.append("textPath")
      .attr("xlink:href", function(d, i) { return "#group" + i; })
      .text(function(d, i) { return cities[i].name; });

  // Remove the labels that don't fit. :(
  groupText.filter(function(d, i) { return groupPath[0][i].getTotalLength() / 2 - 16 < this.getComputedTextLength(); })
      .remove();

  // Add the chords.
  var chord = chord_svg.selectAll(".chord")
      .data(layout.chords)
    .enter().append("path")
      .attr("class", "chord")
      .style("fill", function(d) { 

      	if( parseFloat(formatPercent(d.source.value)) > 0 && parseFloat(formatPercent(d.target.value)) > 0 ){
      		return cities[d.source.index].color;	
      	}else{
      		// return "#d3d3d3";
      		return "rgba(211,211,211,0.3)";
      	}
      })
      	
      // .style("fill", function(d){
      // 	return "red";
      // })
      .attr("d", path);


  var chord_tip = d3.tip().attr("id", "chord-tip-wrap").html(function(d){

  	return '<div class="tip-wrap">\
  				<div>' + cities[d.target.index].name + " → " + cities[d.source.index].name + ": " + formatPercent(d.source.value) + '</div>\
  				<div>' + cities[d.source.index].name + " → " + cities[d.target.index].name + ": " + formatPercent(d.target.value) + '</div>\
  			</div>';

  });

  chord_svg.call(chord_tip);

  // Add an elaborate mouseover title for each chord.
  // chord.append("title").text(function(d) {
  //   return cities[d.target.index].name
  //       + " → " + cities[d.source.index].name
  //       + ": " + formatPercent(d.source.value)
  //       + "\n" + cities[d.source.index].name
  //       + " → " + cities[d.target.index].name
  //       + ": " + formatPercent(d.target.value);
  // });

  chord
  .on("mouseover", function(d){
  	chord_tip.show(d);
  })
  .on("mouseout", function(d){
  	chord_tip.hide(d);
  })

  
}



