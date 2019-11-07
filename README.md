# sgsql
want to manipulate or store Shotgun data with SQLITE ? this module can simplify it all for you
this is the first commit, there are just one fully functional module, that is ```write_to_db``` , I will definitely add it later

usage:
```
import sgsql
sgsql.write_to_db(db_file_output_path, sg_script_instance_object, sg_entity, sg_filters, sg_fields):
```

it just like [sg.find()](https://developer.shotgunsoftware.com/python-api/reference.html) but it will pass the result to SQLITE output database, completed with it's table name and data type

disclaimer :
- due to sqlite native data type some unknown shotgun data type will be convert to TEXT data type
- if record on db_file is exist, insertion will not overwrite existing data but will created anew
- if using existing db_file insertion will automatically add new field if necessary
