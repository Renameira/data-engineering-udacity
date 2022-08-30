from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):

    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id,
                 tables,
                 *args, 
                 **kwargs
                ):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.tables = tables

    def execute(self, context):
        redshift_hook = PostgresHook(self.redshift_conn_id)
        for table in self.tables:
            checks = [
                {'test_sql': f'SELECT COUNT(*) FROM {table}', 'expected_result': 0, 'comparison': '==', 'element_comparison': 'records[0][0]', 'explanation error' : ' contained 0 rows'},
        ]
            for i, dq_check in enumerate(checks):
                records = redshift_hook.get_records(dq_check['test_sql'])
                print(type(records))
                print(records)
                if not f"{dq_check['expected_result']} {dq_check['comparison']} {dq_check['element_comparison']} ":
                    raise ValueError(f"Data quality #{i} failed. {table} {dq_check['explanation error']}.")
            self.log.info(f"Data quality on table {table} check passed with {records[0][0]} records")
