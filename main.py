from fastapi import FastAPI,Path,HTTPException,Query
import json
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal
app =FastAPI()

class Patient(BaseModel):
       id: Annotated[str, Field(..., description='ID of the patient', examples=['P001'])]
       name: Annotated[str, Field(..., description='Name of the patient')]
       city: Annotated[str, Field(..., description='City where the patient is living')]
       age: Annotated[int, Field(..., gt=0, lt=120, description='Age of the patient')]
       gender: Annotated[Literal['male', 'female', 'others'], Field(..., description='Gender of the patient')]
       height: Annotated[float, Field(..., gt=0, description='Height of the patient in mtrs')]
       weight: Annotated[float, Field(..., gt=0, description='Weight of the patient in kgs')]

       @computed_field
       @property
       def bmi(self)->float:
           bmi =  round( self.weight/(self.height**2),2)
           return bmi
       

       @computed_field
       @property
       def verdict(self)-> float:
           
        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi < 25:
            return 'Normal'
        elif self.bmi < 30:
            return 'Normal'
        else:
            return 'Obese'
           
def load_data():
    with open("patients.json",'r') as f:
        data =json.load(f)
    return data

def save_data(data):
    with open("patients.json",'w') as f:
        json.dump(data,f)

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


@app.post("/create")
def create_patient(patient:Patient):
    #load exisiting data
    data = load_data()
    #check if patinet alrdey exit
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient alreday exist")
    #new patint add in the db
    data[patient.id]=patient.model_dump(exclude=["id"])

    #save into python file
    save_data(data)
    return JSONResponse(status_code=201,content={'message':'Patient created Successfully'})
