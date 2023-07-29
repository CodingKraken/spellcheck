from tree import dictionary
from one_step_suggestions import suggestions

def mostUsed(similars: list, dictionary):
  mostUsed = 0
  for i in range(len(similars)):
    currentFreq = dictionary.get(similars[i])
    currentFreq = currentFreq[0]
    if currentFreq > mostUsed:
      mostUsed = currentFreq

def partition(similars, start, end, dictionary):
  # defining the pivot
  pivot = similars[end] # rightmost elemement
  i = start - 1 # element larger than pivot
  
  # iterating through similars and sorting which elements are before and after the pivot
  for j in range(start, end):
    #when element smaller than pivot
    freqPivot = dictionary.get(pivot)
    freqElementJ = dictionary.get(similars[j])
    if  freqElementJ[0] < freqPivot[0]:
      i += 1 # move focused marker over one
      swap(similars, i, j) # swap element less than pivot with element greater than pivot

  swap(similars, i + 1, end)
  return i + 1

def swap(similars, i, j):
  temp = similars[i]
  similars[i] = similars[j]
  similars[j] = temp

def quickSort(similars: list, start, end, dictionary):
  if len(similars) < 2:
    return mostUsed(similars, dictionary)
  else:
    if start < end:
      pIndex = partition(similars, start, end, dictionary)
      quickSort(similars, start, pIndex - 1, dictionary)
      quickSort(similars, pIndex + 1, end, dictionary)

def returnSorted(similars: list, start, end, dictionary):
  quickSort(similars, start, end, dictionary)
  print(similars)

words = ["yay", "ray", "say", "play", "the", "words", "talk"]
# quickSort(suggestions("yay"), 0, len(words) - 1, dictionary)
returnSorted(words, 0, len(words) - 1, dictionary)