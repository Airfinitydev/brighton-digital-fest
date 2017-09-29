from airflow import DAG
from airflow.operators.latest_only_operator import LatestOnlyOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2017, 9, 27),
    'email': ['airflow@airflow.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'daily_mailiser',
    default_args=default_args,
    schedule_interval='@daily'
)

latest_only = LatestOnlyOperator(task_id='latest_only', dag=dag)


download_news = PythonOperator(
    task_id='download_news',
    python_executable=argus_news_scraper,
    dag=dag
)


extract_headlines = PythonOperator(
    task_id='extract_headlines',
    dag=dag
)


add_hate = PythonOperator(
    task_id='add_hate',
    dag=dag
)


bigotry_enhancer = PythonOperator(
    task_id='bigotry_enhancer',
    dag=dag
)


fear_mongering_filter = PythonOperator(
    task_id='fear_mongering_filter',
    dag=dag
)


merge_with_real_headlines = PythonOperator(
    task_id='merge_with_real_headlines',
    dag=dag
)


export_to_web = PythonOperator(
    task_id='export_to_web',
    dag=dag
)


latest_only >> \
    download_webpage >> \
        extract_headlines >> \
            add_hate >> \
                bigotry_enhancer >> \
                    fear_mongering_filter >> \
                        merge_with_real_headlines >> \
                            export_to_web
