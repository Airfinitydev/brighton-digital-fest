from airflow import DAG
from airflow.operators.latest_only_operator import LatestOnlyOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

from services.argus_scraper import ArgusScraper
from services.text_processing import prove_carcinogenic_effect_with_science

WEBPAGE_FILE_PATH = '/usr/local/airflow/dags/data/argus_news.html'
HEADLINES_FILE_PATH = '/usr/local/airflow/dags/data/headlines.jsonl'


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
    python_callable=ArgusScraper.save_webpage_to_file,
    op_kwargs={
        'url': 'http://www.theargus.co.uk/news/',
        'file_path': WEBPAGE_FILE_PATH
    },
    dag=dag
)


extract_headlines = PythonOperator(
    task_id='extract_headlines',
    python_callable=ArgusScraper.extract_headlines,
    op_kwargs={
        'input_file': WEBPAGE_FILE_PATH,
        'output_file': HEADLINES_FILE_PATH
    },
    dag=dag
)


apply_bs = PythonOperator(
    task_id='apply_bs',
    python_callable=prove_carcinogenic_effect_with_science,
    op_kwargs={
        'headlines_file_path': HEADLINES_FILE_PATH,
        'use_actual_science': False
    },
    dag=dag
)


# bigotry_enhancer = PythonOperator(
#     task_id='bigotry_enhancer',
#     dag=dag
# )


# fear_mongering_filter = PythonOperator(
#     task_id='fear_mongering_filter',
#     dag=dag
# )


# merge_with_real_headlines = PythonOperator(
#     task_id='merge_with_real_headlines',
#     dag=dag
# )


# export_to_web = PythonOperator(
#     task_id='export_to_web',
#     dag=dag
# )


latest_only >> \
    download_news >> \
    extract_headlines >> \
    apply_bs # >> \
    # bigotry_enhancer >> \
    # fear_mongering_filter >> \
    # merge_with_real_headlines >> \
    # export_to_web
