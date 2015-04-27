// http://bost.ocks.org/mike/chart/
function histogramChart(config) {
    var margin = {top: 20, right: 20, bottom: 50, left: 50},
        width = null,
        useDivWidth = true,
        height = null,
        useDivHeight = true,
        numBins = 10,
        xMax = null,
        xMin = null,
        duration = 0,
        transition = "linear",
        barPadding =  2,
        xLabel = "Value",
        yLabel = "Frequency",
        xScale = d3.scale.linear(),
        yScale = d3.scale.linear(),
        xAxis = d3.svg.axis().scale(xScale).orient("bottom").tickSize(6, 0),
        yAxis = d3.svg.axis().scale(yScale).orient("left");

    if (config) {
        if (config.margin)     margin     = config.margin;
        if (config.width) {
            width = config.width;
            useDivWidth = false;
        }
        if (config.height) {
            height = config.height;
            useDivHeight = false;
        }
        if (config.numBins)    numBins    = config.numBins;
        if (config.xMin)       xMin       = config.xMin;
        if (config.xMax)       xMax       = config.xMax;
        if (config.transition) transition = config.transition;
        if (config.duration)   duration   = config.duration;
        if (config.barPadding) barPadding = config.barPadding;
        if (config.xLabel)     xLabel     = config.xLabel;
        if (config.yLabel)     yLabel     = config.yLabel;
        if (config.xScale)     xScale     = config.xScale;
        if (config.yScale)     yScale     = config.yScale;
        if (config.xAxis)      xAxis      = config.xAxis;
        if (config.yAxis)      yAxis      = config.yAxis;
    }

    function chart(selection) {
        // generate chart here
        selection.each(function(data) {
            var max = xMax !== null ? xMax : d3.max(data),
                min = xMin !== null ? xMin : d3.min(data);

            var data = d3.layout.histogram()
                .range([min, max])
                .bins(numBins)(data);
            
            divWidth = d3.select(this).node().getBoundingClientRect().width;
            if (useDivWidth) {
                width = divWidth - margin.left - margin.right; 
            } 
            if (useDivHeight) {
                height = divWidth / 3 - margin.top - margin.bottom; 
            }

            // Update the x-scale.
            xScale
                .domain([min, max])
                .range([0, width]);

            // Update the y-scale.
            yScale
                .domain([0, d3.max(data, function(d) { return d.y; })])
                .range([height, 0]);

            // Select the svg element, if it exists.
            var svg = d3.select(this).selectAll("svg").data([data]);

            // Otherwise, create the skeletal chart.
            var gEnter = svg.enter().append("svg").append("g");
            gEnter.append("g").attr("class", "x axis")
                .append("text")
                    .attr("x", margin.left / 3)
                    .attr("y", margin.bottom / 2)
                    .attr("dy", ".71em")
                    .style("text-anchor", "end")
                    .text(xLabel); 
            gEnter.append("g").attr("class", "y axis") 
                .append("text")
                    .attr("transform", "rotate(-90)")
                    .attr("y", 6)
                    .attr("dy", ".71em")
                    .style("text-anchor", "end")
                    .text(yLabel); 

                // Update the outer dimensions.
            svg .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom);

            // Update the inner dimensions.
            var g = svg.select("g")
                    .attr("transform", "translate(" + margin.left + "," + margin.top + ")")

            var bar = g.selectAll(".bar")
                    .data(data)

            var barEnter = bar.enter().append("g")
                .attr("class", "bar")
                .attr("transform", "translate("+xScale.range()[1]+","+yScale.range()[0]+")")

            barEnter.append("rect")
                .attr("height", 0)
                .attr("width", xScale(data[0].dx) - barPadding);

            barEnter.append("text")
                .attr("dy", ".75em")
                .attr("y", -10)
                .attr("x", xScale(data[0].dx) / 2)
                .attr("text-anchor", "middle")
                .text(function(d) { return d.y; });

            // Update the bars 
            var barUpdate = bar.transition(transition).duration(duration)
                .attr("transform", function(d) {
                    return "translate("+xScale(d.x)+","+yScale(d.y)+")";
                });

            barUpdate.select("rect")
                .attr("height", function(d) { return height - yScale(d.y);})
                .attr("width", xScale(data[0].dx) - barPadding);
            barUpdate.select("text")
                .attr("x", xScale(data[0].dx) / 2)
                .attr("text-anchor", "middle")
                .text(function(d) { return d.y; });

            var barExit = bar.exit().transition(transition).remove().duration(duration)
                .attr("transform", "translate("+xScale.range()[1]+","+yScale.range()[0]+")");

            barExit.select("rect")
                .attr("height", 0)
                .attr("width", xScale(data[0].dx) - barPadding);

            // Update the x-axis.
            g.select(".x.axis")
                .attr("transform", "translate(0," + yScale.range()[0] + ")")
                .call(xAxis).transition(transition).duration(duration)

            // Update the y-axis.
            g.select(".y.axis").transition(transition).duration(duration)
                .attr("transform", "translate("+ (-margin.left / 3) +",0)")
                .call(yAxis);

        });
    }   

    chart.margin = function(_) {
        if (!arguments.length) return margin;
        margin = _;
        return chart;
    };

    chart.width = function(_) {
        if (!arguments.length) return width;
        if (_) useDivWidth = false;
        width = _;
        return chart;
    };

    chart.height = function(_) {
        if (!arguments.length) return height;
        if (_) useDivHeight = false;
        height = _;
        return chart;
    };

    chart.numBins = function(_) {
        if (!arguments.length) return numBins;
        numBins = _;
        return chart;
    }

    chart.xMin = function(_) {
        if (!arguments.length) return xMin;
        xMin = _;
        return chart;
    }

    chart.xMax = function(_) {
        if (!arguments.length) return xMax;
        xMax = _;
        return chart;
    }

    chart.duration = function(_) {
        if (!arguments.length) return duration;
        duration = _;
        return chart;
    }

    chart.transition = function(_) {
        if (!arguments.length) return transition;
        transition = _;
        return chart;
    }

    chart.barPadding = function(_) {
        if (!arguments.length) return barPadding;
        barPadding = _;
        return chart;
    }

    chart.xLabel = function(_) {
        if (!arguments.length) return xLabel;
        xLabel = _;
        return chart;
    }   

    chart.yLabel = function(_) {
        if (!arguments.length) return yLabel;
        yLabel = _;
        return chart;
    }
    
    return chart; 
}
