import json
import os
from dataclasses import asdict
import psycopg2
from psycopg2 import extras
from ....shared.DTO.context_data import ContextDTO
from .validate_postgres import validate_context_dto 

# Global variables to hold the PostgreSQL connection
conn = None
table_name = None  # Store the table name globally

def initialize_postgres_db(config_path='config.json'):
    """
    Initializes the PostgreSQL connection using settings from the config.json file.
    """
    global conn, table_name
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_file_path = os.path.join(current_dir, config_path)
    
    with open(config_file_path, 'r') as file:
        config = json.load(file)
    
    conn = psycopg2.connect(config['postgres_uri'])
    table_name = config['postgres_table_name']

def add_postgres_data(context_dto: ContextDTO):
    """
    Add a new entry to the PostgreSQL database using the provided ContextDTO object.
    :param context_dto: An instance of ContextDTO representing the data to be stored.
    :return: The ID of the newly added item.
    """
    validate_context_dto(context_dto)

    cursor = conn.cursor()
    # Prepare the SQL query with placeholders for each field in the DTO
    fields = ', '.join([field for field in asdict(context_dto) if getattr(context_dto, field) is not None])
    values = [getattr(context_dto, field) for field in asdict(context_dto) if getattr(context_dto, field) is not None]
    placeholders = ', '.join(['%s'] * len(values))

    sql = f"INSERT INTO {table_name} ({fields}) VALUES ({placeholders}) RETURNING id;"
    cursor.execute(sql, tuple(values))
    new_id = cursor.fetchone()[0]  # Fetch the ID of the newly added entry
    conn.commit()  # Commit the transaction
    cursor.close()
    return new_id

def get_postgres_data(id):
    """
    Retrieve an entry from the PostgreSQL database based on its ID.
    :param id: The ID of the document to retrieve.
    :return: The document retrieved from the database.
    """
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    sql = f"SELECT * FROM {table_name} WHERE id = %s;"
    cursor.execute(sql, (id,))
    document = cursor.fetchone()
    cursor.close()
    return parse_to_context_dto(document)



def parse_to_context_dto(db_row):
    """
    Parses database row data into a ContextDTO instance.
    
    :param db_row: A list containing the database row data.
    :return: An instance of ContextDTO populated with the database data.
    """
    if db_row:
        return ContextDTO(
            id=str(db_row[0]),
            tags=db_row[1],
            convo_id=db_row[2],
            user_id=db_row[3],
            conversation_date=db_row[4],
            last_updated=db_row[5],
            last_mentioned=db_row[6],
            status=db_row[7]
        )
    else:
        return None
    

def rollback_postgres_data(document_id):
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM context WHERE id = %s;", (document_id,))
            conn.commit()
    except Exception as e:
        print(f"Failed to rollback PostgreSQL data: {str(e)}")
        conn.rollback()
