from datetime import datetime
import airflow.models
import utils.helpers as helpers

args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2016, 12, 1),
    'retries': 1,
}

dag = airflow.models.DAG(
    dag_id='ictrp',
    default_args=args,
    max_active_runs=1,
    schedule_interval='@monthly'
)

collector_task = helpers.create_collector_task(
    name='ictrp',
    dag=dag,
    environment={
        'ICTRP_USER': airflow.models.Variable.get('ICTRP_USER'),
        'ICTRP_PASS': airflow.models.Variable.get('ICTRP_PASS'),
    }
)

processor_task = helpers.create_processor_task(
    name='ictrp',
    dag=dag
)

merge_trials_identifiers_task = helpers.create_processor_task(
    name='merge_trials_identifiers',
    dag=dag
)

processor_task.set_upstream(collector_task)
merge_trials_identifiers_task.set_upstream(processor_task)
