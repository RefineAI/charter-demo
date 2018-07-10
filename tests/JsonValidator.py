import json
str = {u'status': {u'code': 10000, u'description': u'Ok'}, u'outputs': [{u'status': {u'code': 10000, u'description': u'Ok'}, u'created_at': u'2017-04-09T14:59:55.844543Z', u'input': {u'data': {u'image': {u'url': u'https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcRTDkTI5R040B327idli7L_o-MtGv0lCwDxZyZwJKSddOPHyXO6'}}, u'id': u'bdf2c6780b5b485da0933031e32394d9'}, u'model': {u'name': u'general-v1.3', u'output_info': {u'type_ext': u'concept', u'message': u'Show output_info with: GET /models/{model_id}/output_info', u'type': u'concept'}, u'created_at': u'2016-03-09T17:11:39.608845Z', u'app_id': None, u'model_version': {u'status': {u'code': 21100, u'description': u'Model trained successfully'}, u'created_at': u'2016-07-13T01:19:12.147644Z', u'id': u'aa9ca48295b37401f8af92ad1af0d91d', u'active_concept_count': 9171}, u'id': u'aaa03c23b3724a16a56b629203edc62c'}, u'data': {u'concepts': [{u'app_id': None, u'id': u'ai_gRZHdRD7', u'value': 0.9967743, u'name': u'wheel'}, {u'app_id': None, u'id': u'ai_TZ3C79C6', u'value': 0.9962605, u'name': u'road'}, {u'app_id': None, u'id': u'ai_QwfPt5x7', u'value': 0.9923259, u'name': u'cyclist'}, {u'app_id': None, u'id': u'ai_QN2GGtJC', u'value': 0.97610474, u'name': u'seated'}, {u'app_id': None, u'id': u'ai_TjbmxC6B', u'value': 0.97525275, u'name': u'tree'}, {u'app_id': None, u'id': u'ai_zXhVrrgw', u'value': 0.9641051, u'name': u'lifestyle'}, {u'app_id': None, u'id': u'ai_z6Q5H2Lq', u'value': 0.9585372, u'name': u'biker'}, {u'app_id': None, u'id': u'ai_8Qw6PFLZ', u'value': 0.95838445, u'name': u'recreation'}, {u'app_id': None, u'id': u'ai_Zmhsv0Ch', u'value': 0.95314974, u'name': u'outdoors'}, {u'app_id': None, u'id': u'ai_JfH5nDwN', u'value': 0.9493039, u'name': u'footpath'}, {u'app_id': None, u'id': u'ai_PBTpj0kl', u'value': 0.94928265, u'name': u'park'}, {u'app_id': None, u'id': u'ai_TdCBSxxT', u'value': 0.9362782, u'name': u'sport'}, {u'app_id': None, u'id': u'ai_V1FjkFXr', u'value': 0.93481445, u'name': u'leisure'}, {u'app_id': None, u'id': u'ai_l8TKp2h5', u'value': 0.9266087, u'name': u'people'}, {u'app_id': None, u'id': u'ai_FwtMR9mk', u'value': 0.9244586, u'name': u'motion'}, {u'app_id': None, u'id': u'ai_VPmHr5bm', u'value': 0.9119082, u'name': u'adult'}, {u'app_id': None, u'id': u'ai_lrTHSPdB', u'value': 0.90911067, u'name': u'action'}, {u'app_id': None, u'id': u'ai_FkctLMVh', u'value': 0.90870714, u'name': u'exercise'}, {u'app_id': None, u'id': u'ai_tBcWlsCp', u'value': 0.90854573, u'name': u'nature'}, {u'app_id': None, u'id': u'ai_hKbvQtBD', u'value': 0.9063741, u'name': u'vitality'}]}, u'id': u'a430a55f4f7045f4b7d6d0ec184e77ab'}]}
d = json.loads(json.dumps(str))
#print type(d)

iters = len(d["outputs"][0]["data"]["concepts"])
ref = d["outputs"][0]["data"]["concepts"]
print ref

for i in range(iters):
    print ref[i]["name"]



#loops = len(["outputs"][0]["data"]["concepts"])

#print str(loops)

