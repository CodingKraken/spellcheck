import textwrap
import time
import sys
start = time.perf_counter()
####################
from formatted_dictionary import dictionary
list1 = []
uniquecharacters = "abcdefghijklmnopqrstuvwxyz'"
modified_dictionary = {}
for i in list(dictionary):
    for j in i.lower():
        if not j.isalpha() and j != "'":
            break
    else:
        for j in i.lower():
            if j not in uniquecharacters:
                uniquecharacters = uniquecharacters + str(j)
        list1.append(i)
counter = len(list1)
for i in list1:
    modified_dictionary[i] = counter
    counter += -1
counter = len(modified_dictionary)
print("All uniquecharacters: "+uniquecharacters)
print("now writing modified_dictionary.py...")
with open("modified_dictionary.py", "w", encoding="utf-8") as file:
    file.write("modified_dictionary = {\n")
    file.flush()
    for i, v in enumerate(list1):
        if i != len(list1) - 1:
            string1 = '"'+str(v)+'"'+" : "+str(counter)+",\n"
        else:
            string1 = '"'+str(v)+'"'+" : "+str(counter)+"\n"
        string2 = textwrap.indent(string1, "    ")
        file.write(string2)
        file.flush()
        counter += -1
    file.write("}")
    file.flush()
print("finished writing to modified_dictionary.py, now constructing BK tree")
#####################################################################
#####################################################################
# Computation of Damerau-Levenshtein Distance, based on 
# Lowrance, Wagner (1975), "An Extension to the String-to-String Correction Problem"
# and https://en.wikipedia.org/wiki/Damerau-Levenshtein_distance
def edit_dist(a: str, b: str, alphabet: str="0123456789abcdefghijklmnopqrstuvwxyz'") -> int:
    # the paper indexes all strings from 1, and certain special 2d arrays 
    # from 0 and -1, to get around this we can use dictionaries where the 
    # keys allow for such indexing, without nasty magic offsets
    d: dict[tuple[int, int], int] = {}
    a_dict: dict[int, str] = {}
    b_dict: dict[int, str] = {}
    for i in range(1, len(a)+1):
        a_dict[i] = a[i-1]
    for j in range(1, len(b)+1):
        b_dict[j] = b[j-1]


    # da[c] will store largest x <= len(a)-1 s.t. a[x] = c, for all characters.
    # later, db will hold the largest y <= len(b)-1 s.t. b[y] = a[i]
    da: dict[str, int] = {}

    for i in alphabet:
        da[i] = 0

    max_dist = len(a) + len(b)
    d[-1,-1] = max_dist

    # index -1 always holds the maximum distance possible between a and b,
    # index 0 is the cost between the null string and the current index
    # of the characters in a and b respectively
    for i in range(0,len(a)+1):
        d[i, -1] = max_dist
        d[i, 0]  = i
    for j in range(0,len(b)+1):
        d[-1, j] = max_dist
        d[0, j] = j
    
    for i in range(1, len(a)+1):
        db = 0
        for j in range(1, len(b)+1):
            # store indices of last common letter in a and b in k and l,
            # these will be used to compute the cost of transpositions
            k = da[b_dict[j]]
            l = db
            cost = 1
            if a_dict[i] == b_dict[j]:                
                cost = 0
                db = j
            d[i, j] = min(d[i-1, j-1] + cost,                                   # substitution
                          d[i,   j-1] + 1,                                      # insertion
                          d[i-1, j  ] + 1,                                      # deletion
                          max(d[i-1,j-1], d[k-1, l-1] + (i-k-1) + 1 + (j-l-1))) # transposition
            da[a_dict[i]] = i
    return d[len(a), len(b)] # The final edit distance between the strings
