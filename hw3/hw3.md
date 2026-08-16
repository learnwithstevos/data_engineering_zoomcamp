Module 3 Homework: Data Warehousing & Athena/Glue
============================================

1) What is count of records for the 2024 Yellow Taxi Data?
![Question 1 Answer](hw3_images/hw3_q1.png)

2) Write a query to count the distinct number of PULocationIDs for the entire dataset on both the tables. What is the estimated amount of data that will be read when this query is executed on the External Table and the Table?

    Ans: Athena doesn't have this feature in AWS but for Bigquery the answer is: 0 MB for the External Table and 155.12 MB for the Materialized Table

3) Write a query to retrieve the PULocationID from the table (not the external table) in BigQuery. Now write a query to retrieve the PULocationID and DOLocationID on the same table. Why are the estimated number of Bytes different?

    Ans: BigQuery is a columnar database, and it only scans the specific columns requested in the query. Querying two columns (PULocationID, DOLocationID) requires reading more data than querying one column (PULocationID), leading to a higher estimated number of bytes processed.

4) What is count of records for the 2024 Yellow Taxi Data?
![Question 1 Answer](hw3_images/hw3_q4.png)

5) What is the best strategy to make an optimized table in Big Query if your query will always filter based on tpep_dropoff_datetime and order the results by VendorID (Create a new table with this strategy)

    Ans: Partition by tpep_dropoff_datetime and Cluster on VendorID

6) Write a query to retrieve the distinct VendorIDs between tpep_dropoff_datetime 2024-03-01 and 2024-03-15 (inclusive)
Use the materialized table you created earlier in your from clause and note the estimated bytes. Now change the table in the from clause to the partitioned table you created for question 5 and note the estimated bytes processed. What are these values?

    Ans: 183.96 MB for non-partitioned table and 326.02 MB for the partitioned table
    ![Question 6 Answer](hw3_images/hw3_q6_v1.png)
    ![Question 6 Answer](hw3_images/hw3_q6_v2.png)



7) Where is the data stored in the External Table you created?
Ans: s3

8) It is best practice in Athena to always cluster your data:
Ans: False

9) Write a SELECT count(*) query FROM the materialized table you created. How many bytes does it estimate will be read? Why? 

    0 - because count(*) does not need to read any column data
        ![Question 9 Answer](hw3_images/hw3_q9.png)
