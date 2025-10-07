from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

client = MongoClient("mongodb://localhost:27017/")
db = client["HealthCareSystem"]
user_table = db["Users"]
medication_table = db['Medications']
patient_table = db['Patient']
medical_information_table = db['Medical_Information']
lifestyle_table = db['Lifestyle']
dietary_information_table = db['Dietary_Information']

@app.route('/')
def home():
    session['admin'] = False
    return render_template('index.html')

@app.route('/login', methods=['POST','GET'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if username == 'admin' and password == 'admin1212':
        session['admin'] = True
        return redirect(url_for('admin'))
    user = user_table.find_one({"username": username, "password": password})
    if user:
        return redirect(url_for('dashboard', user_id=user['Patient_ID']))
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
    confirm_password = request.form.get('confirm_password')
    if password != confirm_password:
        return render_template("signup.html", signup_error="Passwords don't match")
    if user_table.find_one({"username": username}):
        return render_template("signup.html", signup_error="Username already exists")
    patient_id = f'P0{user_table.count_documents({}) + 5001}'
    user_table.insert_one({"Patient_ID": patient_id, "username": username, "email": email, "password": password})
    return redirect(url_for('dashboard', user_id=patient_id))

@app.route('/submit_health_data', methods=['POST'])
def submit_health_data():
    data = request.form.to_dict()
    int_data = ['Age', 'Height_cm', 'Weight_kg', 'Blood_Pressure_Systolic', 'Blood_Pressure_Diastolic', 'Cholesterol_Level', 'Blood_Sugar_Level', 'Daily_Steps', 'Exercise_Frequency', 'Sleep_Hours', 'Caloric_Intake', 'Protein_Intake', 'Carbohydrate_Intake', 'Fat_Intake']

    for key in int_data:
        data[key] = int(data[key])

    patient = ['Patient_ID', 'Age', 'Gender', 'Height_cm', 'Weight_kg']
    medical_information = ['Patient_ID', 'BMI', 'Chronic_Disease', 'Blood_Pressure_Systolic', 'Blood_Pressure_Diastolic', 'Cholesterol_Level', 'Blood_Sugar_Level', 'Genetic_Risk_Factor', 'Allergies']
    lifestyle = ['Patient_ID', 'Daily_Steps', 'Exercise_Frequency', 'Sleep_Hours', 'Alcohol_Consumption', 'Smoking_Habit', 'Dietary_Habits']
    dietary_information = ['Patient_ID', 'Caloric_Intake', 'Protein_Intake', 'Carbohydrate_Intake', 'Fat_Intake', 'Preferred_Cuisine', 'Food_Aversions']

    user_id = request.args['user_id']
    data['Patient_ID'] = user_id
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

    if patient_table.find_one({'Patient_ID': user_id}) is not None:
        patient_table.replace_one({'Patient_ID': user_id}, patient_document)
        medical_information_table.replace_one({'Patient_ID': user_id}, medical_information_document)
        lifestyle_table.replace_one({'Patient_ID': user_id}, lifestyle_document)
        dietary_information_table.replace_one({'Patient_ID': user_id}, dietary_information_document)
    else:
        patient_table.insert_one(patient_document)
        medical_information_table.insert_one(medical_information_document)
        lifestyle_table.insert_one(lifestyle_document)
        dietary_information_table.insert_one(dietary_information_document)

    return redirect(url_for('dashboard', user_id=user_id))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('signup.html')

@app.route('/medication', methods=['GET', 'POST'])
def medication():
    user_id = request.args['user_id']
    medications = list(medication_table.find({"Patient_ID": user_id}))
    user = user_table.find_one({'Patient_ID': user_id})
    return render_template('medication.html', user_id=user['Patient_ID'], medications=medications)

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    user_id = request.args['user_id']
    user = user_table.find_one({'Patient_ID': user_id})
    medications = list(medication_table.find({"Patient_ID": user_id}))
    medication_count = len(medications)
    reminders = []
    for medication in medications:
        year = int(medication['medStartDate'][0:4])
        month = int(medication['medStartDate'][5:7])
        date = int(medication['medStartDate'][8:])
        medDate = datetime(year, month, date)

        if datetime.now() > medDate:
            reminders.append(medication)
    reminder_count = len(reminders)

    return render_template('dashboard.html', user_id=user['Patient_ID'], reminders=reminders, medication_count=medication_count, username=user['username'], reminder_count=reminder_count)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    user_id = request.args['user_id']
    user = user_table.find_one({'Patient_ID': user_id})

    patient = patient_table.find_one({'Patient_ID': user_id})
    medical_information = medical_information_table.find_one({'Patient_ID': user_id})
    lifestyle = lifestyle_table.find_one({'Patient_ID': user_id})
    dietary_information = dietary_information_table.find_one({'Patient_ID': user_id})

    if patient is None:
        return render_template('user_detail.html', data=user)

    data = {}
    data.update(user)
    data.update(patient)
    data.update(medical_information)
    data.update(lifestyle)
    data.update(dietary_information)
    return render_template('profile.html', data=data)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    user_count = len(list(user_table.find({})))
    medication_count = len(list(medication_table.find({})))

    users = []

    for user in list(user_table.find({})):
        user_id = user['Patient_ID']
        patient = patient_table.find_one({'Patient_ID': user_id})
        medical_information = medical_information_table.find_one({'Patient_ID': user_id})
        lifestyle = lifestyle_table.find_one({'Patient_ID': user_id})
        dietary_information = dietary_information_table.find_one({'Patient_ID': user_id})
        data = {}
        data.update(user)

        if patient is None:
            users.append(data)
            continue

        data.update(patient)
        data.update(medical_information)
        data.update(lifestyle)
        data.update(dietary_information)
        users.append(data)

    print(users)
    return render_template('admin.html', user_count=user_count, medication_count=medication_count, users=users)

@app.route('/diet_plan', methods=['GET', 'POST'])
def diet_plan():
    user_id = request.args['user_id']
    user = user_table.find_one({'Patient_ID': user_id})
    return render_template('diet_plan.html', user_id=user['Patient_ID'])

@app.route('/add_medication', methods=['GET', 'POST'])
def add_medication():
    user_id = request.args['user_id']
    user = user_table.find_one({'Patient_ID': user_id})
    return render_template('add_medication.html', user_id=user['Patient_ID'])

@app.route('/user_detail', methods=['GET', 'POST'])
def user_detail():
    user_id = request.args['user_id']
    user = user_table.find_one({'Patient_ID': user_id})

    patient = patient_table.find_one({'Patient_ID': user_id})
    medical_information = medical_information_table.find_one({'Patient_ID': user_id})
    lifestyle = lifestyle_table.find_one({'Patient_ID': user_id})
    dietary_information = dietary_information_table.find_one({'Patient_ID': user_id})

    if patient is None:
        return render_template('user_detail.html', data=user)

    data = {}
    data.update(user)
    data.update(patient)
    data.update(medical_information)
    data.update(lifestyle)
    data.update(dietary_information)
    return render_template('user_detail.html', data=data)

@app.route('/register_medication', methods=['POST'])
def register_medication():
    user_id = request.args['user_id']
    medName = request.form.get('medName')
    medDosage = request.form.get('medDosage')
    medFrequence = request.form.get('medFrequency')
    medTime = request.form.get('medTime')
    medStartDate = request.form.get('medStartDate')
    medDuration = request.form.get('medDuration')
    medNotes = request.form.get('medNotes')

    document = {'Patient_ID': user_id,
                'medName': medName,
                'medDosage': medDosage,
                'medFrequence': medFrequence,
                'medTime': medTime,
                'medStartDate': medStartDate,
                'medDuration': medDuration,
                'medNotes': medNotes
                }
    
    db['Medications'].insert_one(document)

    return redirect(url_for('medication', user_id=user_id))

@app.route('/delete_user', methods=['GET', 'POST'])
def delete_user():
    user_id = request.args['user_id']
    user_table.delete_one({'Patient_ID': user_id})
    patient_table.delete_one({'Patient_ID': user_id})
    medical_information_table.delete_one({'Patient_ID': user_id})
    lifestyle_table.delete_one({'Patient_ID': user_id})
    dietary_information_table.delete_one({'Patient_ID': user_id})
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)
