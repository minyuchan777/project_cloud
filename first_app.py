import streamlit as st
import pandas as pd
import altair as alt
import dna_app
import re


st.write("""
# DNA Nucleotide Count Web App

This app counts the nucleotide composition of query DNA!

***
""")

###################
# Input Text Box
###################

#st.sidebar.header('Enter DNA sequence')
st.header('Enter DNA sequence')


#sequence = st.sidebar.text_area("Sequence input", sequence_input, height=250)
seq = st.text_area("Sequence input", height=250)

st.write("""
***
""")

## Prints the input DNA sequence
st.header('INPUT (DNA Query)')

## DNA nucleotide count
st.header('OUTPUT (DNA Nucleotide Count)')

### 1. Print dictionary
st.subheader('1. Print dictionary')


def DNA_nucleotide_count(seq):
    d = dict([
              ('A', seq.count('a')),
              ('T', seq.count('t')),
              ('G', seq.count('g')),
              ('C', seq.count('c'))
              ])
    return d


X = DNA_nucleotide_count(seq)

#X_label = list(X)
#X_values = list(X.values())

X

### 2. Print text
st.subheader('2. Print text')
st.write('There are ' + str(X['A']) + ' adenine (A)')
st.write('There are ' + str(X['T']) + ' thymine (T)')
st.write('There are ' + str(X['C']) + ' cytosine (C)')
st.write('There are ' + str(X['G']) + ' guanine (G)')

### 3. Display DataFrame
st.subheader('3. Display DataFrame')
df = pd.DataFrame.from_dict(X, orient='index')
df = df.rename({0: 'count'}, axis='columns')
df.reset_index(inplace=True)
df = df.rename(columns = {'index':'nucleotide'})
st.write(df)

### 4. Display Bar Chart using Altair
st.subheader('4. Display Bar chart')
p = alt.Chart(df).mark_bar().encode(
    x='nucleotide',
    y='count'
)
p = p.properties(
    width=alt.Step(80)  # controls width of bar
)
st.write(p)

### 5. Transcribe or Translate sequence using module function
st.subheader('5. Transcribe or Translate')
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

for i in seq:
    match1 = re.findall("t", seq, re.IGNORECASE)
    match2 = re.findall("u", seq, re.IGNORECASE)

    if match1:
        trans_rna_seq = seq.replace('t', 'u')
        for i in range(0, len(trans_rna_seq), 3):
            if codon[trans_rna_seq[i:i + 3]]:
                protein_seq += codon[trans_rna_seq[i:i + 3]]
        st.write("This is a DNA sequence")
        st.write("The translated protein sequence is: ", protein_seq)
        st.write("The RNA sequence is: ", trans_rna_seq)
        break

    elif match2:
        # transcribe user dna sequence into rna sequence
        trans_dna_seq = seq.replace('u', 't')
        for i in range(0, len(seq), 3):
            if codon[seq[i:i + 3]]:
                protein_seq += codon[seq[i:i + 3]]
        st.write("This is a RNA sequence")
        st.write("The translated protein sequence is: ", protein_seq)
        st.write("The DNA sequence is: ", trans_dna_seq)
        break

    else:
        st.write("This is not a valid nucleotide sequence")
        break


### 6. Findings of palindromes with spacer region are assigned to 'spacer_palindromes'
st.subheader('6. Palindrome Finder')
spacer_palindromes = dna_app.remove_unwanted_palindromes(dna_app.find_spacer_palindrome(seq),
                                                         dna_app.find_palindrome(seq))

# To print palindromes with no spacers:
st.write('no. of non-spacer palindromes found:', len(dna_app.find_palindrome(seq)))
num = 0
for pal1 in dna_app.find_palindrome(seq):
    num += 1
    st.write('Palindrome ' + str(num) + ':\n' + pal1[0])
    st.write('Indexes:', pal1[1], '-', pal1[2])
    st.write('Length:', len(pal1[0]), '\n')

# To print palindromes with spacers:
st.write('no. of spacer palindromes found:', len(dna_app.find_spacer_palindrome(seq)))
for pal2 in dna_app.find_spacer_palindrome(seq):
    num += 1
    st.write('Palindromes with spacer region ' + str(num) + ':\n' + pal2[0])
    st.write('Indexes:', pal2[1], '-', pal2[2])
    st.write('Length:', len(pal2[0]), '\n')
