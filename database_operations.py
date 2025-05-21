from typing import List, Optional
from datetime import datetime, date
from database_connection import DatabaseConnection

class DatabaseOperations:
    def __init__(self):
        self.db = DatabaseConnection()
        if self.db.connect():
            print("\nConnected to database successfully")
        else:
            print("Failed to connect to database")

    def execute_query(self, query, params=None):
        cursor = self.db.get_cursor()
        if cursor:
            try:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                self.db.connection.commit()
                return True
            except Exception as e:
                print(f"Error executing query: {str(e)}")
                return False
        return False

    def fetch_all(self, query, params=None):
        cursor = self.db.get_cursor()
        if cursor:
            try:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                return cursor.fetchall()
            except Exception as e:
                print(f"Error fetching data: {str(e)}")
                return []
        return []

    def fetch_one(self, query, params=None):
        cursor = self.db.get_cursor()
        if cursor:
            try:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                return cursor.fetchone()
            except Exception as e:
                print(f"Error fetching data: {str(e)}")
                return None
        return None

    def add_student(self, name, dob, gender, email, phone, address):
        query = """
            INSERT INTO Students (FullName, DOB, Gender, Email, Phone, Address) 
            VALUES (?, ?, ?, ?, ?, ?)
        """
        return self.execute_query(query, (name, dob, gender, email, phone, address))

    def get_all_students(self):
        print("Fetching all students...")
        query = "SELECT StudentID, FullName, DOB, Gender, Email, Phone, Address FROM Students ORDER BY StudentID"
        results = self.fetch_all(query)
        print(f"Found {len(results) if results else 0} students")
        return results

    def get_student(self, student_id):
        query = "SELECT StudentID, FullName, DOB, Gender, Email, Phone, Address FROM Students WHERE StudentID = ?"
        return self.fetch_one(query, (student_id,))

    def update_student(self, student_id, name, dob, gender, email, phone, address):
        query = """
            UPDATE Students 
            SET FullName = ?, DOB = ?, Gender = ?, Email = ?, Phone = ?, Address = ? 
            WHERE StudentID = ?
        """
        return self.execute_query(query, (name, dob, gender, email, phone, address, student_id))

    def delete_student(self, student_id):
        query = "DELETE FROM Students WHERE StudentID = ?"
        return self.execute_query(query, (student_id,))

    def add_teacher(self, name, department, email, phone):
        query = """
            INSERT INTO Teachers (FullName, Department, Email, Phone) 
            VALUES (?, ?, ?, ?)
        """
        return self.execute_query(query, (name, department, email, phone))

    def get_all_teachers(self):
        print("Fetching all teachers...")
        query = "SELECT TeacherID, FullName, Department, Email, Phone FROM Teachers ORDER BY TeacherID"
        results = self.fetch_all(query)
        print(f"Found {len(results) if results else 0} teachers")
        return results

    def get_teacher(self, teacher_id):
        query = "SELECT TeacherID, FullName, Department, Email, Phone FROM Teachers WHERE TeacherID = ?"
        return self.fetch_one(query, (teacher_id,))

    def update_teacher(self, teacher_id, name, department, email, phone):
        query = """
            UPDATE Teachers 
            SET FullName = ?, Department = ?, Email = ?, Phone = ? 
            WHERE TeacherID = ?
        """
        return self.execute_query(query, (name, department, email, phone, teacher_id))

    def delete_teacher(self, teacher_id):
        query = "DELETE FROM Teachers WHERE TeacherID = ?"
        return self.execute_query(query, (teacher_id,))

    def add_class(self, name, teacher_id=None):
        query = """
            INSERT INTO Classes (ClassName, TeacherID) 
            VALUES (?, ?)
        """
        return self.execute_query(query, (name, teacher_id))

    def get_all_classes(self):
        print("Fetching all classes...")
        query = """
            SELECT c.ClassID, c.ClassName, ISNULL(t.FullName, 'No Teacher') as TeacherName
            FROM Classes c
            LEFT JOIN Teachers t ON c.TeacherID = t.TeacherID
            ORDER BY c.ClassID
        """
        results = self.fetch_all(query)
        print(f"Found {len(results) if results else 0} classes")
        return results

    def get_class(self, class_id):
        query = "SELECT ClassID, ClassName, TeacherID FROM Classes WHERE ClassID = ?"
        return self.fetch_one(query, (class_id,))

    def assign_teacher_to_class(self, class_id, teacher_id):
        query = "UPDATE Classes SET TeacherID = ? WHERE ClassID = ?"
        return self.execute_query(query, (teacher_id, class_id))

    def delete_class(self, class_id):
        query = "DELETE FROM Classes WHERE ClassID = ?"
        return self.execute_query(query, (class_id,))

    def add_subject(self, name, description):
        query = """
            INSERT INTO Subjects (SubjectName, Description) 
            VALUES (?, ?)
        """
        return self.execute_query(query, (name, description))

    def get_all_subjects(self):
        print("Fetching all subjects...")
        query = "SELECT SubjectID, SubjectName, Description FROM Subjects ORDER BY SubjectID"
        results = self.fetch_all(query)
        print(f"Found {len(results) if results else 0} subjects")
        return results

    def get_subject(self, subject_id):
        query = "SELECT SubjectID, SubjectName, Description FROM Subjects WHERE SubjectID = ?"
        return self.fetch_one(query, (subject_id,))

    def update_subject(self, subject_id, name, description):
        query = """
            UPDATE Subjects 
            SET SubjectName = ?, Description = ? 
            WHERE SubjectID = ?
        """
        return self.execute_query(query, (name, description, subject_id))

    def delete_subject(self, subject_id):
        query = "DELETE FROM Subjects WHERE SubjectID = ?"
        return self.execute_query(query, (subject_id,))

    def assign_subject_to_class(self, class_id, subject_id):
        query = "INSERT INTO ClassSubjects (ClassID, SubjectID) VALUES (?, ?)"
        return self.execute_query(query, (class_id, subject_id))

    def get_class_subjects(self, class_id):
        query = """
            SELECT s.SubjectID, s.SubjectName, s.Description
            FROM Subjects s
            JOIN ClassSubjects cs ON s.SubjectID = cs.SubjectID
            WHERE cs.ClassID = ?
            ORDER BY s.SubjectName
        """
        return self.fetch_all(query, (class_id,))

    def enroll_student_in_class(self, student_id, class_id):
        query = "INSERT INTO Enrollments (StudentID, ClassID) VALUES (?, ?)"
        return self.execute_query(query, (student_id, class_id))

    def get_all_enrollments(self):
        print("Fetching all enrollments...")
        query = """
            SELECT e.StudentID, s.FullName, c.ClassName, e.EnrollmentDate
            FROM Enrollments e
            JOIN Students s ON e.StudentID = s.StudentID
            JOIN Classes c ON e.ClassID = c.ClassID
            ORDER BY s.FullName
        """
        results = self.fetch_all(query)
        print(f"Found {len(results) if results else 0} enrollments")
        return results

    def get_class_enrollments_by_name(self, class_name):
        if class_name == 'All Classes':
            return self.get_all_enrollments()
            
        print(f"Fetching enrollments for class: {class_name}")
        query = """
            SELECT e.StudentID, s.FullName, c.ClassName, e.EnrollmentDate
            FROM Enrollments e
            JOIN Students s ON e.StudentID = s.StudentID
            JOIN Classes c ON e.ClassID = c.ClassID
            WHERE c.ClassName = ?
            ORDER BY s.FullName
        """
        results = self.fetch_all(query, (class_name,))
        print(f"Found {len(results) if results else 0} enrollments for class {class_name}")
        return results

    def get_class_enrollments(self, class_id):
        print(f"Fetching enrollments for class ID: {class_id}")
        query = """
            SELECT s.StudentID, s.FullName
            FROM Students s
            JOIN Enrollments e ON s.StudentID = e.StudentID
            WHERE e.ClassID = ?
            ORDER BY s.FullName
        """
        results = self.fetch_all(query, (class_id,))
        print(f"Found {len(results) if results else 0} enrollments for class ID {class_id}")
        return results

    def delete_enrollment(self, student_id, class_name):
        print(f"Deleting enrollment for student {student_id} in class {class_name}")
        query = """
            DELETE FROM Enrollments 
            WHERE StudentID = ? AND ClassID IN (
                SELECT ClassID FROM Classes WHERE ClassName = ?
            )
        """
        return self.execute_query(query, (student_id, class_name))

    
    def add_grade(self, student_id, class_id, subject_id, grade):
        query = """
            INSERT INTO Grades (StudentID, SubjectID, ClassID, Grade) 
            VALUES (?, ?, ?, ?)
        """
        return self.execute_query(query, (student_id, subject_id, class_id, grade))

    def get_all_grades(self):
        print("Fetching all grades...")
        query = """
            SELECT g.GradeID, s.FullName, c.ClassName, sub.SubjectName, g.Grade
            FROM Grades g
            JOIN Students s ON g.StudentID = s.StudentID
            JOIN Classes c ON g.ClassID = c.ClassID
            JOIN Subjects sub ON g.SubjectID = sub.SubjectID
            ORDER BY s.FullName, sub.SubjectName
        """
        results = self.fetch_all(query)
        print(f"Found {len(results) if results else 0} grades")
        return results

    def get_grade(self, grade_id):
        query = """
            SELECT g.GradeID, s.FullName, c.ClassName, sub.SubjectName, g.Grade
            FROM Grades g
            JOIN Students s ON g.StudentID = s.StudentID
            JOIN Classes c ON g.ClassID = c.ClassID
            JOIN Subjects sub ON g.SubjectID = sub.SubjectID
            WHERE g.GradeID = ?
        """
        return self.fetch_one(query, (grade_id,))

    def get_filtered_grades(self, class_filter, subject_filter):
        print(f"Fetching grades with filters - Class: {class_filter}, Subject: {subject_filter}")
        base_query = """
            SELECT g.GradeID, s.FullName, c.ClassName, sub.SubjectName, g.Grade
            FROM Grades g
            INNER JOIN Students s ON g.StudentID = s.StudentID
            INNER JOIN Classes c ON g.ClassID = c.ClassID
            INNER JOIN Subjects sub ON g.SubjectID = sub.SubjectID
            WHERE 1=1
        """
        params = []
        
        if class_filter and class_filter != 'All':
            base_query += " AND c.ClassName = ?"
            params.append(class_filter)
            
        if subject_filter and subject_filter != 'All':
            base_query += " AND sub.SubjectName = ?"
            params.append(subject_filter)
            
        base_query += " ORDER BY s.FullName, sub.SubjectName"
        
        try:
            results = self.fetch_all(base_query, tuple(params) if params else None)
            print(f"Found {len(results) if results else 0} grades")
            if not results:
                print("No grades found with the current filters")
            return results
        except Exception as e:
            print(f"Error in get_filtered_grades: {str(e)}")
            return []

    def update_grade(self, grade_id, new_grade):
        query = "UPDATE Grades SET Grade = ? WHERE GradeID = ?"
        return self.execute_query(query, (new_grade, grade_id))

    def delete_grade(self, grade_id):
        query = "DELETE FROM Grades WHERE GradeID = ?"
        return self.execute_query(query, (grade_id,))

    
    def get_class_performance_report(self, class_name):
        query = """
            SELECT sub.SubjectName,
                   AVG(g.Grade) as AvgGrade,
                   MAX(g.Grade) as MaxGrade,
                   MIN(g.Grade) as MinGrade,
                   COUNT(DISTINCT g.StudentID) as StudentCount
            FROM Grades g
            JOIN Classes c ON g.ClassID = c.ClassID
            JOIN Subjects sub ON g.SubjectID = sub.SubjectID
            WHERE c.ClassName = ?
            GROUP BY sub.SubjectName
            ORDER BY sub.SubjectName
        """
        return self.fetch_all(query, (class_name,))

    def get_teacher_load_report(self, teacher_name):
        query = """
            SELECT c.ClassName,
                   COUNT(DISTINCT e.StudentID) as StudentCount,
                   STRING_AGG(CONVERT(NVARCHAR(MAX), s.SubjectName), ', ') as Subjects,
                   COUNT(DISTINCT s.SubjectID) * 3 as TotalHours
            FROM Classes c
            JOIN Teachers t ON c.TeacherID = t.TeacherID
            LEFT JOIN Enrollments e ON c.ClassID = e.ClassID
            LEFT JOIN ClassSubjects cs ON c.ClassID = cs.ClassID
            LEFT JOIN Subjects s ON cs.SubjectID = s.SubjectID
            WHERE t.FullName = ?
            GROUP BY c.ClassName
            ORDER BY c.ClassName
        """
        return self.fetch_all(query, (teacher_name,))

    def get_student_grades(self, student_name):
        print(f"Fetching grades for student: {student_name}")
        try:
            
            query = """
                SELECT sub.SubjectName, g.Grade, c.ClassName, NULL as GradeDate
                FROM Grades g
                JOIN Students s ON g.StudentID = s.StudentID
                JOIN Classes c ON g.ClassID = c.ClassID
                JOIN Subjects sub ON g.SubjectID = sub.SubjectID
                WHERE s.FullName = ?
                ORDER BY sub.SubjectName
            """
            results = self.fetch_all(query, (student_name,))
            print(f"Found {len(results) if results else 0} grades for student {student_name}")
            return results
        except Exception as e:
            print(f"Error in get_student_grades: {str(e)}")
            return []
            
    
    def get_class_average_grades(self):
        query = """
            SELECT c.ClassName, AVG(g.Grade) as AvgGrade
            FROM Grades g
            JOIN Classes c ON g.ClassID = c.ClassID
            GROUP BY c.ClassName
            ORDER BY c.ClassName
        """
        return self.fetch_all(query)
    
    def get_subject_average_grades(self):
        query = """
            SELECT sub.SubjectName, AVG(g.Grade) as AvgGrade
            FROM Grades g
            JOIN Subjects sub ON g.SubjectID = sub.SubjectID
            GROUP BY sub.SubjectName
            ORDER BY sub.SubjectName
        """
        return self.fetch_all(query)
    
    def get_gender_distribution(self):
        query = """
            SELECT Gender, COUNT(*) as Count
            FROM Students
            GROUP BY Gender
        """
        return self.fetch_all(query)
    
    def get_class_enrollment_counts(self):
        query = """
            SELECT c.ClassName, COUNT(e.StudentID) as StudentCount
            FROM Classes c
            LEFT JOIN Enrollments e ON c.ClassID = e.ClassID
            GROUP BY c.ClassName
            ORDER BY c.ClassName
        """
        return self.fetch_all(query)
    
    def get_grade_distribution(self):
        try:
            print("Fetching grade distribution data...")
            query = """
                SELECT 
                    CASE
                        WHEN Grade >= 90 THEN 'A (90-100)'
                        WHEN Grade >= 80 THEN 'B (80-89)'
                        WHEN Grade >= 70 THEN 'C (70-79)'
                        WHEN Grade >= 60 THEN 'D (60-69)'
                        ELSE 'F (Below 60)'
                    END as GradeRange,
                    COUNT(*) as Count
                FROM Grades
                GROUP BY 
                    CASE
                        WHEN Grade >= 90 THEN 'A (90-100)'
                        WHEN Grade >= 80 THEN 'B (80-89)'
                        WHEN Grade >= 70 THEN 'C (70-79)'
                        WHEN Grade >= 60 THEN 'D (60-69)'
                        ELSE 'F (Below 60)'
                    END
                ORDER BY 
                    CASE GradeRange
                        WHEN 'A (90-100)' THEN 1
                        WHEN 'B (80-89)' THEN 2
                        WHEN 'C (70-79)' THEN 3
                        WHEN 'D (60-69)' THEN 4
                        WHEN 'F (Below 60)' THEN 5
                    END
            """
            result = self.fetch_all(query)
            print(f"Found {len(result) if result else 0} grade distribution records")
            return result
        except Exception as e:
            print(f"Error in get_grade_distribution: {str(e)}")
            return []
