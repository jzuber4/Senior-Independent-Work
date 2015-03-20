class @Tree
    # divId specifies div that tree will inhabit
    # data is data representing tree
    # prefix is namespace prefix to prevent collision with
    # other properties stored on the objects in the tree
    constructor: (@divId, data, options = {}) ->
        @selectedNodes = []
        @duration = options.duration ? 500
        @i = 0
        @nodeClick = options.nodeClick ? (() ->)
        @radius = 20 ? options.radius
        @xScale = options.xScale ? 1
        @yScale = options.yScale ? 1

        # create the space containing the tree
        @margin = options.margin ? {
            top:    options.marginTop    ? 50
            right:  options.marginRight  ? 50
            left:   options.marginLeft   ? 50
            bottom: options.marginBottom ? 50
        }
        @width  = options.width  ? @xScale * ($("##{@divId}").width() - @margin.left - @margin.right)
        @height = options.height ? @yScale * (@width - @margin.top - @margin.bottom - 200)

        @tree = d3.layout.tree()
            .size([@width, @height])

        @diagonal = d3.svg.diagonal()
            .projection((d) -> [d.x, d.y])

        @svg = d3.select("##{@divId}").append("svg")
            .attr("width", @width + @margin.right + @margin.left)
            .attr("height", @height + @margin.top + @margin.bottom)
          .append("g")
            .attr("transform", "translate(#{@margin.left},#{@margin.top})")

        Tree.assertValid data

        # make tree
        @root = data
        @root.x0 = @width / 2
        @root.y0 = 0
        do @update

    # static function, validates whether data represents valid tree
    # throws error if invalid
    @assertValid: (data) ->
        root = data

        # recursively check
        assertValid = (node, parent) ->
            # node must have children defined
            unless node.children?
                throw new Error("Tree: node must have property \"children\"")

            # node must not already have been seen (no cycles)
            if node.seen?
                throw new Error("Tree: tree must not contain cycles")
            node.seen = true

            # all subtrees must be valid
            _.each node.children, (child) -> assertValid child, node.name

        removeSeen = (node) ->
            delete node.seen
            _.each node.children, (child) -> removeSeen child

        # check if the data is valid, recursively
        assertValid data, null
        # remove added property "seen"
        removeSeen data

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
                classes = ""
                if d.classes?
                    _.each d.classes, (c) -> classes = classes + c + " "
                if (@selectedNodes.indexOf d) != -1
                    classes + "node selected"
                else if d.name?
                    classes + "node"
                else
                    classes + "node invalid"
            )

        # Enter any new nodes at the parent's previous position
        nodeEnter = node.enter().append("g")
            .attr("transform", (d) => "translate(#{d.x},#{d.y})")
            .on("click", @nodeClick)
            .attr("class", (d) =>
                classes = ""
                if d.classes?
                    _.each d.classes, (c) -> classes = classes + c + " "
                if (@selectedNodes.indexOf d) != -1
                    classes + "node selected"
                else if d.name?
                    classes + "node"
                else
                    classes + "node invalid"
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
            .attr("r", @radius)

        nodeUpdate.select("text")
            .style("fill-opacity", 1)
            .text((d) -> d.name)

        # Transition exiting nodes to the parent's new position
        nodeExit = node.exit().transition()
            .duration(@duration)
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
            .attr("d", @diagonal)
            .style("stroke-opacity", 1e-6)

        # Transition links to their new position.
        link.transition()
            .duration(@duration)
            .style("stroke-opacity", 1)
            .attr("d", @diagonal)

        # Transition exiting nodes to the parent's new position
        link.exit().transition()
            .duration(@duration)
            .style("stroke-opacity", 1e-6)
            .remove()

        # Stash the old positions for transition
        nodes.forEach((d) ->
            d.x0 = d.x
            d.y0 = d.y
        )

    # converts tree into easily serializable representation
    toSerializable: () =>
        toSerializable = (curr) ->
            if curr.children?
                {
                    name: curr.name
                    children: (toSerializable child for child in curr.children)
                }
            else
                {
                    name: curr.name
                    children: []
                }
        toSerializable @root

    # get node(s) by name, return [] if none contained
    get: (name) =>
        found = []
        get = (node, name) ->
            if name == node.name
                found.push node
            _.each node.children, (child) -> get(child, name)
        get @root, name

        found

    # apply a function f to each node in depth first order
    each: (f) =>
        each = (node) ->
            f node
            if node.children?
                _.each node.children, (child) -> each child
        each @root
        do @update


    # recursively search whole tree for node with name
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

class @BinaryTree extends Tree
    constructor: (@divId, data, options = {}) ->
        BinaryTree.assertValid data
        super @divId, data, options

    # validates whether data represents a valid binary tree
    # throws error if invalid
    @assertValid: (data) ->

        # only added requirement is that there are at most 2 children
        assertValid = (node) ->
            if node.children.length > 2
                throw new Error("BinaryTree: a node cannot have more than two children")
            _.all node.children, (child) -> assertValid child

        # validate as tree
        super data
        # validate as binary tree
        assertValid data

    insert: (node, name) =>
        node.name = name
        node.children = [{name:null,parent:node,children:[]},{name:null,parent:node,children:[]}]
        do @update

    remove: (node) =>
        emptyNode = {name: null, parent:node.parent, children:[]}
        index = node.parent.children.indexOf node
        node.parent.children[index] = emptyNode
        do @update

    # rotates the node (assumes binary tree) and redraws.
    # left or right depends on which side the child is on
    rotate: (node) =>
        unless node.parent?
            return # root cannot be rotated

        parent = node.parent
        grandparent = parent.parent

        # rotate and change children
        swapped = null
        if parent.children[0] == node
            # rotate right
            swapped = node.children[1]
            node.children[1] = parent
            parent.children[0] = swapped

        else
            # rotate left
            swapped = node.children[0]
            node.children[0] = parent
            parent.children[1] = swapped

        # change parents
        parent.parent = node
        swapped.parent = parent
        node.parent = grandparent

        # set child of grandparent (node will be root if it doesn't exist)
        if grandparent?
            if grandparent.children[0] == parent
                grandparent.children[0] = node
            else
                grandparent.children[1] = node
        else
            @root = node

        do @update
