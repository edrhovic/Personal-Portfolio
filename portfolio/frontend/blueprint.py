from flask import Blueprint, render_template, redirect, url_for, session, request, make_response, flash
import mysql.connector
import re
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

blueprint = Blueprint('blueprint', __name__, template_folder='templates')

db_config = {
    'host':'localhost',
    'user':'root',
    'password':'',
    'database':'portfoliodb'
}

def make_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, proxy-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

def connect_db():
    return mysql.connector.connect(**db_config)


@blueprint.route('/')
@blueprint.route('/home')
def dashboard():
    if 'loggedIn' in session:
        first_name = session.get('firstname')
        response = make_response(render_template('dashboard.html', first_name=first_name))
        return make_header(response)

    return redirect(url_for('auth.login'))

@blueprint.route('/blog')
def blog():
    if 'loggedIn' in session:
        return render_template('blog.html')
    return redirect(url_for('auth.login'))

@blueprint.route('/profile', methods=['POST', 'GET'])
def profile():

    if 'loggedIn' in session:
        username = session['loggedIn']

        if request.method == 'POST':
            firstname = request.form.get('firstname')
            middlename = request.form.get('middlename')
            lastname = request.form.get('lastname')
            birthday = request.form.get('birthday')
            age = request.form.get('age')
            contact = request.form.get('contact')
            email = request.form.get('email')

            errors = []

            #Validation for First Name, Middle Name, and Last Name
            name_regex = r'^[A-Za-z ]{2,}$'
            if not re.match(name_regex, firstname) or not firstname.strip():
                errors.append("First name must contain only letters and spaces, and be at least 2 characters long.")
            if not re.match(name_regex, middlename) or not middlename.strip():
                errors.append("Middle name must contain only letters and spaces, and be at least 2 characters long.")
            if not re.match(name_regex, lastname) or not lastname.strip():
                errors.append("Last name must contain only letters and spaces, and be at least 2 characters long.")

            #Validation for contact number
            if not re.match(r'^\d{11}$', contact):
                errors.append("Contact number must be exactly 11 digits, with no symbols or spaces.")

            #Validation for email
            email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_regex, email):
                errors.append("Invalid email address. Please use a valid email (e.g., example@example.com).")
    

            #Validation for birthday
            birthday_regex = r'^\d{4}-\d{2}-\d{2}$'
            if not re.match(birthday_regex, birthday):
                errors.append("Invalid birthday format. Please enter a valid date (e.g., YYYY-MM-DD).")
            else:
                birthday_obj = datetime.strptime(birthday, '%Y-%m-%d')
                current_age = datetime.now().year - birthday_obj.year
                if datetime.now().month < birthday_obj.month or (datetime.now().month == birthday_obj.month and datetime.now().day < birthday_obj.day):
                    current_age -= 1
                if int(age) != current_age:
                    errors.append("Age must be accurate based on the given birthday.")
            if errors:
                for error in errors:
                    flash(error, category='error')
                return redirect(url_for('blueprint.profile'))
            
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("UPDATE my_tb SET firstname=%s, middlename=%s, lastname=%s, birthday=%s, age=%s, contact=%s, email=%s WHERE username=%s", (firstname, middlename, lastname, birthday, age, contact, email, username))
            conn.commit()
            cursor.close()
            conn.close()
            flash('Profile updated successfully!', category='success')
            return redirect(url_for('blueprint.profile'))
        
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM my_tb WHERE username=%s", (username,))
        usr = cursor.fetchone()
        
        if usr:
            return render_template('profile.html', usr=usr)
    
    return redirect(url_for('auth.login'))

@blueprint.route('/delete_profile', methods=['POST', 'GET'])
def delete_profile():

    if 'loggedIn' in session:
        username = session['loggedIn']
        password = request.form.get('password')

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM my_tb WHERE username=%s", (username,))
        usr = cursor.fetchone()

        if usr and check_password_hash(usr[9], password):
            conn.commit()
            session.clear()
            flash('Your profile has been deleted successfully!', 'success')
            return redirect(url_for('auth.login'))
        
        else:
            flash('Incorrect password. Please try again.', 'danger')
            return redirect(url_for('blueprint.profile'))
        
    return redirect(url_for('auth.login'))

