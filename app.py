from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
db = client["HealthCareSystem"]
user_table = db["Users"]

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST','GET'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = user_table.find_one({"username": username, "password": password})
    if user:
        return render_template('dashboard.html', username=username)
    else:
        return render_template('login.html', login_error='incorrect credentials')
    
@app.route('/login_first', methods=['POST','GET'])
def login_first():
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    if user_table.find_one({"username": username}):
        return render_template("signup.html", signin_error="Username already exists")
    patient_id = f'{db.Patient.count_documents({}) + 1}'
    user_table.insert_one({"Patient_ID": patient_id, "username": username, "email": email, "password": password})
    return render_template('login.html')

@app.route('/profile', methods=['POST', 'GET'])
def profile():
    return render_template('profile.html')

@app.route('/submit_health_data', methods=['POST'])
def submit_health_data():
    data = request.form.to_dict()
    
    int_data = ['Age', 'Height_cm', 'Weight_kg', 'Blood_Pressure_Systolic', 'Blood_Pressure_Diastolic', 'Cholesterol_Level', 'Blood_Sugar_Level', 'Daily_Steps', 'Exercise_Frequency', 'Sleep_Hours', 'Alcohol_Consumption', 'Caloric_Intake', 'Protein_Intake', 'Carbohydrate_Intake', 'Fat_Intake']

    for key in int_data:
        data[key] = int(data[key])

    patient = ['Patient_ID', 'Age', 'Gender', 'Height_cm', 'Weight_kg']
    medical_information = ['Patient_ID', 'BMI', 'Chronic_Disease', 'Blood_Pressure_Systolic', 'Blood_Pressure_Diastolic', 'Cholesterol_Level', 'Blood_Sugar_Level', 'Genetic_Risk_Factor', 'Allergies']
    lifestyle = ['Patient_ID', 'Daily_Steps', 'Exercise_Frequency', 'Sleep_Hours', 'Alcohol_Consumption', 'Smoking_Habit', 'Dietary_Habits']
    dietary_information = ['Patient_ID', 'Caloric_Intake', 'Protein_Intake', 'Carbohydrate_Intake', 'Fat_Intake', 'Preferred_Cuisine', 'Food_Aversions']

    data['Patient_ID'] = f'P0{db.Patient.count_documents({}) + 1}'
    data['BMI'] = data['Weight_kg']/pow(data['Height_cm'],2)

    patient_document = {}
    medical_information_document = {}
    lifestyle_document = {}
    dietary_information_document = {}

    for key in patient:
        patient_document[key] = data[key]
    
    for key in medical_information:
        medical_information_document[key] = data[key]
    
    for key in lifestyle:
        lifestyle_document[key] = data[key]
    
    for key in dietary_information:
        dietary_information_document[key] = data[key]

    db.Patient.insert_one(patient_document)
    db.Medical_Information.insert_one(medical_information_document)
    db.Lifestyle.insert_one(lifestyle_document)
    db.Dietary_Information.insert_one(dietary_information_document)

    return "<h2>Thank you, your health data has been recorded.</h2>"

@app.route('/signup')
def signup():
    return render_template('signup.html')


if __name__ == '__main__':
    app.run(debug=True)
