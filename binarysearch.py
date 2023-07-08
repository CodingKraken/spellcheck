# woah here's a comment

word = "the"
file = open('dictionary.txt')
contents = file.read()
file.close()
D = contents.split()
def d_check(wd, d):
    wd = wd.lower()
    wd = wd.replace("-", "")
    A = "!&',./0123456789abcdefghijklmnopqrstuvwxyz"
    v = [A.find(c) for c in wd]
    l = 0
    h = len(d) - 1
    while l <= h:
        m = (l + h) // 2
        w = (d[m]).lower()
        w = w.replace("-", "")
        if w == wd:
            return True
        if l == h:
            return False
        lv = len(v)
        lw = len(w)
        mn = min(lv, lw)
        i = 0
        while i < (mn) and v[i] == A.find(w[i]):
            i += 1
        if i == (lv) or v[i] > A.find(w[i]):
            l = m + 1
        else:
            h = m - 1
print(d_check(word, D))
