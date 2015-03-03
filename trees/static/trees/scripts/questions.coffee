# make a BST Search question with data in the div specified by divId
class @BSTSearchQuestion
    constructor: (divId, data, onChange) ->
        @tree = new BinaryTree(divId, data)
        @onChange = onChange? onChange : (() -> )

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

    change: (f) ->
        @onChange = f

    # update the tree to have a new set of selected nodes
    # return true if the tree is updated without error, false otherwise
    update: (text) =>
        try
            # get list of selected names from text
            names = _.map((text.split ","), (s) -> s.trim()).filter((s) -> s.length > 0)

            @answer = []
            @tree.each (node) =>
                if node.name?
                    index = names.indexOf (node.name.toString())
                    if index != -1
                        @answer.push node
                        names.splice index, 1

            @tree.selectArray @answer
            do @onChange
            true
        catch e
            console.log e
            false

    submit: () =>
        _.map @answer, (node) -> node.name

class @BSTInsertQuestion

    constructor: (divId, data) ->
        @tree = new BinaryTree(divId, {name: data[0], children: [{name: null, children: []}, {name: null, children: []}]})

        # sequence of keys to insert
        nums = data[1..]

        onClick = (d) =>
            # can only insert in empty nodes
            if d.name?
                return

            num = nums[0]
            nums = nums[1..]

            @tree.insert(d, num)

        @tree.nodeOnClick onClick

    submit: () =>
        @tree.toSerializable()



