import time
####################
#set main parameters up here

# most importantly, set your root word:
rootword = "stick"

from formatted_dictionary import dictionary # change this to match the original sorted-by-frequency-from-mostfrequent-to-leastfrequent list of english words, that you *must* have

modified_dictionary_name = "please don't write" # this where you set the name of the file for modified_dictionary to be written to
# change modified_dictionary_name to "please don't write" if you do not want an extra such file.

treenamestring = "tree.py" # this is where you set the name of the file to store the BK tree.
# you wouldn't be running this program if you didn't want one of these.

# you can also change the name of the dictionary variable name in the tree file:
tree_variable_name = "dictionary"

# why not also give you the ability to change the other dictionary's variable name:
modified_dictionary_variable_name = "modified_dictionary"
# leave as is if you have changed modified_dictionary_name to "please dont write"
# the program wont even reach this section if "please dont write" is specified

####################
comments = []
totaltime = 0
####################
start_createfirstdict = time.perf_counter()
list1 = []
modified_dictionary = {}
for i in list(dictionary):
    for j in i.lower():
        if not j.isalpha() and j != "'":
            break
    else:
        list1.append(i)
counter = len(list1)
for i, v in enumerate(list1):
    modified_dictionary[v] = counter - i
end_createfirstdict = time.perf_counter()
time_createfirstdict = end_createfirstdict-start_createfirstdict
comments.append(f"time to create modified_dictionary: {time_createfirstdict}s")
totaltime += time_createfirstdict

if modified_dictionary_name != "please don't write":
    print("now writing modified_dictionary.py...")
    start_writefirstdict = time.perf_counter()
    with open(modified_dictionary_name, "w", encoding="utf-8") as file:
        file.write(modified_dictionary_variable_name+" = {\n")
        file.flush()
        for i, v in enumerate(list1):
            if i != len(list1) - 1:
                string1 = '"'+str(v)+'"'+" : "+str(counter)+",\n"
            else:
                string1 = '"'+str(v)+'"'+" : "+str(counter)+"\n"
            string2 = "    " + string1
            file.write(string2)
            file.flush()
            counter += -1
        file.write("}")
        file.flush()
    end_writefirstdict = time.perf_counter()
    time_writefirstdict = end_writefirstdict-start_writefirstdict
    comments.append(f"time to write modified_dictionary: {time_writefirstdict}s")
    totaltime += time_writefirstdict
print("now constructing BK tree")
time_editdist = 0
#####################################################################
# This is a python 3 expression of the damerau-levenshtein distance algorithm.
# Based on pseudocode from Wikipedia: https://en.wikipedia.org/wiki/Damerau-Levenshtein_distance
# and translated from the python 2 code provided by James M. Jenson II: https://gist.github.com/badocelot/5327337
def edit_dist(a, b):
    start_editdist = time.perf_counter()
    INF = len(a) + len(b)
    matrix  = [[INF for _ in range(len(b) + 2)]]
    matrix += [[INF] + list(range(len(b) + 1))]
    matrix += [[INF, m] + [0] * len(b) for m in range(1, len(a) + 1)]
    last_row = {}
    for row in range(1, len(a) + 1):
        ch_a = a[row-1]
        last_match_col = 0
        for col in range(1, len(b) + 1):
            ch_b = b[col-1]
            last_matching_row = last_row.get(ch_b, 0)
            cost = 0 if ch_a == ch_b else 1
            matrix[row+1][col+1] = min(
                matrix[row][col] + cost,
                matrix[row+1][col] + 1,
                matrix[row][col+1] + 1,
                matrix[last_matching_row][last_match_col]
                    + (row - last_matching_row - 1) + 1
                    + (col - last_match_col - 1))
            if cost == 0:
                last_match_col = col
        last_row[ch_a] = row
    end_editdist = time.perf_counter()
    global time_editdist
    time_editdist += (end_editdist - start_editdist)
    return matrix[-1][-1]
#####################################################################
####################
# editdist function is symmetric
# Each node-line: [word, frequency_of_word, (editdist(child1, word), child1), (editdist(child2, word), child2)...]
# All_Nodes: [nodeline1, nodeline2, nodeline3, nodeline4...]
    # we have to initialize All_Nodes using the root node line as the first element, because it is the rot of the tree, and we frollow the tree from the root.
    # this causes a slight problem later because while modified_dictionary is sorted, the root word is not the most frequent.
    # thus, this causes us to modify how we index words and to re-insert the rootnodeline into All_Nodes when it is finished.
