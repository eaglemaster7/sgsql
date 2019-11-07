import sqlite3
import shotgun_api3


def sql_execute_script(db_file, command):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    return_value = c.executescript(command).fetchall()
    conn.commit()
    return return_value


def sql_execute(db_file, command):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    return_value = c.execute(command).fetchall()
    conn.commit()
    return return_value


def sql_execute_many(db_file, command,sequence_data):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.executemany(command,sequence_data)
    conn.commit()


def get_sg_object(address,script_name,api_key):
    return shotgun_api3.Shotgun(address,script_name=script_name,api_key=api_key)