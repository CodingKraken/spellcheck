# This code here creates 4 lists, each pertaining to a type of change. ie: insertion, deletion, substitution, and transposition. each list has one or two for-loop(s) behind it, computing all of the permutations and only appending them to the list if d_check(permutation) = True. The final step adds all the lists together into one list, of which equates to [all the existing words one step away].
# creates (140*len(wd) + 68) words, uses d_check on each one, and appends a word to a list len(suggestions) times, before combining all 4 lists.
# Theoretically, you could run this program once, and then again for each existing word one step away, for all of the 2-step suggestion words.
# please do keep in mind, our 'competition' isn't 96% accurate at suggestions or grammar checks, it is (96% or less) accurate at determining whether a word is a word, and marking it correspondingly. Either we are are already at their pace, or we are already at a point where we can discover the hard way, why they are inaccurate.
from formatted_dictionary import dictionary
D = dictionary

def suggestions(wd):
  insertion = []
  deletion = []
  substitution = []
  transposition = []
  alphabet = "!&',-./0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
  #Insertion
  for i in range(len(wd) + 1):
    for character in alphabet:
      new_word0 = wd[:i] + character + wd[i:]
      if D.get(new_word0, 0) != 0:
        insertion.append(new_word0)
  #Deletion
  for i in range(len(wd)):
    new_word1 = wd[:i] + wd[i + 1:]
    if D.get(new_word1, 0) != 0:
      deletion.append(new_word1)
  #Substitution
  for i in range(len(wd)):
    for character in alphabet:
      new_word2 = wd[:i] + character + wd[i + 1:]
      if D.get(new_word2, 0) != 0:
        substitution.append(new_word2)
  #Transposition
  for i in range(len(wd) - 1):
    new_word3 = wd[:i] + wd[i + 1] + wd[i] + wd[i + 2:]
    if D.get(new_word3, 0) != 0:
      transposition.append(new_word3)
  #Final list
  suggestion_words = insertion + deletion + substitution + transposition

  return suggestion_words