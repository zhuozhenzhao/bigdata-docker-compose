from airflow import DAG

from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator
from datetime import datetime, timedelta


args = {
    'owner': 'airflow',
    'start_date': datetime(2021, 6, 28)
}
dag = DAG('spark_job', default_args=args, schedule_interval="@daily", max_active_runs=1)

scala_spark_example = SparkSubmitOperator(
    java_class="org.kylg.dbiv.AppRunner",
    application="hdfs:/tmp/edwin/dbivp1-1.0-SNAPSHOT-jar-with-dependencies.jar",
    task_id="submit_scala_spark_pi",
    name='airflowspark-submittest',
    dag=dag,
    jars='/usr/spark/jars/spark-2.4-spline-agent-bundle_2.11-0.6.1.jar,/usr/spark/jars/commons-configuration-1.6.jar',
    #packages='za.co.absa.spline.agent.spark:spark-2.4-spline-agent-bundle_2.12:0.6.1',
    conf={'spark.sql.queryExecutionListeners':'za.co.absa.spline.harvester.listener.SplineQueryExecutionListener', 'spark.spline.lineageDispatcher.http.producer.url':'http://spline_server:8080/producer'})