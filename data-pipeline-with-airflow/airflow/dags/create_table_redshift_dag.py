from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.postgres_operator import PostgresOperator

from load_data_from_s3_to_redshift import default_args

dag = DAG('Create_table',
          default_args=default_args,
          description='Create table in the redshift or postgres with Airflow'
        )

start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)

create_table_task = PostgresOperator(
	task_id = 'create_table_redshift_or_postgres',
	dag = dag,
	sql = '../../create_table.sql'
)

end_operator = DummyOperator(task_id='Stop_execution', dag=dag)

# Order of tasks
start_operator >> create_table_task >> end_operator

