from fastapi import FastAPI,Path,HTTPException,Query
import json
app =FastAPI()
def load_data():
    with open("patients.json",'r') as f:
        data =json.load(f)
    return data

@app.get("/")
def home_page():
    return {"message":"Home Page"}

@app.get("/about")
def about_abhinav():
    return({'message':"Fully funtional manage to patient record"})

@app.get("/view")
def get_data():
    data = load_data()
    return data

@app.get("/patient/{patient_id}")
def Patient_id(patient_id:str =Path(...,description="Id of the pateint",example="P001")):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=400,detail="Patient not found")

@app.get("/sort")
def sort_patient(sort_by : str = Query(...,description='Sort on the bassi of height , weight or bmi'),order_by : str = Query('asc',description='sort in ascing or descending order') ):
    valid_fileds = ['height', 'weight','bmi']

    if sort_by not in valid_fileds:
        raise HTTPException(status_code=400,detail='invlaid fiend selecte from {valid_fileds}')

    if order_by not in ['asc','desc']:
        raise HTTPException(status_code=400,detail="Invalid Oder selete")
    
    data = load_data()
# reverse -> True decsenting order sorting
    sort_order = True if order_by=='desc' else False
    sort_data = sorted(data.values(),key=lambda x : x.get(sort_by,0),reverse=sort_order)
    return sort_data

