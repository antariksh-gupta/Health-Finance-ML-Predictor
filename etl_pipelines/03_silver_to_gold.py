from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, count, round

spark = SparkSession.builder \
    .appName("HealthFinance-GoldAnalytics") \
    .getOrCreate()

SILVER_S3_PATH = "s3a://health-finance-datalake/silver/health_insurance/"
GOLD_S3_PATH = "s3a://health-finance-datalake/gold/risk_features/"

def build_gold_layer():
    print("Reading clean data from Silver layer...")
    df_silver = spark.read.format("delta").load(SILVER_S3_PATH)

    # Feature Engineering & Aggregations for BI / ML Forecasting
    print("Generating Risk Analytics Features...")
    df_gold = df_silver.groupBy("region", "smoker_flag") \
                       .agg(
                           round(avg("charges"), 2).alias("avg_premium_cost"),
                           round(avg("bmi"), 2).alias("avg_bmi"),
                           count("*").alias("total_customers")
                       )

    print("Writing to Gold layer for Unity Catalog & Serving...")
    df_gold.write.format("delta").mode("overwrite").save(GOLD_S3_PATH)
    print("Gold layer ready for Power BI & ML Prediction.")

if __name__ == "__main__":
    build_gold_layer()
