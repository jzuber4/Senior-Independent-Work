class Tree
    constructor: (@divId, @url) ->
        @duration = 750
        @id = 0

        # create the space containing the tree
        @margin = {top: 20, right: 50, left: 50, bottom: 20}
        @width  = $(@divId).width() - margin.left - margin.right
        @height = $(@divId).width() * 1.5 - margin.top - margin.bottom

        @tree = d3.layout.tree()
            .size([height, width])

        @diagonal = d3.svg.diagonal()
            .projection((d) -> [d.x, d.y])

        @svg = d3.select(@divId).append("svg")
            .attr("width", width + margin.right + margin.left)
            .attr("height", height + margin.top + margin.bottom)
          .append("g")
            .attr("transform", "translate(#{margin.left},#{margin.top})")

        # load the data
        d3.json(@url, (error, data) =>
            @root = data
            # build the tree
            do @update
        )

    update:
        # compute the new tree layout
        nodes = tree.nodes(@root).reverse()
        links = tree.links(nodes)

        # adjust the tree to fit
        maxdepth = d3.max(nodes, (n) -> n.depth)
        nodes.forEach((d) => d.y = d.depth * (@height / maxdepth))

        # update the nodes
        node = svg.selectAll("g.node")
            .data(nodes, (d) => (d.id || d.id = ++@i))

        # Enter any new nodes at the parent's previous position
        nodeEnter = node.enter().append("g")
            .attr("class", "node")
            .attr("transform", (d) => "translate(#{@root.x0},#{@root.y0})")