####################
# editdist function is symmetric
# Each node-line: [word, frequency_of_word, (parent, editdist(parent, word)), (editdist(child1, word), child1, freq_of_child1)...]
# All_Nodes: [nodeline1, nodeline2, nodeline3, nodeline4...]
# the function below takes in a word, and if the word has an editdis with the rootword equal to some other word listed as a child in the rootwordline, it will move on to that child and repeat the process
# the word to analyze it's children is named currentnode here, where the currentnodeline is the line consisting of the currentnode, its frequency, its parent, and its children
# recur until the word has an editdistance not shared by any of the children in currentnodeline, at which point the currentnode will become the parent of the word, and the word will become another child of the currentnode
# Also please note that back up where we created the modified_dictionary, we one assume that the formatted_dictionary is already ranked by frequency, and two the 'frequency's are relative and count down by one. Therefore we can speed this code up a whole bunch by calculating the index of each nodeline in All_Nodes via that 'frequency'.
####################
def stuff(allnodes, currentnodeline, word, rootfreq_num, len_num, uniqchars): # This is a recursive function, its job is to follow the current tree down from the root until it hits a spot where the word should be added. all the important information to change the tree accordingly is then passed ahead to 'central command', and so by doing such, the tree grows by one word every time this function returns
    newnode = []
    newwordline = [] # This list will be the nodeline for whichever word is currently being added to All_Nodes
    updatedcurrentnodeline = currentnodeline[:] # make a copy of the currentnodeline in case this is where we add the word, so that central command knows what to change currentnodeline to.
    currentnode = currentnodeline[0] # Get currentnode from currentnodeline
    editdis = edit_dist(currentnode, word, alphabet=chars) # Compare currentnode and the word
    children = currentnodeline[3:] #save children of currentnode in order to subsequently determine whether to add the word or recur.
    if children: # this returns True if children exist, and False if list of children is empty
        for i, child in enumerate(children):
            if child[0] == editdis:
                newnode = child
                if newnode[2] > rootfreq_num: # it turns out since the modified_dictionary is already sorted, the only part of All_Nodes that isn't sorted is the rootnodeline, and because it is supposed to be somewhere more towards the middle of the list, that means for everything else in relation to where the rootnodeline should be, their frequency matches up with their index in All_Nodes in differing ways.
                    newnodeline = allnodes[len_num-newnode[2]+1]
                else:
                    newnodeline = allnodes[len_num-newnode[2]]
                return stuff(allnodes, newnodeline, word, rootfreq_num, len_num, uniq_chars) # ok cool so we found a child that shares our editdis, and therefore our new currentnode is that child.
            elif child[0] > editdis: # we create each nodeline with their children in order by editdis. since the children are in order, if while we go across the children we encounter a child that has an editdis greater than ours, we can know for sure that none of the subsequent children will share our editdis, and so we can stop right there. Since wherever we would insert the new child is exactly right before the first greater-than child, we can insert the new child at exactly the position where this conditional first retrusn True.
                updatedcurrentnodeline.insert(i + 3, (editdis, word, modified_dictionary.get(word)))
                break
        else:
            updatedcurrentnodeline.append((editdis, word, modified_dictionary.get(word))) # This would mean we went through every child, and all of them had editdis's less than ours, and therefore we can add this new child at the very end. logically, it means 'if break not encountered'
    else: # if there are no children, then none of them share our editdis, and we can just immediately add this new child.
        updatedcurrentnodeline.append((editdis, word, modified_dictionary.get(word)))
    newwordline = [word, modified_dictionary.get(word), (currentnode, editdis)] # This was going to happen no matter how we encounter the children, and if this currentnodeline is not our parent, then we recur before even reaching this line.
    # Again, we can just calculate the index using said frequency
    if currentnodeline == allnodes[0]:
        loc = 0
    elif int(currentnodeline[1]) > rootfreq_num:
        loc = len_num - currentnodeline[1] + 1
    else:
        loc = len_num - currentnodeline[1]
    Shipment = [loc, updatedcurrentnodeline, newwordline] # Package all the important information into one list, and send it to 'central command'
    return Shipment
len_dictionary = len(modified_dictionary) # get relevant numbers so we can calculate indexes
frequency_of_stick = modified_dictionary.get("stick")
index_of_stick_in_dictionary = len_dictionary - frequency_of_stick + 1
Dict = list(modified_dictionary) # Gets all of the dictionary words
Dict.remove("stick") # Correction: gets all of the *other* dictionary words
Rootnodeline = ['stick', frequency_of_stick, None] # Creates the rootnodeline
All_Nodes = [Rootnodeline] # Initialize the tree using the rootnodeline
counter = 1
for i in Dict: # 'central command' - commence tree growth
    Package = stuff(All_Nodes, All_Nodes[0], i, frequency_of_stick, len_dictionary, uniquecharacters) # run the stuff above
    present1 = Package[0] # Unwrap package
    present2 = Package[1]
    present3 = Package[2]
    All_Nodes[present1] = present2 # Make changes based on package
    All_Nodes.append(present3)
    counter += 1
    if counter%1000 == 0:
        print(str(counter), "out of", str(len_dictionary - 1), "words added...")
FinalTree = All_Nodes[1:index_of_stick_in_dictionary] + [All_Nodes[0]] + All_Nodes[index_of_stick_in_dictionary:] # Again, we only one have misplaced nodeline, the rootnodeline, and here we say we can return All_Nodes back to the same ordering as the original modified_dictionary in one step 
# FinalTree is the final list of word-lines, can now just file.write(each line) into tree.py
print("finished constructing tree, now writing tree to file")
with open("tree.py", "w", encoding="utf-8") as file:
    counter = 0
    file.write("dictionary2 = {\n")
    file.flush()
    for i, v in enumerate(FinalTree):
        if len(v) < 4: # add (None) to end of all dead-end nodelines, since they have no children. This caused many problems when trying to do this during the construction of the tree, so instead we do it later.
            if i != len_dictionary - 1:
                string3 = '"' + str(v[0]) + '"' + " : " + str((v[1], v[2], (None))) + ",\n"
            else:
                string3 = '"' + str(v[0]) + '"' + " : " + str((v[1], v[2], (None))) + "\n"
            string4 = textwrap.indent(string3, "    ") # In VS code, 4 spaces = 1 indent
            file.write(string4)
            file.flush()
        else:
            familystring = v[3:]
            newfamilystring = [v[1], v[2]]
            for i in familystring:
                newmemberstring = tuple(i)
                newfamilystring.append(newmemberstring)
            newnewfamilystring = tuple(newfamilystring)
            if i != len_dictionary - 1:
                string3 = '"' + str(v[0]) + '"' + " : " + str(newnewfamilystring) + ",\n"
            else:
                string3 = '"' + str(v[0]) + '"' + " : " + str(newnewfamilystring) + "\n"
            string4 = textwrap.indent(string3, "    ")
            file.write(string4)
            file.flush()
        counter += 1
        if counter%10000 == 0:
            print(str(counter), "wordlines written...")
    file.write("}")
    file.flush()
end = time.perf_counter()
from tree import dictionary2
size = sys.getsizeof(dictionary2) + sys.getsizeof(modified_dictionary)
print("Done! Took", str((end-start)//60), "minutes and", str((end-start)%60), "seconds", "along with", str(size/1000000), "megabytes of memory")
