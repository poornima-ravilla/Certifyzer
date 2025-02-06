from flask import Flask,jsonify, render_template, request, redirect, url_for, Response,session
import sqlite3
import pandas as pd
import os
from werkzeug.utils import secure_filename
from email.mime.text import MIMEText 
from email.mime.multipart import MIMEMultipart
import smtplib

app = Flask(__name__)

# Login Page 

# secret Key for invalid password message
app.secret_key='Invalid_PasssecretKey'

# Function to get username password data 
def get_mentor_from_db():
    conn = sqlite3.connect('Events.db')
    query = 'SELECT * FROM mentor'
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_club_from_db():
    conn = sqlite3.connect('Events.db')
    query = 'SELECT * FROM club'
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Function to fetch user details based on the email provided
def get_user_by_email(email):
    conn = sqlite3.connect('Events.db')  # Connect to your database
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM club WHERE username=?", (email,))
    result = cursor.fetchone()
    conn.close()
    return result
def get_usermentor_by_email(email):
    conn = sqlite3.connect('Events.db')  # Connect to your database
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM mentor WHERE username=?", (email,))
    result = cursor.fetchone()
    conn.close()
    return result
def send_email(to_email, subject, body,value):
    # Set up SMTP connection
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.ehlo()
    smtp.starttls()

    # Login with your email and password (use an app-specific password if 2FA is enabled)
    smtp.login('my157mail@gmail.com', 'qmdo tzfn buey cpxf')

    # Build the message
    msg = MIMEMultipart()
    msg['From'] = 'my157mail@gmail.com'
    msg['To'] = to_email
    msg['Subject'] = subject
    body_value = f"{body} Your verification code is {value}."
    msg.attach(MIMEText(body_value, 'plain'))

    # Send the email
    smtp.sendmail('my157mail@gmail.com', to_email, msg.as_string())
    smtp.quit()


# Route to forgot password
@app.route('/forgot-password', methods=['POST'])
def forgot_password():
    try:
        
        # data = request.get_json()  
        # print(f"Received data: {data}")
        # print(request.form)
        email = request.form.get('email')
        print(email)
        if not email:
            return jsonify({"success": False, "message": "Email value not sent"}), 400
    # Query the database for the password based on email
        user = get_user_by_email(email)
        
        
        if not user:
            user = get_usermentor_by_email(email)

    
        if user:
        # Send an email to the user
            send_email(email, 'Hi there!', 'Hello, this is an automatic message from our system!\nPassword for your Account :',user[0])
        
        # Return success response
            return jsonify({'success': True, 'message': 'Email sent successfully.'})
        else:
        # Return error if email not found
            return jsonify({'success': False, 'message': 'Email not found.'})
    except Exception as e:
        # Log the error
        print(f"Error in forgot_password route: {e}")
        return jsonify({'success': False, 'message': 'Something went wrong, please try again later.'}), 500
# Route to display login form
@app.route('/', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        username = request.form.get('email')

        password = request.form['password']
        # Fetch users from both mentor and club databases
        users_mentor = get_mentor_from_db()
        

        # Check if the user is a mentor
        usermentor = users_mentor[
            (users_mentor['username'] == username) & 
            (users_mentor['password'] == password)
        ]
        users_club = get_club_from_db()
        userclub = users_club[
            (users_club['username'] == username) & 
            (users_club['password'] == password)
        ]
        


        username = username.split('@')[0]

        # if mentor isnt empty
        if not usermentor.empty:
            # return redirect(url_for('mentor_welcome', username=username))
            return redirect(url_for('mentor_welcome'))

        # Check if the user is a club
        
        
        # if club isnt empty
        if not userclub.empty:
            return redirect(url_for('club_welcome', username=username))

        session['error'] = 'Invalid Username Or Password '
        return redirect('/')
    error = session.pop('error', None)  
    return render_template('loginevent.html', error=error)

# Route to welcome mentor after successful login
@app.route('/mentor_welcome')
def mentor_welcome():
    # return render_template('mentor_welcome.html', username=username)
    return render_template('index.html')


# Route to welcome club after successful login
@app.route('/club_welcome/<username>')
def club_welcome(username):
    conn = get_db_conn()
    cursor = conn.cursor()
    # create 2 table for username entered 
    Club_events = f"{username}_events"
    Club_det = f"{username}_club_det"
    email= f"{username}@gmail.com"
    
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {Club_events} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                evename TEXT,   
                date TEXT,
                points INTEGER,
                desc TEXT,  
                filepath TEXT
        )
    ''')

    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {Club_det} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                faculty TEXT,
                president TEXT,
                email TEXT,
                contact NUMBER,
                profile BLOB
        )
    ''')
    # query = f'''
    #     INSERT INTO {Club_det} (id, faculty, president, email, contact, profile) VALUES (?, ?, ?, ?, ?, ?)
    # '''
    
    # # Insert data into the table
    # cursor.execute(query, (1, 'faculty_name', 'President_name', 'email_ID', '0000000000', None))

    # Commit the transaction to save the changes
    conn.commit()

    # Close the connection to the database
    
    
    
    cursor.execute(f'SELECT * FROM {Club_events}')
    events = cursor.fetchall()

    cursor.execute(f'SELECT * FROM {Club_det}')
    club_det = cursor.fetchone()

    conn.close()

    return render_template('Club_home.html', username=username, events=events, club_det=club_det)



