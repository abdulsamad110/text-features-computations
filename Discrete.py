import re
import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

import collections
from collections import Counter
from nltk.corpus import state_union
from nltk.tokenize import word_tokenize
import xlrd
import string
import re
import xlwt
import os
from xlwt import Workbook 

wordnet_lemmatizer = WordNetLemmatizer()
punctuations = "?:!.,;"

def stopword_removal(token):
    tokens_without_sw = [word for word in token if not word in stopwords.words()]
    return tokens_without_sw

def lemmitization(token):
    token = wordnet_lemmatizer.lemmatize(token, pos="v")
    return token

def output_to_csv(file_name, data_list, review_df):
    df = pd.DataFrame(data_list)
    df = df.fillna(0)
    df.index.name = "Review #"
    df['body'] = review_df['body']
    cols = df.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    df = df[cols]
    df.to_csv(file_name)



def discrete_emotion():
  filtered_list=[]
  seperate_counters = []
  count=0
  total = 0
  length_list=0
  wbWrite = xlwt.Workbook()      #Allow accesss to xlsx file
  style = xlwt.easyxf('font: bold 1')          #First row of output xls will be bold
  
  prepList = ["","Joy","Anger","Anticipation","Anxiety","Disgust","Sadness","Surprize","Trust"]    #First Row
  print (os.path.dirname(os.path.abspath(__file__)))
                   # XLSX formatted source file reading Source
  for FilesCounter in range(1 , 8):   #no need of the for loop in our dataset, this is for when we have 10 columns
    sheetToWrite = wbWrite.add_sheet(prepList[FilesCounter])    #sheet name
    Review_df = pd.read_csv("D:/Data.csv")

                    # Reading of emotions source file in XLSX formate
    for i in range(1 ,len(prepList)):
        sheetToWrite.write(0, i, prepList[i],style)
   
    
    wbjoy = xlrd.open_workbook("D:/Laxicons/"+ prepList[FilesCounter] +".xlsx") #Joy laxicon reading from xlsx format
    print("ON LAXICON",prepList[FilesCounter])
    
    discrete_emotion_list = [];         
    for read in range(12500):  #loop till the last row of sheet
            print("##################")
            print("ON VALUE",read)
            sheetjoy = wbjoy.sheet_by_index(0)      #First column      
            sumOfJoy = 0
            percentage = 0
            addedSum= []
            addedRow= []
            addedColumn= []
            txt1 = Review_df['body'].tolist()[read];
            without_special = re.sub("[^A-Za-z0-9*\.\u2019-]+" , ' ' , str(txt1))  #This will remove special character from sheet
                       # Word Count from source file 
            split_string = without_special.split()  #split() method splits a string into a list
            length_list=len(split_string)      #len() function returns the number of items in an object  
                        # Stop word removal from source file 
            stop_words = set(stopwords.words('english'))  #English tokenization
            word_tokens = word_tokenize(without_special) #tokenization of one sentence/review
           
            tempList= []
            for words in word_tokens:    #for loop for each tokenize word in a sentence/review 
                
                if words not in stop_words:
                    tempList.append(words) #join each words after removing stopwords
            filtered_list.append(tempList) 
                                    # Comparison and Match Count
            tempRow = read+1
            sheetToWrite.write(tempRow, 0, without_special)  #This is for writing sentence/review in the first column of output sheet

            for i in filtered_list:
                same_values_counter = []
                for k in i:    
                    wcount = 0
                    for j in range(sheetjoy.nrows):   #For loop for the row of joy
                        if k == sheetjoy.cell_value(j, 0):  #This will compare the Each word in a sentence/review with the laxicon of joy
                            same_values_counter.append(k)   #This will save value in the above array same_values_counter = []
            filtered_list = []
            counts = Counter(same_values_counter)
            for count in counts.elements():
                if not count in addedSum:
                    sumOfJoy = sumOfJoy+counts[count]   #sum of joy words in an each sentence/review
                    addedSum.append(count)
            percentage = round((sumOfJoy*100)/length_list,4)  #this will find percentage of the joy word in an each row, percentage is not compulsory we can only show the counts also
            sheetToWrite.write(read+1, prepList.index("Joy"), percentage)  #sheetToWrite.write(row + 1, write in index of Joy, value to write)
            discrete_emotion_list.append(percentage)
    output_to_csv('EmoSheet.csv', discrete_emotion_list, Review_df)
              
    

discrete_emotion()
