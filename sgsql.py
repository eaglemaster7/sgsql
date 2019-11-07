import os
import util


def write_to_db(db_file_output_path, sg_script_instance_object, sg_entity, sg_filters, sg_fields):
    """
    :param db_file_output_path: database file destination
    :param sg_script_instance_object: shotgun object, see : shotgun initialization page
    :param sg_entity: entity name like 'Task' or 'Asset' or something
    :param sg_filters: see : shotgun filters on sg.find()
    :param sg_fields: see : shotgun fields on sg.find()

    the behaviour will be:
    - due to sqlite native data type some unknown shotgun data type will be convert to TEXT data type
    - if record on db_file is exist, insertion will not overwrite existing data but will created anew
    - if using existing db_file insertion will automatically add new field if necessary
    """

    def flatten_json_one_level(fields,data_dict):

        fin=[]
        for item in data_dict:
            pair=[]
            for f in fields:
                val=item[f]
                if isinstance(val, dict):  # if second level is not flat then use 'name' key
                    pair.append(str(item[f]['name']))
                else:
                    pair.append(str(item[f]))
            fin.append(tuple(pair))
        return fin

    def convert_to_sql_data_type(sg_data_type_input):
        """
        some will convert to TEXT datatype
        """
        ret_val = None
        if sg_data_type_input == 'text':
            ret_val = 'TEXT'
        elif sg_data_type_input == 'number':
            ret_val = 'NUMERIC'
        elif sg_data_type_input == 'date':
            ret_val = 'TEXT'
        elif sg_data_type_input == 'entity':
            ret_val = 'TEXT'
        else:
            ret_val = 'TEXT'
        return ret_val

    def create_sql_creation_syntax(dict_field_data_type):
        x = []
        for i in dict_field_data_type:
            x.append(i+' '+dict_field_data_type[i])
        y = ','.join(x)
        sql_table_creation = '''CREATE TABLE IF NOT EXISTS {0} ({1})'''.format(sg_entity, y)
        return sql_table_creation

    def read_data_types_from_sg(entity, fields):
        """

        :param entity: sg_entity
        :param fields: list of sg_fields []
        :return: dictionary of {field : data_type}
        """
        field_data_type_dict = {}
        all_field_schema = sg_script_instance_object.schema_field_read(entity)
        for field in fields:
            sg_data_type = all_field_schema[field]['data_type']['value']
            sql_data_type = convert_to_sql_data_type(sg_data_type)
            field_data_type_dict[field] = sql_data_type
        return field_data_type_dict

    sg_find_result = sg_script_instance_object.find(sg_entity, sg_filters, sg_fields)

    # make sure folder that on db_file exist / created before
    dir_name = os.path.dirname(db_file_output_path)
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

    #
    # step 1 read all data type and  create table ----------------------------------------------------------------------
    field_data_type_dict = read_data_types_from_sg(sg_entity, sg_fields)  # get the sql data type from sg data type
    sql_creation = create_sql_creation_syntax(field_data_type_dict)  # get the sql creation string
    util.sql_execute(db_file_output_path, sql_creation)  # actual execute to create table

    #
    # step 3 make sure old table has all the column required for insertion if not then alter to add new column----------
    sql = "PRAGMA TABLE_INFO('{0}')".format(sg_entity)
    sql_original_table_schema = util.sql_execute(db_file_output_path, sql)

    sql_original_table_creation_columns = []

    for column_info in sql_original_table_schema:
        sql_original_table_creation_columns.append(column_info[1])

    new_column_differences = [i for i in sg_fields if i not in sql_original_table_creation_columns]

    for new_column in new_column_differences:
        new_field_data_type_dict = read_data_types_from_sg(sg_entity,new_column_differences)
        util.sql_execute(db_file_output_path, "ALTER TABLE '{0}' ADD COLUMN '{1}' {2}".format(
            sg_entity, new_column, new_field_data_type_dict[new_column]))

    #
    # step 4 execute many insertions -----------------------------------------------------------------------------------

    z = flatten_json_one_level(sg_fields, sg_find_result)
    x = []
    for i in range(len(sg_fields)):
        x.append('?')
    string_char = ','.join(x)
    cmd = '''INSERT INTO {0} ({1}) values ({2})'''.format(sg_entity,",".join(sg_fields),string_char)
    util.sql_execute_many(db_file_output_path, cmd, z)



def insertDataFromSQLTable2SG(table_data,sg_instance_object):
    pass