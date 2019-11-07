import sgsql
import util
import shotgun_api3

sgo = shotgun_api3.Shotgun("https://mnca.shotgunstudio.com",
                           script_name	="mncaAccess",
                           api_key		="53fbc8b53012e7677d23afb4ce15ce53f728f29ce0c58d6a9cfff503bcdb1e28")

'''
filter = [["project", "is", {"type": "Project", "id": 170}]]
fields = ["content", "entity", "id", "sg_status_list", "updated_at", "updated_by"]
sgsql.create_db_from_sg("c:/bak3/fff.db",sgo,"Task",filter,fields)
'''

filter = [["project", "is", {"type": "Project", "id": 170}]]
fields = ["id","code","sg_sequence","sg_cut_out"]
sgsql.write_to_db("c:/bak3/jjxb.db",sgo,"Shot",filter,fields)

