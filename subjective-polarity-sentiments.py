import collections
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.corpus import state_union
from nltk.tokenize import word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import xlrd
import xlwt
import string
import re
from textblob import TextBlob


filtered_list=[]
seperate_counters = []
same_values_counter = []
count=0
length_list=0

                # XLSX formatted source file reading Source
                
loc = ("Data.xlsx")  
wb = xlrd.open_workbook(loc) 
sheet = wb.sheet_by_index(0)
ww=xlwt.Workbook()
ws=ww.add_sheet("Dev Sentiment", cell_overwrite_ok=True)
sid_obj = SentimentIntensityAnalyzer() 



for read in range(sheet.nrows):
    print("#############")
    print("Article # = " + str(read))
    print("#############")
    txt1=sheet.cell_value(read, 0)
                    # Special Character removing from source file 
    without_special = re.sub("[^A-Za-z0-9*\.\u2019-]+" , ' ' , str(txt1))
    sentiment_dict = sid_obj.polarity_scores(without_special)
    analysis=TextBlob(without_special)
    sentiment=(sentiment_dict['pos'] - sentiment_dict['neg']) - 0.02

    #Colums Name
    ws.write(0,0,"Reviews")
    ws.write(0,1,"Polarity")
    ws.write(0,2,"Sentiment")
    ws.write(0,3,"Subjectivity")


    #Data Filling
    ws.write(read,0,without_special)
    ws.write(read,1,analysis.sentiment[0])
    ws.write(read,2,sentiment)
    ws.write(read,3,analysis.sentiment[1])

ww.save("Sentiment1.xls")
 

    



