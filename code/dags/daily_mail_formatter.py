from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.latest_only_operator import LatestOnlyOperator
from airflow.operators.python_operator import PythonOperator

from services.argus_scraper import ArgusScraper
from services import text_processing
from services.html_exporter import render_headlines_to_html
from services.image_downloader import download_random_images

PROJ_DIR = os.path.dirname(os.path.abspath(__file__))

WEBPAGE_FILE_PATH = os.path.join(PROJ_DIR, 'data/argus_news.html')
HEADLINES_FILE_PATH = os.path.join(PROJ_DIR, 'data/headlines.jsonl')
HTML_OUTPUT_FILE = os.path.join(PROJ_DIR, 'data/index.html')
IMAGE_FOLDER = os.path.join(PROJ_DIR, 'data/images')


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


apply_science = PythonOperator(
    task_id='apply_science',
    python_callable=text_processing.prove_carcinogenic_effect_with_science,
    op_kwargs={
        'headlines_file_path': HEADLINES_FILE_PATH,
        'use_actual_science': False
    },
    dag=dag
)


bigotry_enhancer = PythonOperator(
    task_id='bigotry_enhancer',
    python_callable=text_processing.discover_terrorists,
    op_kwargs={
        'headlines_file_path': HEADLINES_FILE_PATH
    },
    dag=dag
)


export_to_web = PythonOperator(
    task_id='export_to_web',
    python_callable=render_headlines_to_html,
    op_kwargs={
        'headlines_file_path': HEADLINES_FILE_PATH,
        'output_file': HTML_OUTPUT_FILE
    },
    dag=dag
)


# download_images = PythonOperator(
#     task_id='download_random_images',
#     python_callable=download_random_images,
#     op_kwargs={
#         'headlines_file_path': HEADLINES_FILE_PATH, 
#         'output_folder': IMAGE_FOLDER
#     },
#     dag=dag
# )


latest_only >> \
    download_news >> \
    extract_headlines >> \
    apply_science >> \
    bigotry_enhancer >> \
    export_to_web


# extract_headlines >> \
#     download_images >> \
#     export_to_web
