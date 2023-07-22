# Computation of Damerau-Levenshtein Distance, based on 
# Lowrance, Wagner (1975), "An Extension to the String-to-String Correction Problem"
# and https://en.wikipedia.org/wiki/Damerau-Levenshtein_distance
def edit_dist(a: str, b: str, alphabet: str="0123456789abcdefghijklmnopqrstuvwxyz") -> int:
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
            if a_dict[i] == b_dict[j] and i == j:                
                cost = 0
                db = j
            d[i, j] = min(d[i-1, j-1] + cost,                           # substitution
                          d[i,   j-1] + 1,                              # insertion
                          d[i-1, j  ] + 1,                              # deletion
                          max(1, d[k-1, l-1] + (i-k-1) + 1 + (j-l-1)))  # transposition
            da[a_dict[i]] = i
    return d[len(a), len(b)] # The final edit distance between the strings
