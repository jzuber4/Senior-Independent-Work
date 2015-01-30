class @Tree
    constructor: (@divId, data, @click) ->
        @duration = 750
        @i = 0

        # create the space containing the tree
        @margin = {top: 50, right: 50, left: 50, bottom: 50}
        @width  = $("##{@divId}").width() - @margin.left - @margin.right
        @height = @width - @margin.top - @margin.bottom

        @tree = d3.layout.tree()
            .size([@height, @width])

        @diagonal = d3.svg.diagonal()
            .projection((d) -> [d.x, d.y])

        @svg = d3.select("##{@divId}").append("svg")
            .attr("width", @width + @margin.right + @margin.left)
            .attr("height", @height + @margin.top + @margin.bottom)
          .append("g")
            .attr("transform", "translate(#{@margin.left},#{@margin.top})")

        # make tree
        @root = data
        @root.x0 = @width / 2
        @root.y0 = 0
        @update @root

    update: (source) ->
        # compute the new tree layout
        nodes = @tree.nodes(@root).reverse()
        links = @tree.links(nodes)

        # adjust the tree to fit
        maxdepth = d3.max(nodes, (n) -> n.depth)
        nodes.forEach((d) => d.y = d.depth * .5 * (@height / maxdepth))

        # update the nodes
        node = @svg.selectAll("g.node")
            .data(nodes, (d) => (d.id || d.id = ++@i))

        # Enter any new nodes at the parent's previous position
        nodeEnter = node.enter().append("g")
            .attr("class", (d) -> if d.name? then "node" else "node invalid")
            .attr("transform", (d) -> "translate(#{source.x0},#{source.y0})")
            .on("click", @click)

        nodeEnter.append("circle")
            .attr("r", 1e-6)

        nodeEnter.append("text")
            .attr("text-anchor", "middle")
            .attr("y", 4)
            .text((d) -> d.name)
            .style("fill-opacity", 1e-6)

        # Transition nodes to their new position
        nodeUpdate = node.transition()
            .duration(@duration)
            .attr("transform", (d) -> "translate(#{d.x},#{d.y})")

        nodeUpdate.select("circle")
            .attr("r", 20)

        nodeUpdate.select("text")
            .style("fill-opacity", 1)

        # Transition exiting nodes to the parent's new position
        nodeExit = node.exit().transition()
            .duration(@duration)
            .attr("transform", "translate(#{source.x},#{source.y})")
            .remove()

        nodeExit.select("circle")
            .attr("r", 1e-6)

        nodeExit.select("text")
            .style("fill-opacity", 1e-6)

        # update the links
        link = @svg.selectAll("path.link")
            .data(links, (d) -> d.target.id)

        # Enter any new links at the parents previous position
        link.enter().insert("path", "g")
            .attr("class", "link")
            .attr("d", (d) =>
                o = {x: source.x0, y: source.y0}
                @diagonal({source: o, target: o})
            )

        # Transition links to their new position.
        link.transition()
            .duration(@duration)
            .attr("d", @diagonal)

        # Transition exiting nodes to the parent's new position
        link.exit().transition()
            .duration(@duration)
            .attr("d", (d) =>
                o = {x: source.x, y: source.y}
                @diagonal({source: o, target: o})
            )
            .remove()

        # Stash the old positions for transition
        nodes.forEach((d) ->
            d.x0 = d.x
            d.y0 = d.y
        )












