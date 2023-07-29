from editdist import edit_dist
from tree import dictionary


def searchTree(tree, parent, query, similarWords):
    parentList = tree.get(parent)
    d = edit_dist(parent, query)
    tolerence = 2

    # if the parent word is in acceptable tolerance t
    if d <= tolerence:
        similarWords.append(parent)

    # Do not have the first index become a negative number
    if d - tolerence <= 0:
        low = 0
    else:
        low = d - tolerence

    # only look at children in acceptable range
    # [edit-dist(parent, query) + t, edit-distance(parent, query) - t]
    for i in range(low, d + tolerence + 1):
        try:
            child = parentList[i + 2][1]
            searchTree(tree, child, query, similarWords)
        except:
           break 
    

def returnSimilars(tree, parent, query, similarWords):
  searchTree(tree, parent, query, similarWords)
  finalSuggestions = []
  finalTol = 1

  # make sure that the final words that are presented are within the
  # tolerence limit in order to make suggestions more accurate 
  for i in range(len(similarWords)):
    if edit_dist(similarWords[i], query) <= finalTol:
        finalSuggestions.append(similarWords[i])


  return finalSuggestions

queryWord = input("What word do you want to check? ").lower().strip()
print(returnSimilars(dictionary, "stick", queryWord, []))