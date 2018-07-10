from clarifai.rest import ClarifaiApp
import json
app = ClarifaiApp("WbLe7smmpqg_v8rChg86PpuLhozg_GWofrs-0vBm", "xwbkbSHw6vq-tEDtGBzZ8qZIxJH4KqZauWVcf6dH")
# get the general model
model = app.models.get("general-v1.3")
# predict with the model

def getObjects(image):
    if image is None:
        image = "https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcRTDkTI5R040B327idli7L_o-MtGv0lCwDxZyZwJKSddOPHyXO6"
    result = model.predict_by_url(url=image)
    d = json.loads(json.dumps(str))
    iters = len(d["outputs"][0]["data"]["concepts"])
    ref = d["outputs"][0]["data"]["concepts"]
    returnRes = []

    for i in range(iters):
        returnRes.append(ref[i]["name"])
        print ref[i]["name"]
    print returnRes;