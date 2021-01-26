#!/usr/bin/env python
# coding: utf-8

# In[1]:


from pyspark import SparkContext
from pyspark.streaming import StreamingContext

if __name__ == "__main__":
    # Create a local StreamingContext with two working thread and batch interval of 1 second
    sc = SparkContext("local[2]", "NetworkWordCount")
    ssc = StreamingContext(sc, 1)

    # Create a DStream that will connect to hostname:port, like localhost:9999
    lines = ssc.socketTextStream("127.0.0.1", 1117)
    lines.pprint()
    ssc.start()             # Start the computation
    ssc.awaitTermination()  # Wait for the computation to terminate


# In[ ]:




