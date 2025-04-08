import os
import logging
from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import Student
from database import db, init_db

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create the Flask application
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev_key_for_student_management")

# Initialize the database
init_db(app)

@app.route('/')
def index():
    """Render the home page."""
    return render_template('index.html')

@app.route('/students', methods=['GET'])
def view_students():
    """View all students in the database."""
    students = Student.get_all_students()
    return render_template('view_students.html', students=students)

@app.route('/students/add', methods=['GET', 'POST'])
def add_student():
    """Add a new student to the database."""
    if request.method == 'POST':
        roll_number = request.form['roll_number']
        name = request.form['name']
        course = request.form['course']
        
        try:
            gpa = float(request.form['gpa'])
            if gpa < 0 or gpa > 4.0:
                flash('GPA must be between 0 and 4.0', 'danger')
                return render_template('add_student.html')
        except ValueError:
            flash('GPA must be a number', 'danger')
            return render_template('add_student.html')
        
        # Check if roll number already exists
        if Student.get_student_by_roll(roll_number):
            flash('A student with this roll number already exists', 'danger')
            return render_template('add_student.html')
        
        # Create a new student
        student = Student(roll_number, name, course, gpa)
        success = student.save()
        
        if success:
            flash('Student added successfully!', 'success')
            return redirect(url_for('view_students'))
        else:
            flash('An error occurred while adding the student', 'danger')
    
    return render_template('add_student.html')

@app.route('/students/search', methods=['GET', 'POST'])
def search_student():
    """Search for a student by roll number."""
    if request.method == 'POST':
        roll_number = request.form['roll_number']
        student = Student.get_student_by_roll(roll_number)
        
        if student:
            return render_template('search_student.html', student=student, found=True)
        else:
            flash('No student found with that roll number', 'warning')
    
    return render_template('search_student.html', found=False)

@app.route('/students/edit/<roll_number>', methods=['GET', 'POST'])
def edit_student(roll_number):
    """Edit an existing student's information."""
    student = Student.get_student_by_roll(roll_number)
    
    if not student:
        flash('Student not found', 'danger')
        return redirect(url_for('view_students'))
    
    if request.method == 'POST':
        name = request.form['name']
        course = request.form['course']
        
        try:
            gpa = float(request.form['gpa'])
            if gpa < 0 or gpa > 4.0:
                flash('GPA must be between 0 and 4.0', 'danger')
                return render_template('edit_student.html', student=student)
        except ValueError:
            flash('GPA must be a number', 'danger')
            return render_template('edit_student.html', student=student)
        
        # Update student information
        student.name = name
        student.course = course
        student.gpa = gpa
        
        success = student.update()
        
        if success:
            flash('Student information updated successfully!', 'success')
            return redirect(url_for('view_students'))
        else:
            flash('An error occurred while updating the student information', 'danger')
    
    return render_template('edit_student.html', student=student)

@app.route('/students/delete/<roll_number>', methods=['POST'])
def delete_student(roll_number):
    """Delete a student record."""
    student = Student.get_student_by_roll(roll_number)
    
    if not student:
        flash('Student not found', 'danger')
    else:
        success = student.delete()
        
        if success:
            flash('Student deleted successfully!', 'success')
        else:
            flash('An error occurred while deleting the student', 'danger')
    
    return redirect(url_for('view_students'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
