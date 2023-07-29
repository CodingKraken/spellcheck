from editdist import edit_dist
from tree import dictionary


def searchTree(tree, parent, query, similarWords):
    parentList = tree.get(parent)
    t = 1
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
  return similarWords

queryWord = input("What word do you want to check? ")
print(returnSimilars(dictionary, "stick", queryWord, []))