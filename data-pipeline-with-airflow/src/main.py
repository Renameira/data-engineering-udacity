from sqlalchemy_schemadisplay import create_schema_graph
from sqlalchemy import MetaData
from config import Settings




def generator_erd():
    """
    Generate the ER diagram using sqlalchemy_schemadisplay.

    Returns: The png image with the database schema in assets file.
    """
    graph = create_schema_graph(metadata=MetaData(Settings.CONNECTION_STRING_SPARKIFYDB))
    return graph.write_png("./images/sparkify_erd.png")





generator_erd()
