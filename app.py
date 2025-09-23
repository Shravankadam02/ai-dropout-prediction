from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
import pandas as pd
import json
import os
from datetime import datetime
from werkzeug.utils import secure_filename
from utils.risk_calculator import RiskCalculator

app = Flask(__name__)
app.secret_key = 'sih_demo_key_2024'  # Demo only - use secure key in production
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize risk calculator
risk_calc = RiskCalculator()

# Global variable to store student data (in production, use proper database)
students_data = None

def load_sample_data():
    """Load sample student data from CSV"""
    global students_data
    try:
        students_data = pd.read_csv('data/students_sample.csv')
        return True
    except FileNotFoundError:
        return False

def load_student_notes():
    """Load student intervention notes from JSON file"""
    notes_file = 'data/student_notes.json'
    if os.path.exists(notes_file):
        with open(notes_file, 'r') as f:
            return json.load(f)
    return {}

def save_student_notes(notes):
    """Save student intervention notes to JSON file"""
    notes_file = 'data/student_notes.json'
    os.makedirs('data', exist_ok=True)
    with open(notes_file, 'w') as f:
        json.dump(notes, f, indent=2)

@app.route('/')
def index():
    """Redirect to login page"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page with hardcoded credentials for demo"""
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        
        # Hardcoded credentials for demo
        if username == 'mentor' and password == 'admin':
            session['user_id'] = 'mentor'
            session['user_role'] = 'mentor'
            if request.is_json:
                return jsonify({'status': 'success', 'redirect': '/dashboard'})
            return redirect(url_for('dashboard'))
        else:
            error_msg = 'Invalid credentials. Use mentor/admin'
            if request.is_json:
                return jsonify({'status': 'error', 'message': error_msg})
            flash(error_msg, 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout and clear session"""
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    """Main mentor dashboard"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Load sample data if not already loaded
    if students_data is None:
        if not load_sample_data():
            flash('Sample data not found. Please upload a CSV file.', 'warning')
    
    return render_template('dashboard.html')

@app.route('/admin')
def admin():
    """Admin dashboard with summary statistics"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    return render_template('admin.html')

@app.route('/api/upload-csv', methods=['POST'])
def upload_csv():
    """Upload and process CSV file"""
    global students_data
    
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and file.filename.lower().endswith('.csv'):
        try:
            # Read CSV directly from memory
            students_data = pd.read_csv(file)
            
            # Validate required columns
            required_cols = ['student_id', 'first_name', 'last_name', 'attendance_percent', 
                           'fees_due_days', 'attempts_in_subject_X', 'last_3_tests_avg', 'previous_3_tests_avg']
            missing_cols = [col for col in required_cols if col not in students_data.columns]
            
            if missing_cols:
                return jsonify({'error': f'Missing columns: {", ".join(missing_cols)}'}), 400
            
            return jsonify({
                'message': 'CSV uploaded successfully',
                'student_count': len(students_data),
                'columns': list(students_data.columns)
            })
            
        except Exception as e:
            return jsonify({'error': f'Error processing CSV: {str(e)}'}), 400
    
    return jsonify({'error': 'Invalid file format. Please upload a CSV file.'}), 400

@app.route('/api/load-sample')
def load_sample():
    """Load sample data endpoint"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    if load_sample_data():
        return jsonify({
            'message': 'Sample data loaded successfully',
            'student_count': len(students_data)
        })
    else:
        return jsonify({'error': 'Sample data file not found'}), 404

@app.route('/api/students')
def get_students():
    """Get all students with computed risk scores"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    global students_data
    if students_data is None:
        return jsonify({'error': 'No student data loaded'}), 400
    
    try:
        # Calculate risk for all students
        students_with_risk = []
        for _, row in students_data.iterrows():
            risk_result = risk_calc.calculate_risk(row.to_dict())
            student_info = {
                'student_id': row['student_id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'class': row.get('class', 'N/A'),
                'roll_no': row.get('roll_no', 'N/A'),
                'attendance_percent': row['attendance_percent'],
                'fees_due_days': row['fees_due_days'],
                'last_3_tests_avg': row['last_3_tests_avg'],
                'risk_score': round(risk_result['risk_score'], 3),
                'risk_level': risk_result['risk_level'],
                'risk_color': risk_result['risk_color']
            }
            students_with_risk.append(student_info)
        
        # Sort by risk score (highest first)
        students_with_risk.sort(key=lambda x: x['risk_score'], reverse=True)
        
        return jsonify({
            'students': students_with_risk,
            'total_count': len(students_with_risk)
        })
        
    except Exception as e:
        return jsonify({'error': f'Error calculating risks: {str(e)}'}), 500

@app.route('/api/student/<student_id>')
def get_student_detail(student_id):
    """Get detailed student information with risk analysis"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    global students_data
    if students_data is None:
        return jsonify({'error': 'No student data loaded'}), 400
    
    try:
        # Find student
        student_row = students_data[students_data['student_id'] == student_id]
        if student_row.empty:
            return jsonify({'error': 'Student not found'}), 404
        
        student = student_row.iloc[0].to_dict()
        
        # Calculate detailed risk analysis
        risk_result = risk_calc.calculate_detailed_risk(student)
        
        # Load intervention notes
        notes = load_student_notes()
        student_notes = notes.get(student_id, [])
        
        # Prepare response
        response = {
            'student_id': student['student_id'],
            'first_name': student['first_name'],
            'last_name': student['last_name'],
            'class': student.get('class', 'N/A'),
            'roll_no': student.get('roll_no', 'N/A'),
            'attendance_percent': student['attendance_percent'],
            'fees_due_days': student['fees_due_days'],
            'attempts_in_subject_X': student['attempts_in_subject_X'],
            'last_test_1': student.get('last_test_1', 0),
            'last_test_2': student.get('last_test_2', 0),
            'last_test_3': student.get('last_test_3', 0),
            'last_3_tests_avg': student['last_3_tests_avg'],
            'previous_3_tests_avg': student['previous_3_tests_avg'],
            'risk_analysis': risk_result,
            'intervention_notes': student_notes
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': f'Error fetching student details: {str(e)}'}), 500

@app.route('/api/student/<student_id>/note', methods=['POST'])
def add_student_note(student_id):
    """Add intervention note for a student"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    note_text = data.get('note', '').strip()
    
    if not note_text:
        return jsonify({'error': 'Note text is required'}), 400
    
    try:
        # Load existing notes
        notes = load_student_notes()
        
        # Add new note
        if student_id not in notes:
            notes[student_id] = []
        
        new_note = {
            'timestamp': datetime.now().isoformat(),
            'mentor_id': session['user_id'],
            'note': note_text
        }
        
        notes[student_id].append(new_note)
        
        # Save notes
        save_student_notes(notes)
        
        return jsonify({
            'message': 'Note added successfully',
            'note': new_note
        })
        
    except Exception as e:
        return jsonify({'error': f'Error saving note: {str(e)}'}), 500

@app.route('/api/summary')
def get_summary():
    """Get summary statistics for admin dashboard"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    global students_data
    if students_data is None:
        return jsonify({'error': 'No student data loaded'}), 400
    
    try:
        # Calculate risk for all students
        risk_counts = {'Low': 0, 'Medium': 0, 'High': 0}
        attendance_stats = []
        score_trends = []
        
        for _, row in students_data.iterrows():
            risk_result = risk_calc.calculate_risk(row.to_dict())
            risk_counts[risk_result['risk_level']] += 1
            
            attendance_stats.append({
                'student_id': row['student_id'],
                'attendance': row['attendance_percent']
            })
            
            score_trends.append({
                'student_id': row['student_id'],
                'previous_avg': row['previous_3_tests_avg'],
                'current_avg': row['last_3_tests_avg']
            })
        
        return jsonify({
            'total_students': len(students_data),
            'risk_distribution': risk_counts,
            'attendance_stats': attendance_stats,
            'score_trends': score_trends,
            'high_risk_percentage': round((risk_counts['High'] / len(students_data)) * 100, 1)
        })
        
    except Exception as e:
        return jsonify({'error': f'Error generating summary: {str(e)}'}), 500

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('data', exist_ok=True)
    os.makedirs('static/uploads', exist_ok=True)
    os.makedirs('utils', exist_ok=True)
    
    # Load sample data on startup
    load_sample_data()
    
    # Run Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)