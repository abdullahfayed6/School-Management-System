# School Management System

A comprehensive GUI-based School Management System built with Python, Tkinter, and SQL Server. This application provides an intuitive interface for managing students, teachers, classes, subjects, enrollments, and grades.

## Features

- **Student Management**: Add, edit, delete, and search student records
- **Teacher Management**: Manage teacher information, assignments, and departments
- **Class Management**: Create and manage classes with assigned teachers
- **Subject Management**: Define and organize academic subjects
- **Enrollment System**: Track student enrollment across different classes
- **Grade Management**: Record, analyze, and report on student grades
- **Data Visualization**: Interactive graphs for student performance, grade distribution, gender demographics, and more
- **Reporting**: Generate detailed reports on class performance, teacher workload, and student achievements

## Technology Stack

- **Frontend**: Python Tkinter with TTK themed widgets
- **Backend**: Python 
- **Database**: Microsoft SQL Server
- **Data Visualization**: Matplotlib

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Microsoft SQL Server
- SQL Server ODBC drivers
- Required Python packages (see requirements below)

### Required Python Packages

- pyodbc
- matplotlib
- numpy
- tkinter (included with Python)
- ttkthemes

### Installation

1. Clone the repository to your local machine
2. Set up a SQL Server database named 'school'
3. Run the `create_schema.py` script to set up the database tables:
   ```powershell
   python create_schema.py
   ```
4. Run the application:
   ```powershell
   python gui_app.py
   ```

## Database Configuration

The application connects to a SQL Server database. Update the connection settings in `database_connection.py` if needed:

```python
def __init__(self):
    self.SERVER_NAME = 'Abdallah' 
    self.DATABASE_NAME = 'school'   
    self.connection = None
    self.cursor = None
```

## Project Structure

- `gui_app.py`: Main application file with GUI implementation
- `database_connection.py`: Handles database connectivity
- `database_operations.py`: Contains all database operations and queries
- `create_schema.py`: Creates the database schema for first-time setup
- `grade_graph.py`: Supports grade distribution visualizations

## Usage

After launching the application, use the navigation menu to access different sections:

- **Students**: Manage student information
- **Teachers**: Add or modify teacher records
- **Classes**: Create and manage class groups
- **Subjects**: Define academic subjects
- **Enrollments**: Assign students to classes
- **Grades**: Record and view student grades
- **Reports**: Generate various analytical reports
- **Graphs**: View visual representations of school data

## Data Visualization

The system provides several visualization options:

1. **Class Performance**: Bar chart showing average grades by class
2. **Subject Performance**: Horizontal bar chart of performance by subject
3. **Student Demographics**: Pie chart of gender distribution
4. **Enrollment Distribution**: Bar chart showing enrollment numbers by class
5. **Grade Distribution**: Pie chart showing grade ranges (A-F)

## License

This project is for educational purposes.

## Acknowledgements

- The ttkthemes library for enhancing the GUI appearance
- Matplotlib for data visualization capabilities
- PyODBC for SQL Server connectivity
