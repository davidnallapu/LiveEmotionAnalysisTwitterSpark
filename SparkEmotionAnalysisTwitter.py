import pandas as pd
import numpy as np
import os
os.environ["JAVA_HOME"] = "/Library/Java/JavaVirtualMachines/adoptopenjdk-8.jdk/Contents/Home"
os.environ["PATH"] = os.environ["JAVA_HOME"] + "/bin:" + os.environ["PATH"]
import json
from pyspark.ml import Pipeline
from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from sparknlp.annotator import *
from sparknlp.base import *
import sparknlp
from sparknlp.pretrained import PretrainedPipeline
import collections
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

spark = sparknlp.start()

MODEL_NAME='classifierdl_use_emotion'

documentAssembler = DocumentAssembler()\
    .setInputCol("text")\
    .setOutputCol("document")
    
use = UniversalSentenceEncoder.pretrained(name="tfhub_use", lang="en")\
 .setInputCols(["document"])\
 .setOutputCol("sentence_embeddings")


sentimentdl = ClassifierDLModel.pretrained(name=MODEL_NAME)\
    .setInputCols(["sentence_embeddings"])\
    .setOutputCol("sentiment")

nlpPipeline = Pipeline(
      stages = [
          documentAssembler,
          use,
          sentimentdl
      ])


def predict_emotion():
    empty_df = spark.createDataFrame([['']]).toDF("text")
    pipelineModel = nlpPipeline.fit(empty_df)
    df = spark.createDataFrame(pd.DataFrame({"text":text_list}))
    result = pipelineModel.transform(df)
#     result.select(F.explode(F.arrays_zip('document.result', 'sentiment.result')).alias("cols")) \
#     .select(F.expr("cols['0']").alias("document"),
#         F.expr("cols['1']").alias("sentiment")).show(truncate=False)
    #Getting a list of emotions
    emotions = []
    for i in result.select(F.collect_list('sentiment')).first()[0]:
        emotions.append(str(i[0].result))

    #Getting a count of the emotions
    
    counter=collections.Counter(emotions)
    print(counter)
    
    
    # return counter
    #Visualisation
#     labels, values = zip(*counter.items())

#     indexes = np.arange(len(labels))
#     width = 1
#     import matplotlib.pyplot as plt
#     plt.bar(indexes, values, width)
#     plt.xticks(indexes + width * 0.5, labels)
#     if(len(text_list)%10==0):
#         plt.show()
def animate_framed(i):
    if(len(text_list)>1):
        empty_df = spark.createDataFrame([['']]).toDF("text")
        pipelineModel = nlpPipeline.fit(empty_df)
        df = spark.createDataFrame(pd.DataFrame({"text":text_list}))
        result = pipelineModel.transform(df)
        emotions = []
        for i in result.select(F.collect_list('sentiment')).first()[0]:
            emotions.append(str(i[0].result))

        #Getting a count of the emotions
        counter = collections.Counter(emotions)
        labels, values = zip(*counter.items())
        indexes = np.arange(len(labels))
        width = 1
        plt.bar(indexes, values, width)
        plt.xticks(indexes + width * 0.5, labels)
    

    
import time
import os
import re

def follow(thefile):
    '''generator function that yields new lines in a file
    '''
    # seek the end of the file
    thefile.seek(0, os.SEEK_END)
    
    # start infinite loop
    while True:
        # read last line of file
        line = thefile.readline()
        # sleep if file hasn't been updated
        if not line:
            time.sleep(0.1)
            continue
        yield line

    
        
        
import time
import os
import re

text_list = []
counter = dict()
def follow(thefile):
    '''generator function that yields new lines in a file
    '''
    # seek the end of the file
    thefile.seek(0, os.SEEK_END)
    
    # start infinite loop
    while True:
        # read last line of file
        line = thefile.readline()
        # sleep if file hasn't been updated
        if not line:
            time.sleep(0.1)
            continue
        yield line

    
        
        
if __name__ == '__main__':
    logfile = open("tweets.txt","r")
    loglines = follow(logfile)
    fig = plt.figure()
    ax = plt.gca()
    # animation = FuncAnimation(fig, func=animate_framed, fargs=(counter,), interval=10)
    animation = FuncAnimation(fig, func=animate_framed, interval=1000)
    plt.show()
    # iterate over the generator
    for s in loglines:
        re.sub("\S*\d\S*", "", s).strip()
        tokens = s.strip().split()
        clean_tokens = [t for t in tokens if re.match(r'[^\W\d]*$', t)]
        clean_s = ' '.join(clean_tokens)
        
        if(len(clean_s.split(' '))>1):
            text_list.append(clean_s)
            predict_emotion()
            
            