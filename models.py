from database import db

class Student:
    """Student model for managing student records."""
    
    def __init__(self, roll_number, name, course, gpa):
        """Initialize a new Student instance."""
        self.roll_number = roll_number
        self.name = name
        self.course = course
        self.gpa = gpa
    
    def save(self):
        """Save the student to the database."""
        try:
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO students (roll_number, name, course, gpa) VALUES (?, ?, ?, ?)",
                (self.roll_number, self.name, self.course, self.gpa)
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error saving student: {e}")
            return False
    
    def update(self):
        """Update the student's information in the database."""
        try:
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE students SET name = ?, course = ?, gpa = ? WHERE roll_number = ?",
                (self.name, self.course, self.gpa, self.roll_number)
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating student: {e}")
            return False
    
    def delete(self):
        """Delete the student from the database."""
        try:
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM students WHERE roll_number = ?",
                (self.roll_number,)
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting student: {e}")
            return False
    
    @staticmethod
    def get_all_students():
        """Get all students from the database."""
        try:
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT roll_number, name, course, gpa FROM students")
            rows = cursor.fetchall()
            conn.close()
            
            students = []
            for row in rows:
                student = Student(row[0], row[1], row[2], row[3])
                students.append(student)
            
            return students
        except Exception as e:
            print(f"Error getting all students: {e}")
            return []
    
    @staticmethod
    def get_student_by_roll(roll_number):
        """Get a student by roll number."""
        try:
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT roll_number, name, course, gpa FROM students WHERE roll_number = ?",
                (roll_number,)
            )
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return Student(row[0], row[1], row[2], row[3])
            return None
        except Exception as e:
            print(f"Error getting student by roll: {e}")
            return None
