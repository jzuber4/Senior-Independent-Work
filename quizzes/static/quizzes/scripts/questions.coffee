# make a BST Search question with data in the div specified by divId
class @BSTSearchQuestion
    constructor: (divId, data, @onChange = (() -> )) ->
        opts =
            nodeClass: ((d) -> if d.name? then "clickable" else "")
            radius: ((d) ->
                if not d.children? or d.children.length == 0
                    5
                else
                    20
            )
        @tree = new BinaryTree(divId, data, opts)

        # click function that allows user to select nodes (and fill input)
        @answer = []

        onClick = (d) =>
            # disallow nodes without names
            unless d.name?
                return

            # toggle selected status of node
            index = @answer.indexOf d
            if index == -1
                @tree.select d
                @answer.push d
            else
                @tree.deselect d
                @answer.splice index, 1

            # reorder nodes by depth first order
            newAnswer = []
            @tree.each (node) =>
                if (@answer.indexOf node) != -1
                    newAnswer.push node
            @answer = newAnswer

            do @onChange

        @tree.nodeOnClick onClick

    # set the change callback to f
    change: (f) ->
        @onChange = f

    # update the tree to have a new set of selected nodes
    # return true if the tree is updated without error, false otherwise
    update: (text) =>
        try
            # get list of selected names from text
            console.log("inUpdate")
            names = _.map((text.split /(\s+)/), (s) -> s.trim()).filter((s) -> s.length > 0 and !isNaN(s))
            console.log("names")

            @answer = []
            @tree.each (node) =>
                if node.name?
                    index = names.indexOf (node.name.toString())
                    if index != -1
                        @answer.push node
                        names.splice index, 1

            @tree.selectArray @answer
            true
        catch e
            console.log e
            false

    # get the value to submit to the server
    submit: () =>
        _.map @answer, (node) -> node.name

# make a BST Insert question with data in the div specified by divId
# set the change callback to onChange (default is noop function)
class @BSTInsertQuestion
    constructor: (divId, @data, @change = (() -> )) ->

        # dimensions and setup for making display of numbers
        @numsHeight = 90
        @largerRadius = 30
        @circleRadius = 20
        @circleMargin = 10
        @width  = (2 * @circleRadius + @circleMargin) * data.length
        @duration = 500
        # svg container for display

        @svg = d3.select("##{divId}").append("svg")
                .attr("width", @width)
                .attr("height", @numsHeight)

        # sequence of keys to insert
        @nums = data[1..]

        # create display of numbers
        @update @nums

        # create tree
        treeData = {name: data[0], children: [{name: "", children: []}, {name: "", children: []}]}
        opts =
            nodeClass: ((d) -> if d.children then "" else "clickable dashed")
        @tree = new BinaryTree(divId, treeData, opts)
        @inserts = []

        onClick = (d) =>
            # can only insert in empty nodes
            # and if there are numbers left to insert
            if d.children or not @nums[0]?
                return

            num = @nums[0]
            @nums = @nums[1..]

            @inserts.push(d)
            @tree.insert(d, num)
            @update @nums
            do @change

        @tree.nodeOnClick onClick

    # update the representation to display the new set of numbers to be inserted
    update: (data) =>

        data = data.slice()
        data.reverse()
        node = @svg.selectAll("g.node")
            .data(data)
            .attr("class", (d, i) =>
                if i != data.length - 1
                    "node faded"
                else
                    "node"
            )

        nodeEnter = node.enter().append("g")
                .attr("transform", (d, i) =>
                    xShift = 1.5 * @largerRadius
                    if i != data.length - 1
                        xShift += @largerRadius + (data.length - 1 - i) * (2 * @circleRadius + @circleMargin)
                    "translate(#{xShift},#{@numsHeight / 2})"
                )
                .attr("class", (d, i) =>
                    if i != data.length - 1
                        "node faded"
                    else
                        "node"
                )

        nodeEnter.append("circle")
                .attr("r", (d, i) =>
                    if i != data.length - 1
                        @circleRadius
                    else
                        @largerRadius
                )

        nodeEnter.append("text")
                .text((d) -> d)
                .attr("dy", ".35em")           # center the text vertically
                .attr("text-anchor", "middle") # center it horizontally

        nodeUpdate = node.transition()
            .duration(@duration)
            .attr("transform", (d, i) =>
                xShift = 1.5 * @largerRadius
                if i != data.length - 1
                    xShift += @largerRadius + (data.length - 1 - i) * (2 * @circleRadius + @circleMargin)
                "translate(#{xShift},#{@numsHeight / 2})"
            )

        nodeUpdate.select("circle")
                .attr("r", (d, i) =>
                    if i != data.length - 1
                        @circleRadius
                    else
                        @largerRadius
                )

        nodeExit = node.exit().transition()
            .duration(@duration)
            .remove()
            .attr("transform", "translate(#{1.5 * @largerRadius},#{@numsHeight})")

        nodeExit.select("circle")
            .attr("r", 1e-6)

        nodeExit.select("text")
            .style("fill-opacity", 1e-6)

    # set the change callback to f
    onChange: (f) =>
        @change = f

    # get the number of elements left to insert
    numLeft: () =>
        @nums.length

    # can an insertion be undone?
    canUndo: () =>
        @inserts.length > 0

    # undo the last insertion
    undo: () =>
        if @canUndo()
            d = @inserts.pop()
            @tree.remove d
            @nums.unshift d.name
            @update @nums

    # get the value to submit to the server
    submit: () =>
        @tree.toSerializable()



