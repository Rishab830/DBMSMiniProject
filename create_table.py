import pymongo
import pandas as pd

data = pd.read_csv("Personalized_Diet_Recommendations.csv")

data_dict = data.to_dict()

patient = ['Patient_ID', 'Age', 'Gender', 'Height_cm', 'Weight_kg']
medical_information = ['Patient_ID', 'BMI', 'Chronic_Disease', 'Blood_Pressure_Systolic', 'Blood_Pressure_Diastolic', 'Cholesterol_Level', 'Blood_Sugar_Level', 'Genetic_Risk_Factor', 'Allergies']
lifestyle = ['Patient_ID', 'Daily_Steps', 'Exercise_Frequency', 'Sleep_Hours', 'Alcohol_Consumption', 'Smoking_Habit', 'Dietary_Habits']
dietary_information = ['Patient_ID', 'Caloric_Intake', 'Protein_Intake', 'Carbohydrate_Intake', 'Fat_Intake', 'Preferred_Cuisine', 'Food_Aversions']
recommendations = ['Patient_ID', 'Recommended_Calories', 'Recommended_Protein', 'Recommended_Carbs', 'Recommended_Fats', 'Recommended_Meal_Plan']

patient_data = []
medical_information_data = []
lifestyle_data = []
dietary_information_data = []
recommendations_data = []

for i in range(len(data_dict['Patient_ID'])):
    patient_document = {}
    medical_information_document = {}
    lifestyle_document = {}
    dietary_information_document = {}
    recommendations_document = {}
    
    for key in patient:
        patient_document[key] = data_dict[key][i]
    patient_data.append(patient_document)
    
    for key in medical_information:
        medical_information_document[key] = data_dict[key][i]
    medical_information_data.append(medical_information_document)
    
    for key in lifestyle:
        lifestyle_document[key] = data_dict[key][i]
    lifestyle_data.append(lifestyle_document)
    
    for key in dietary_information:
        dietary_information_document[key] = data_dict[key][i]
    dietary_information_data.append(dietary_information_document)
    
    for key in recommendations:
        recommendations_document[key] = data_dict[key][i]
    recommendations_data.append(recommendations_document)

client = pymongo.MongoClient("mongodb://localhost:27017/")

db = client["HealthCareSystem"]

patient_collection = db["Patient"]
medical_information_collection = db["Medical_Information"]
lifestyle_collection = db["Lifestyle"]
dietary_information_collection = db["Dietary_Information"]
recommendations_collection = db["Recommendations"]

patient_collection.create_index('Patient_ID', unique=True)
medical_information_collection.create_index('Patient_ID', unique=True)
lifestyle_collection.create_index('Patient_ID', unique=True)
dietary_information_collection.create_index('Patient_ID', unique=True)
recommendations_collection.create_index('Patient_ID', unique=True)

patient_collection.insert_many(patient_data)
medical_information_collection.insert_many(medical_information_data)
lifestyle_collection.insert_many(lifestyle_data)
dietary_information_collection.insert_many(dietary_information_data)
recommendations_collection.insert_many(recommendations_data)