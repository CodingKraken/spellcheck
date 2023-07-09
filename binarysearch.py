# woah here's a comment!
#comment two!
# comment tre

word = "yay"
file = open('correctdictionary.txt')
contents = file.read()
file.close()
D = contents.split()
def d_check(wd, d):
    wd1 = wd.lower()
    A = "!&',-./0123456789abcdefghijklmnopqrstuvwxyz"
    v = [A.find(c) for c in wd1]
    l = 0
    h = len(d) - 1
    while l <= h:
        m = (l + h) // 2
        w = d[m]
        print(m, w)
        w1 = w.lower()
        if w == wd:
            return True
        if l == h:
            return l
        lwd = len(wd)
        lw = len(w)
        mn = min(lwd, lw)
        i = 0
        while i < mn and v[i] == A.find(w1[i]):
            i += 1
        if i == lw:
            l = m + 1
        elif i == lwd:
            h = m - 1
        elif v[i] > A.find(w1[i]):
            l = m + 1
        else:h = m - 1

print(d_check(word, D))
