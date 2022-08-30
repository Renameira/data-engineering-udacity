from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadDimensionOperator(BaseOperator):

    ui_color = '#80BD9E'

    @apply_defaults
    def __init__(self,
                redshift_conn_id= "",
                table = "",
                sql_query = "",
                mode="append-only",
                *args, 
                **kwargs
                ):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.sql_query = sql_query
        self.mode = mode

    def execute(self, context):
        self.log.info("Connecting to Redshift")
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        sql_insert = ""
        if self.mode == "append-only":
            sql_insert = """
                    BEGIN;
                    INSERT INTO {}
                    {};
                    """.format(self.table, self.sql_query)
        else:
            sql_insert = """
                    BEGIN;
                    TRUNCATE TABLE {}; 
                    INSERT INTO {}
                    {};
                    """.format(self.table, self.table, self.sql_query)
            
        redshift.run(sql_insert)