# modified_dictionary is built in such a way that each word is sorted by relative frequency
# that relative frequency is represented by a number, and these numbers count down from most frequent to least frequent words.
# that means it is really easy to calculate the index of a word in allnodes, using this frequency, and so we do so.
####################


def stuff(allnodes, currentnodeline, word, rootfreq_num, len_num):
    currentnode = currentnodeline[0]
    editdis = edit_dist(currentnode, word)
    for i, child in enumerate(currentnodeline[2:]):
        if child[0] == editdis:
            child_freq = modified_dictionary[child[1]]
            return stuff(allnodes, allnodes[len_num-child_freq+(child_freq > rootfreq_num)], word, rootfreq_num, len_num)
        elif child[0] > editdis: # this here "i+2" is because the children start at index 2.
            allnodes[(currentnodeline != allnodes[0])*(len_num - currentnodeline[1] + (currentnodeline[1] > rootfreq_num))].insert(i + 2, (editdis, word))
            return
    # this is only encountered when either there are no child nodes to follow, or all of them had editdis's less than word.
    allnodes[(currentnodeline != allnodes[0])*(len_num - currentnodeline[1] + (currentnodeline[1] > rootfreq_num))].append((editdis, word))
    return




start_initialize = time.perf_counter()

# get relevant numbers so we can calculate indexes
Dict = list(modified_dictionary) # Gets all of the dictionary words
Dict.remove(rootword) # Correction: gets all of the *other* dictionary words
Rootnodeline = [rootword, modified_dictionary[rootword]] # Creates the root nodeline
All_Nodes = [Rootnodeline] # Initialize the tree using the root nodeline

end_initialize = time.perf_counter()
time_initialize = end_initialize-start_initialize
comments.append(f"time to initialize for tree-creation: {time_initialize}s")
totaltime += time_initialize

start_createtree = time.perf_counter()

root_freq = modified_dictionary[rootword]
len_dict = len(Dict) + 1
for i, v in enumerate(Dict):
    # it goes through each word (called 'v') in the english dictionary (called "Dict" here), 
    # ... and stuff() will follow down the currently-incomplete tree in order to find v should go, and then updates v's presence in v's parentnodeline.
    # since this isnt iterally a tree, and each node is represented by its presence in the tree, and its connections
    # ... all we have to update to 'add a word to the tree', is a new newword line for v, and to update v's parent wordline to account for v's new presence.
    # each time we add a word to the tree, the tree grows, while the tree has technically always existed since the initialization of rootnodeline and All_nodes
    stuff(All_Nodes, All_Nodes[0], v, root_freq, len_dict) # stuff has already updated the parent
    All_Nodes.append([v, modified_dictionary[v]]) # now we update All_Nodes, in a way that doesn't care who v's parent is.
    if (i+1)%1000 == 0: # this is solely to display progress
        print(f"{(i+1)} out of {len_dict} words in tree...")

FinalTree = All_Nodes[1:(len(modified_dictionary) - modified_dictionary[rootword] + 1)] + [All_Nodes[0]] + All_Nodes[(len(modified_dictionary) - modified_dictionary[rootword] + 1):] # Again, we only one have misplaced nodeline, the rootnodeline, and here we say we can return All_Nodes back to the same ordering as the original modified_dictionary in one step

end_createtree = time.perf_counter()
time_createtree = end_createtree - start_createtree
comments.append(f"time to create tree: {time_createtree}s, of which {time_editdist}s were spent calculating edit_dist")
totaltime += time_createtree

# FinalTree is the final list of word-lines, can now just file.write(each line) into tree.py
print("finished constructing tree, now writing tree to file")
start_writetree = time.perf_counter()
with open(treenamestring, "w", encoding="utf-8") as file:
    value = tuple(FinalTree[0][1:])
    file.write(tree_variable_name+' = {"'+str(FinalTree[0][0])+'" : '+str(value))
    file.flush()
    for i, v in enumerate(FinalTree[1:]):
        value = tuple(v[1:])
        string3 = ',\n    "' + str(v[0]) + '" : ' + str(value)
        file.write(string3)
        file.flush()
        if (i+1)%10000 == 0:
            print(str(i+1), "wordlines written to file...")
    file.write("}")
    file.flush()
end_writetree = time.perf_counter()
time_writetree = end_writetree - start_writetree
comments.append(f"time to write tree to file: {time_writetree}s")
totaltime += time_writetree

print("Done!")
for i in comments:
    print(i)
print(f"total time taken: {totaltime}s")
