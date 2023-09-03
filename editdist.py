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
