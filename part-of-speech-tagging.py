import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import xlrd
import re
import xlwt 
from xlwt import Workbook
import collections
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from nltk.corpus import state_union
from collections import Counter
import string

'''

CC coordinating conjunction
CD cardinal digit
DT determiner
EX existential there (like: "there is" ... think of it like "there exists")
FW foreign word
IN preposition/subordinating conjunction
JJ adjective 'big'
JJR adjective, comparative 'bigger'
JJS adjective, superlative 'biggest'
LS list marker 1)
MD modal could, will
NN noun, singular 'desk'
NNS noun plural 'desks'
NNP proper noun, singular 'Harrison'
NNPS proper noun, plural 'Americans'
PDT predeterminer 'all the kids'
POS possessive ending parent's
PRP personal pronoun I, he, she
PRP$ possessive pronoun my, his, hers
RB adverb very, silently,
RBR adverb, comparative better
RBS adverb, superlative best
RP particle give up
TO to go 'to' the store.
UH interjection errrrrrrrm
VB verb, base form take
VBD verb, past tense took
VBG verb, gerund/present participle taking
VBN verb, past participle taken
VBP verb, sing. present, non-3d take
VBZ verb, 3rd person sing. present takes
WDT wh-determiner which
WP wh-pronoun who, what
WP$ possessive wh-pronoun whose
WRB wh-abverb where, when
'''



filtered_list=[]
same_values_counter = []
prepList = ["","CC" , "CD" , "DT" , "EX" , "FW" , "IN" , "JJ" , "JJR" , "JJS" , "LS" , "MD" , "NN" , "NNS" , "NNP" , "NNPS" , "PDT" , "POS" ,
            "PRP" , "PRP$" , "RB" , "RBR" , "RBS" , "RP" , "RP" , "TO" , "UH" , "VB" , "VBD" , "VBG" , "VBN" , "VBP" , "VBZ" , "WDT" , "WP" , "WP$" , "WRB" ]
count=0
length_list=0

                # XLSX formatted source file reading Source
                
loc = (r"F:\15-9-20\a.xlsx")  
wb = xlrd.open_workbook(loc) 
sheet = wb.sheet_by_index(0)
wbWrite = xlwt.Workbook()
style = xlwt.easyxf('font: bold 1')
sheetToWrite = wbWrite.add_sheet('Reviews Count')



def process1():
    tempcountNN = 0
    try:
        for i in range(1 ,len(prepList)):
            sheetToWrite.write(0, i, prepList[i],style)

        for read in range(sheet.nrows):
            tempIndexList = []
            txt1=sheet.cell_value(read, 0)
                    # Special Character removing from source file 
            without_special = re.sub("[^A-Za-z0-9*\:\u2019-]+" , ' ' , str(txt1))
            #print(without_special)
            # Word Count from source file 
            split_string = without_special.split()
            length_list=len(split_string)

           
            word_tokens = word_tokenize(without_special)
            tagged=nltk.pos_tag(word_tokens)
            counts = Counter( tag for word,  tag in tagged)
            print(counts)
            sheetToWrite.write(read+1, 0, without_special)
            for i in counts.elements():
                if i in prepList:
                    column = prepList.index(i)
                    if not column in tempIndexList:
                        if column!=0:
                            sheetToWrite.write(read+1, column, counts[i])
                            tempIndexList.append(column)
                else:
                    print("ERROR")
        wbWrite.save("Review Count.xls")   
            #print(nltk.help.upenn_tagset())


    except Exception as e:
        print(str(e))

process1()

