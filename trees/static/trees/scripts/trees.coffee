class @Tree
    constructor: (@divId, data) ->
        @selectedNodes = []
        @duration = 750
        @i = 0
        @nodeClick = (() ->)

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
        do @update

    update: () ->
        # compute the new tree layout
        nodes = @tree.nodes(@root).reverse()
        links = @tree.links(nodes)

        # adjust the tree to fit
        maxdepth = d3.max(nodes, (n) -> n.depth)
        nodes.forEach((d) => d.y = d.depth * .5 * (@height / maxdepth))

        # update the nodes data and click function
        node = @svg.selectAll("g.node")
            .data(nodes, (d) => (d.id || d.id = ++@i))
            .on("click", @nodeClick)
            .attr("class", (d) =>
                if (@selectedNodes.indexOf d) != -1
                    "node selected"
                else if d.name?
                    "node"
                else
                    "node invalid"
            )

        # Enter any new nodes at the parent's previous position
        nodeEnter = node.enter().append("g")
            .attr("transform", (d) => "translate(#{@root.x0},#{@root.y0})")
            .attr("class", (d) =>
                if (@selectedNodes.indexOf d) != -1
                    "node selected"
                else if d.name?
                    "node"
                else
                    "node invalid"
            )

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
            .attr("transform", "translate(#{@root.x},#{@root.y})")
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
                o = {x: @root.x0, y: @root.y0}
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
                o = {x: @root.x, y: @root.y}
                @diagonal({source: o, target: o})
            )
            .remove()

        # Stash the old positions for transition
        nodes.forEach((d) ->
            d.x0 = d.x
            d.y0 = d.y
        )

    # get node(s) by name, return [] if none contained
    get: (name) =>
        found = []
        get = (node, name) ->
            if name == node.name
                found.push node
            _.each node.children, (child) -> get(child, name)
        get @root, name

        found

    # recursively search tree for node with name
    contains: (name) =>
        contains = (node, name) ->
            if name == node.name
                true
            else
                _.some node.children, (child) -> contains(child, name)

        contains @root, name

    # select nodes and redraw
    selectArray: (nodes) =>
        @selectedNodes = nodes
        do @update

    # select node redraw
    select: (node) =>
        # add element if contained
        if (@selectedNodes.indexOf node) == -1
            @selectedNodes.push node
            console.log @selectedNodes
            do @update

    # deselect node
    deselect: (node) =>
        index = @selectedNodes.indexOf node
        if index != -1
            @selectedNodes.splice index, 1
            do @update

    # deselect all nodes and redraw
    deselectAll: () =>
        @selectedNodes = []
        do @update

    # get all selected nodes
    selected: () =>
        @selectedNodes

    # set on-click function for each node
    nodeOnClick: (f) =>
        @nodeClick = f
        do @update











