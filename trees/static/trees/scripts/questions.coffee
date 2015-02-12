# make a BST Search question with data in the div specified by divId
@InitQuestionBSTSearch = (divId, data) ->
    tree = new BinaryTree(divId, data)

    # click function that allows user to select nodes (and fill input)
    answer = []

    onClick = (d) ->
        # disallow nodes without names
        unless d.name?
            return

        # toggle selected status of node
        index = answer.indexOf d.name
        if index == -1
            tree.select tree.get(d.name)[0]
            answer.push d.name
        else
            tree.deselect tree.get(d.name)[0]
            answer.splice index, 1

        # update answer
        $("#inputAnswer").val answer

    tree.nodeOnClick onClick

@InitQuestionBSTInsert = (divId, data) ->
    tree = new BinaryTree(divId, {name: null, children: []})
    # sequence of keys to insert
    sequence = data
