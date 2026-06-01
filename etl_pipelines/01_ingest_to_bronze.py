from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp

# Initialize Spark Session for Databricks/AWS EMR
spark = SparkSession.builder \
    .appName("HealthFinance-BronzeIngestion") \
    .getOrCreate()

# AWS S3 Paths (Simulated Cloud Datalake)
RAW_S3_PATH = "s3a://health-finance-datalake/raw/health_insurance_data.csv"
BRONZE_S3_PATH = "s3a://health-finance-datalake/bronze/health_insurance/"

def ingest_to_bronze():
    print("Reading raw data from AWS S3...")
    df_raw = spark.read.csv(RAW_S3_PATH, header=True, inferSchema=True)

    # Data Lineage / Governance: Adding Ingestion Metadata
    df_bronze = df_raw.withColumn("ingestion_timestamp", current_timestamp())

    print("Writing to Bronze layer (Delta format)...")
    # Saving in Delta format for ACID transactions on Datalake
    df_bronze.write.format("delta").mode("overwrite").save(BRONZE_S3_PATH)
    print("Bronze ingestion complete.")

if __name__ == "__main__":
    ingest_to_bronze()
