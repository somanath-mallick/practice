from flask import Flask, request, jsonify,render_template
import psycopg2

app = Flask(__name__)

# Database connection details
DB_HOST = "localhost"
DB_NAME = "somanath"
DB_USER = "postgres"
DB_PASS = "postgres"

def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    return conn


@app.route('/',methods=['POST','GET'])
def first():
    return render_template('html.html')


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
    user = cur.fetchone()

    cur.close()
    conn.close()

    if user:
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401
    
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    gender = data.get('gender')
    phone_number = data.get('phone_number')
    
    if not (name and email and password and gender and phone_number):
        return jsonify({"error": "All fields are required"}), 400

    # Connect to the database
   
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Check if the email already exists
    cur.execute('SELECT * FROM public.users WHERE email = %s', (email,))
    existing_user = cur.fetchone()
    
    if existing_user:
        return jsonify({"error": "Email already registered"}), 409
    
    # Insert the new user into the database
    cur.execute('''
        INSERT INTO public.users (name, email, password, gender, phone_number)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id;
    ''', (name, email, password, gender, phone_number))
    
    conn.commit()
    cur.close()
    conn.close()
    
    return jsonify({"message": "User registered successfully"}), 201



if __name__ == '__main__':
    app.run(debug=True)
