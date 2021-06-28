from airflow import DAG

from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator
from datetime import datetime, timedelta


args = {
    'owner': 'airflow',
    'start_date': datetime(2021, 6, 28)
}
dag = DAG('spark_job', default_args=args, schedule_interval="@daily")

scala_spark_example = SparkSubmitOperator(
    java_class="org.kylg.dbiv.AppRunner",
    application="hdfs:/tmp/edwin/dbivp1-1.0-SNAPSHOT-jar-with-dependencies.jar",
    task_id="submit_scala_spark_pi",
    name='airflowspark-submittest',
    dag=dag)