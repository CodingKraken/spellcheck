from editdist import edit_dist

dictionary3 = {
    'stock' : [291222, ['stick', 1], [1, 'stuck'], [2, 'sick']],
    'sick' : [291070, ['stock', 2], [1, 'slick'], [2, 'sticks']],
    'stick' : [290682, [None], [1, 'stock']],
    'stuck' : [290360, ['stock', 1], [1, 'stack'], [2, 'stoick']],
    'sticks' : [286799, ['sick', 2], [1, 'sticky'], [2, 'stink']],
    'stack' : [285914, ['stuck', 1], [1, 'steck']],
    'sticky' : [282915, ['sticks', 1], [None]],
    'tick' : [282910, ['slick', 2], [None]],
    'slick' : [281489, ['sick', 1], [1, 'spick'], [2, 'tick']],
    'stink' : [276801, ['sticks', 2], [1, 'stik'], [2, 'shtick']]
}

def searchTree(tree, parent, query, similarWords):
    parentList = tree.get(parent)
    t = 2
    d = edit_dist(parent, query)
    # if the parent word is in acceptable tolerance t
    if d <= t:
        similarWords.append(parent)

    # Do not have the first index become a negative number
    if d - t <= 0:
        low = 0
    else:
        low = d - t

    # only look at children in acceptable range
    # [edit-dist(parent, query) + t, edit-distance(parent, query) - t]
    for i in range(low, d + t):
        try:
            child = parentList[i + 2][1]
            searchTree(tree, child, query, similarWords)
        except:
           break 
    

def returnSimilars(tree, parent, query, similarWords):
  searchTree(tree, parent, query, similarWords)
  print(similarWords)

words = []
returnSimilars(dictionary3, "stick", "stim", [])