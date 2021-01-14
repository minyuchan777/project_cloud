import re


protein_seq = ""
# RNA codon table
codon = {"uuu": "F", "cuu": "L", "auu": "I", "guu": "V",
         "uuc": "F", "cuc": "L", "auc": "I", "guc": "V",
         "uua": "L", "cua": "L", "aua": "I", "gua": "V",
         "uug": "L", "cug": "L", "aug": "M", "gug": "V",
         "ucu": "S", "ccu": "P", "acu": "T", "gcu": "A",
         "ucc": "S", "ccc": "P", "aca": "T", "gca": "A",
         "uca": "S", "cca": "P", "acg": "T", "gcg": "A", "gcc": "A",
         "ucg": "S", "ccg": "P", "aau": "N", "gau": "D",
         "uau": "Y", "cau": "H", "aac": "N", "gac": "D",
         "uac": "Y", "cac": "H", "aaa": "K", "gaa": "E",
         "uaa": "-STOP-", "caa": "Q", "aag": "K", "gag": "E",
         "uag": "-STOP-", "cag": "Q",  "agu": "S", "ggu": "G",
         "ugu": "C", "cgu": "R",  "agc": "S", "ggc": "G",
         "uga": "-STOP-", "cga": "R", "aga": "R", "gga": "G",
         "ugc": "C", "cgc": "R",  "agg": "R", "ggg": "G",
         "ugg": "W", "cgg": "R"}


def isComplement(left, right):
    if left == "t" and right == "a":
        return True
    if left == "a" and right == "t":
        return True
    if left == "g" and right == "c":
        return True
    if left == "c" and right == "g":
        return True
    else:
        return False


def expand(seq, left, right):  # string, left, right

    while left >= 0 and right < len(seq) and isComplement(seq[left], seq[right]):
        left -= 1  # decrement the left
        right += 1  # increment the right

    return [seq[left + 1:right], left + 1, right - 1]


def find_palindrome(seq):
    if not seq:  # if string is null
        return ''
    # Temporary list to store data assigned to 'palindrome':
    palindrome = []

    for i in range(len(seq)):
        # even case, like “abba”
        tmp = expand(seq, i, i + 1)

        if tmp != "" and len(tmp[0]) >= 4:
            palindrome.append(tmp)

    return palindrome


def expandSpacer(seq, left, right):
    counter = 0

    # while 'l and r boundary does not exceed ends of string':
    while left >= 0 and right < len(seq):

        if isComplement(seq[left], seq[right]):
            # find minimum 4 bases that are complement:
            counter += 1

        elif not isComplement(seq[left], seq[right]):
            # if previously, 1 complementary pair has been found,
            # but now non-complementary pair is screened,
            # counter is reset to 0:
            if counter == 1:
                counter = 0

            # else if statement since at least 2 consecutive
            # complementary pairs has been found:
            elif counter >= 2:
                break

        left -= 1  # decrement the left
        right += 1  # increment the right

    if counter >= 2:
        return [seq[left + 1:right], left + 1, right - 1]
    else:
        return ""


def find_spacer_palindrome(seq):
    if not seq:  # if string is null
        return ''

    palindrome = []

    for i in range(len(seq)):
        # odd case, like “ac-gt”
        tmp1 = expandSpacer(seq, i, i)

        if tmp1 != "" and len(tmp1):
            palindrome.append(tmp1)

        # even case, like “acgt”
        tmp2 = expandSpacer(seq, i, i + 1)

        if tmp2 != "" and len(tmp2):
            palindrome.append(tmp2)

    return palindrome


def remove_unwanted_palindromes(s_palindrome, palindrome):
    # Temporary list to store unwanted palindromes assigned to 'unwanted':
    unwanted = []
    # to remove results that have nested palindromes in the spacer
    for i in range(len(s_palindrome)):
        range1 = range(s_palindrome[i][1], s_palindrome[i][2])

        for j in range(0, len(palindrome)):
            range2 = range(palindrome[j][1], palindrome[j][2])
            # if there is a non-spacer palindrome within the a spacer palindrome
            if (range2.start in range1) and (range2[-1] in range1) and (s_palindrome[i] not in unwanted):
                unwanted.append(s_palindrome[i])

    # remove nested palindromes
    for u in unwanted:
        s_palindrome.remove(u)
        # print('removed sequence:', u)