# Club Home Page

# folder to store excel files
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'xls', 'xlsx','jpg','png','jpeg','avif'}


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# SQLite connection
def get_db_conn():
    conn = sqlite3.connect('Events.db')
    conn.row_factory = sqlite3.Row
    return conn

# Check if file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS 

# # ClubHome page
# @app.route('/home')
# def home():
#     conn = get_db_conn()
#     events = conn.execute('SELECT * FROM events').fetchall()
#     club_det = conn.execute('SELECT * FROM club_det ').fetchone()
#     conn.close()
#     return render_template('Club_home.html', events=events,club_det=club_det)

# Add events form
@app.route('/addEvent', methods=['POST'])
def addEvent():
    username = request.form['username']

    Club_events = f"{username}_events"

    evename = request.form.get('evenamee')
    date = request.form.get('date')
    points = request.form.get('points')
    desc = request.form.get('desc')
    list_file = request.files['list']
    
    # Check if the uploaded file is an Excel file
       
    if list_file and allowed_file(list_file.filename):
        filename = secure_filename(list_file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        # Save the file to the upload folder
        list_file.save(filepath)

        try:
            # Insert event details along with the file path into the database
            conn = get_db_conn()
            query = f'''
            INSERT INTO {Club_events} (evename, date, points, desc, filepath)
                VALUES (?, ?, ?, ?, ?)
                '''

            conn.execute(query, (evename, date, points, desc, filepath))
            # conn.execute('''
            #     INSERT INTO {Club_events} (evename, date, points, desc, filepath)
            #     VALUES (?, ?, ?, ?, ?)
            # ''', (evename, date, points, desc, filepath))

            conn.commit()
            conn.close()

            return redirect(url_for('club_welcome', username=username))

        

        except Exception as e:
            return f"Error saving event: {e}", 400

    else:
        return "Invalid file format or no file uploaded!", 400
    
@app.route('/update_event', methods=['POST'])
def update_event():
    username = request.form['username']
    Club_events = f"{username}_events"
    

    event_id = request.form['eventId']
    evename = request.form['evetname']
    evedate = request.form['evedate']
    evepoints = request.form['evepoints']
    evedesc = request.form['evedesc']
    
    evefile = request.files['evetfile']
    filepath = None
    if evefile and evefile.filename:
        filename = secure_filename(evefile.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        evefile.save(filepath)

    try:
        conn = get_db_conn()

        if filepath:
            query = f'''
            UPDATE {Club_events}
            SET evename = ?, date = ?, points = ?, desc = ?, filepath = ?
            WHERE id = ?
            '''
            conn.execute(query, (evename, evedate, evepoints, evedesc, filepath, event_id))
        else:
            query = f'''
            UPDATE {Club_events}
            SET evename = ?, date = ?, points = ?, desc = ?
            WHERE id = ?
            '''
            conn.execute(query, (evename, evedate, evepoints, evedesc, event_id))
        # if filepath:
        #     conn.execute('''
        #         UPDATE {Club_events}
        #         SET evename = ?,date = ?, points = ?, desc = ?, filepath = ?
        #         WHERE id=?
        #     ''', (evename,evedate, evepoints, evedesc, filepath, event_id))
        # else:
        #     conn.execute('''
        #         UPDATE {Club_events}
        #         SET evename = ?, date = ?, points = ?, desc = ?
        #         WHERE id = ?
        #     ''', (evename, evedate, evepoints, evedesc, event_id))

        conn.commit()
        conn.close()
        return redirect(url_for('club_welcome',username=username))
    except Exception as e:
        return f"Error updating event: {e}", 400

# edit club data
@app.route('/editclub', methods=['POST'])
def editclub():
    username=request.form['username']
    print(username)
    Club_det = f"{username}_club_det"
    print(Club_det)

    faculty=request.form['faculty']
    president=request.form['president']
    email=request.form['email']
    contact=request.form['contact']

    conn = get_db_conn()
    
    try:
        query = f'''
        UPDATE {Club_det}
        SET faculty = ?, president = ?, email = ?, contact = ?
    '''

        conn.execute(query, (faculty, president, email, contact))
        # conn.execute('''
        #     UPDATE {Club_det}
        #     SET faculty = ?, president = ?, email = ?, contact = ?
        # ''', (faculty, president, email, contact))
        conn.commit()
        conn.close()
        return redirect(url_for('club_welcome',username=username))  # Redirect to the home page after successful edit
    except Exception as e:
        conn.close()
        return f"Error updating club details: {e}", 400

# logo 
@app.route('/upload_image', methods=['POST'])
def upload_image():
    username = request.form.get('username')
    Club_det = f"{username}_club_det"

    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    if file and allowed_file(file.filename):
        # Save the file
        file_data = file.read()

        # Save the file path to the database
        conn = get_db_conn()
        query=f'''
            UPDATE {Club_det} SET profile = ? WHERE id = 1

            '''
        conn.execute(query,(file_data,))
        # conn.execute('UPDATE {Club_det} SET profile = ? WHERE id = 1', (file_data,)) 
        conn.commit()
        conn.close()

        return redirect(url_for('club_welcome',username=username))
    return "Invalid file type", 400

@app.route('/profileImage')
def profile_image():
    username = request.args.get('username')
    Club_det = f"{username}_club_det"

    conn = get_db_conn()
    query=f'''
            SELECT profile FROM {Club_det} WHERE id = 1

            '''
    cursor=conn.execute(query)
    # conn = conn.execute('SELECT profile FROM {Club_det} WHERE id = 1')
    row = cursor.fetchone()
    conn.close()

    if row and row[0]:
        # Serve the image as a response
        return Response(row[0], mimetype='image/jpeg')  # Adjust `mimetype` as per your image type
    else:
         base_path = os.path.abspath(os.path.dirname(__file__))
         logo_path = os.path.join(base_path, 'static', 'css', 'logo.png')
         print(logo_path)
         with open(logo_path, 'rb') as f:
            return Response(f.read(), mimetype='image/png')

@app.route('/logout')
def logout():
    session.clear()  
    return redirect(url_for('login', message='You Are Currently logged out'))

@app.route('/search', methods=['POST'])
def search_student():
    event_name = request.form.get('eventname')
    stud_name = request.form.get('stud_name')

    if not event_name or not stud_name:
        return jsonify({"error": "Please provide both event name and student name"}), 400

    # Connect to the database
    conn = sqlite3.connect("Events.db")
    cursor = conn.cursor()

    try:
        # Step 1: Retrieve all tables ending with '_events'
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%_events';")
        tables = cursor.fetchall()

        if not tables:
            return jsonify({"error": "No tables found ending with '_events'."}), 404

        # Step 2: Search for the event in all tables
        for table in tables:
            table_name = table[0]
            event_column = 'evename'  # Use 'event' for Astronomy_events, 'evename' for others

            # Check if the event exists in the current table (using dynamic column name)
            cursor.execute(f"SELECT filepath, {event_column}, date, points, desc FROM {table_name} WHERE LOWER({event_column}) = LOWER(?)", (event_name,))
            result = cursor.fetchone()

            if result:
                filepath, eventname, date, points, desc = result

                # Step 3: Read the Excel file associated with the event
                try:
                    excel_data = pd.read_excel(filepath)

                    # Debugging: Print column names to console
                    print("Excel Columns:", excel_data.columns.tolist())

                    # Standardize column names by stripping spaces and converting to lowercase
                    excel_data.columns = [col.strip().lower() for col in excel_data.columns]
                    listu = ['Names', 'sss', 'names', 'Name', 'name', 'Student Name', 'student name', 'StudentName']
                    student_column = next((col for col in listu if col in excel_data.columns), None)

                    if not student_column:
                        return jsonify({"error": f"Invalid Excel format. '{student_column}' column not found."}), 400

                    # Step 4: Check if the student exists in the Excel file
                    student_exists = excel_data[excel_data[student_column].str.lower() == stud_name.lower()]
                    if not student_exists.empty:
                        # Return success response with event and student details
                        return jsonify({
                            "message": f"Name: {stud_name}\n\nEvent: {eventname}\n\nDate: {date}\n\nPoints: {points}\n\ndesc: {desc}",
                        }), 200
                except Exception as e:
                    return jsonify({"error": f"Error reading the Excel file at {filepath}: {str(e)}"}), 500

        # If event is not found in any table
        return jsonify({"message": f"Student {stud_name} has NOT participated in Event {event_name}."}), 404

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

    finally:
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)
