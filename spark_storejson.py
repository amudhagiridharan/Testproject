# program to write (insert/upsert) JSON to MongoDB using Spark
from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql import SQLContext
import requests
import json
from pyspark.sql import functions as F
from urllib.request import Request, urlopen

#Set mongodb variables
mongodburi = "mongodb://localhost/newtestdb.AI"

my_spark = SparkSession.builder.master("local[*]").appName("myApp") \
    .config("spark.mongodb.input.uri", mongodburi) \
    .config("spark.mongodb.output.uri", mongodburi) \
    .config('spark.jars.packages', "org.mongodb.spark:mongo-spark-connector_2.12:3.0.1") \
    .getOrCreate()

spark = SparkSession.builder.appName("Python Spark Mongo DB write").getOrCreate()
logger = spark._jvm.org.apache.log4j
logger.LogManager.getRootLogger().setLevel(logger.Level.FATAL)


#Function to fetch json from provided url and insert into mongodb
def write_db(url):
    # Online data source
    onlineData = url

    # read the online data file
    httpData = urlopen(onlineData).read().decode('utf-8')
    print(httpData)
    # convert into RDD
    rdd = spark.sparkContext.parallelize([httpData])

    # create a Dataframe
    jsonDF = spark.read.json(rdd)
    jsonDF.write.format('com.mongodb.spark.sql.DefaultSource').mode("append").save()
    return("write successful")

#writes the input json value to db
def write_json(jsonval):
    print(jsonval)
    # convert into RDD
    rdd = spark.sparkContext.parallelize([jsonval])

    # create a Dataframe
    jsonDF = spark.read.json(rdd)
    jsonDF.write.format('com.mongodb.spark.sql.DefaultSource').mode("append").save()
    return ("write successful")

#writes the upsert json value in db
#_id should be part of JSON provided
def update_results(jsonval):
    print(jsonval)
    # convert into RDD
    rdd = spark.sparkContext.parallelize([jsonval])

    # create a Dataframe
    jsonDF = spark.read.json(rdd)
    jsonDF.write.format('com.mongodb.spark.sql.DefaultSource').mode("append").option("replaceDocument", "false").save()
    return ("write successful")

if __name__ == "__main__":

    #url test
    # url = "http://127.0.0.1:5000/"
    # write_db(url)


    #Json load test

    x = '{ "_id":"dave","username":"dave", "age":30, "city":"New York","photo":"/Users/giridharangovindan/PycharmProjects/finalprojectPHOTO.jpg","result text":""}'
    y = json.loads(x)
    write_json(y)


    #update test

    x_updated = '{"_id":"dave","userid":"dave", "age":30, "city":"New York","photo":"/Users/giridharangovindan/PycharmProjects/finalprojectPHOTO.jpg","result text":"This doesnot look like melanoma probably"}'
    y_updated = json.loads(x_updated)
    update_results(y_updated)