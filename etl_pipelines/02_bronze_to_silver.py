from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, isnan

spark = SparkSession.builder \
    .appName("HealthFinance-SilverTransform") \
    .getOrCreate()

BRONZE_S3_PATH = "s3a://health-finance-datalake/bronze/health_insurance/"
SILVER_S3_PATH = "s3a://health-finance-datalake/silver/health_insurance/"

def process_silver():
    print("Reading from Bronze layer...")
    df = spark.read.format("delta").load(BRONZE_S3_PATH)

    # Data Quality Checks & Handling Data Drift
    print("Applying schema validation and cleaning nulls...")
    df_cleaned = df.filter(col("age").isNotNull() & (col("age") > 0)) \
                   .withColumn("bmi", when(isnan(col("bmi")), 0.0).otherwise(col("bmi"))) \
                   .withColumn("smoker_flag", when(col("smoker") == "yes", 1).otherwise(0))

    print("Writing to Silver layer (Optimized Parquet/Delta)...")
    df_cleaned.write.format("delta").mode("overwrite").save(SILVER_S3_PATH)
    print("Silver transformation complete.")

if __name__ == "__main__":
    process_silver()
