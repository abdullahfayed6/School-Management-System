import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk
from database_operations import DatabaseOperations
from database_connection import DatabaseConnection
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class SchoolManagementGUI:
    def __init__(self):
        self.root = ThemedTk(theme="arc")
        self.root.title("School Management System")
        self.root.geometry("1200x800")
        
        print("Initializing School Management System...")
        
        style = ttk.Style()
        style.configure('Action.TButton', padding=5)
        
        self.db_ops = DatabaseOperations()
        
        self.main_content = ttk.Frame(self.root, padding="10")
        self.main_content.pack(fill=tk.BOTH, expand=True)
        
        self.create_navigation()
        
        self.content_frame = ttk.Frame(self.main_content)
        self.content_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        print("GUI initialized, showing students section...")
        self.show_students()

    def create_navigation(self):
        nav_frame = ttk.LabelFrame(self.main_content, text="Navigation", padding="10")
        nav_frame.pack(fill=tk.X, padx=5, pady=5)

        button_style = {'width': 15, 'padding': 5}
        
        ttk.Button(nav_frame, text="Students", command=self.show_students, **button_style).pack(side=tk.LEFT, padx=5)
        ttk.Button(nav_frame, text="Teachers", command=self.show_teachers, **button_style).pack(side=tk.LEFT, padx=5)
        ttk.Button(nav_frame, text="Classes", command=self.show_classes, **button_style).pack(side=tk.LEFT, padx=5)
        ttk.Button(nav_frame, text="Subjects", command=self.show_subjects, **button_style).pack(side=tk.LEFT, padx=5)
        ttk.Button(nav_frame, text="Enrollments", command=self.show_enrollments, **button_style).pack(side=tk.LEFT, padx=5)
        ttk.Button(nav_frame, text="Grades", command=self.show_grades, **button_style).pack(side=tk.LEFT, padx=5)
        ttk.Button(nav_frame, text="Reports", command=self.show_reports, **button_style).pack(side=tk.LEFT, padx=5)
        ttk.Button(nav_frame, text="Graphs", command=self.show_graphs, **button_style).pack(side=tk.LEFT, padx=5)

    def clear_main_content(self):
        print("Clearing main content...")
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def create_table(self, columns, show="headings"):
        tree = ttk.Treeview(self.content_frame, columns=columns, show=show)
        
        for col in columns:
            tree.heading(col, text=col.title())
            tree.column(col, width=150)
        
        y_scroll = ttk.Scrollbar(self.content_frame, orient="vertical", command=tree.yview)
        x_scroll = ttk.Scrollbar(self.content_frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
        
        tree.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll.grid(row=1, column=0, sticky="ew")
        
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)
        
        return tree

    def create_action_buttons(self, header_frame, tree, add_command, edit_command=None, delete_command=None):
        button_frame = ttk.Frame(header_frame)
        button_frame.pack(side=tk.RIGHT, padx=5)
        
        add_btn = ttk.Button(button_frame, text="Add New", command=add_command, style='Action.TButton')
        add_btn.pack(side=tk.LEFT, padx=2)
        
        if edit_command:
            edit_btn = ttk.Button(button_frame, text="Edit", command=lambda: self.handle_edit(tree, edit_command), style='Action.TButton')
            edit_btn.pack(side=tk.LEFT, padx=2)
        
        if delete_command:
            delete_btn = ttk.Button(button_frame, text="Delete", command=lambda: self.handle_delete(tree, delete_command), style='Action.TButton')
            delete_btn.pack(side=tk.LEFT, padx=2)

    def handle_edit(self, tree, edit_command):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an item to edit")
            return
        edit_command(tree)

    def handle_delete(self, tree, delete_command):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an item to delete")
            return
        delete_command(tree)

    def show_students(self):
        self.clear_main_content()
        
        header_frame = ttk.Frame(self.content_frame)
        header_frame.pack(fill=tk.X, padx=5, pady=(0, 20))
        
        ttk.Label(header_frame, text="Students Management", font=('Helvetica', 16, 'bold')).pack(side=tk.LEFT, padx=5)
        
        button_frame = ttk.Frame(header_frame)
        button_frame.pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(button_frame, text="Add New Student", 
                  command=self.show_add_student_dialog,
                  style='Action.TButton').pack(side=tk.LEFT, padx=2)
        
        ttk.Button(button_frame, text="Edit Student",
                  command=lambda: self.show_edit_student_dialog(tree),
                  style='Action.TButton').pack(side=tk.LEFT, padx=2)
        
        ttk.Button(button_frame, text="Delete Student",
                  command=lambda: self.delete_student(tree),
                  style='Action.TButton').pack(side=tk.LEFT, padx=2)
        
        search_frame = ttk.LabelFrame(self.content_frame, text="Search", padding="5")
        search_frame.pack(fill=tk.X, padx=5, pady=(0, 10))
        
        ttk.Label(search_frame, text="Search by name:").pack(side=tk.LEFT, padx=5)
        search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=search_var, width=40)
        search_entry.pack(side=tk.LEFT, padx=5)
        
        table_frame = ttk.Frame(self.content_frame)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
        
        columns = ("ID", "Name", "DOB", "Gender", "Email", "Phone", "Address")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        col_widths = {
            "ID": 50,
            "Name": 150,
            "DOB": 100,
            "Gender": 60,
            "Email": 150,
            "Phone": 120,
            "Address": 200
        }
        
        for col in columns:
            tree.heading(col, text=col.title())
            tree.column(col, width=col_widths.get(col, 120), minwidth=50)
        
        y_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        x_scroll = ttk.Scrollbar(table_frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
        
        tree.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll.grid(row=1, column=0, sticky="ew")
        
        def filter_students(*args):
            search_text = search_var.get().lower()
            
            for item in tree.get_children():
                tree.delete(item)
            
            students = self.db_ops.get_all_students()
            for student in students:
                if not search_text or search_text in str(student[1]).lower():
                    student_id = student[0]
                    full_name = student[1]
                    dob = student[2].strftime('%Y-%m-%d') if student[2] else ''
                    gender = student[3]
                    email = student[4] or ''
                    phone = student[5] or ''
                    address = student[6] or ''
                    
                    formatted_values = (
                        student_id,
                        full_name,
                        dob,
                        gender,
                        email,
                        phone,
                        address
                    )
                    tree.insert("", tk.END, values=formatted_values)
        
        search_var.trace('w', filter_students)
        
        context_menu = tk.Menu(tree, tearoff=0)
        context_menu.add_command(label="Edit Student", command=lambda: self.show_edit_student_dialog(tree))
        context_menu.add_command(label="Delete Student", command=lambda: self.delete_student(tree))
        
        def show_context_menu(event):
            item = tree.identify_row(event.y)
            if item:
                tree.selection_set(item)
                context_menu.post(event.x_root, event.y_root)
        
        tree.bind("<Button-3>", show_context_menu)
        
        filter_students()

    def show_add_student_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Student")
        dialog.geometry("400x500")
        
        ttk.Label(dialog, text="Full Name:").pack(pady=5)
        name_entry = ttk.Entry(dialog, width=40)
        name_entry.pack()
        
        ttk.Label(dialog, text="Date of Birth (YYYY-MM-DD):").pack(pady=5)
        dob_entry = ttk.Entry(dialog, width=40)
        dob_entry.pack()
        
        ttk.Label(dialog, text="Gender (M/F):").pack(pady=5)
        gender_entry = ttk.Entry(dialog, width=40)
        gender_entry.pack()
        
        ttk.Label(dialog, text="Email:").pack(pady=5)
        email_entry = ttk.Entry(dialog, width=40)
        email_entry.pack()
        
        ttk.Label(dialog, text="Phone:").pack(pady=5)
        phone_entry = ttk.Entry(dialog, width=40)
        phone_entry.pack()
        
        ttk.Label(dialog, text="Address:").pack(pady=5)
        address_entry = ttk.Entry(dialog, width=40)
        address_entry.pack()
        
        def save_student():
            try:
                dob = datetime.datetime.strptime(dob_entry.get(), "%Y-%m-%d").date()
                if self.db_ops.add_student(
                    name_entry.get(),
                    dob,
                    gender_entry.get().upper(),
                    email_entry.get(),
                    phone_entry.get(),
                    address_entry.get()
                ):
                    messagebox.showinfo("Success", "Student added successfully!")
                    dialog.destroy()
                    self.show_students()
                else:
                    messagebox.showerror("Error", "Failed to add student")
            except ValueError:
                messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD")
        
        ttk.Button(dialog, text="Save", command=save_student).pack(pady=20)

    def show_edit_student_dialog(self, tree):
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a student to edit")
            return
        
        student_id = tree.item(selected_item)['values'][0]
        student = self.db_ops.get_student(student_id)
        if not student:
            messagebox.showerror("Error", "Student not found")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Student")
        dialog.geometry("400x500")
        
        ttk.Label(dialog, text="Full Name:").pack(pady=5)
        name_entry = ttk.Entry(dialog, width=40)
        name_entry.insert(0, student[1])
        name_entry.pack()
        
        ttk.Label(dialog, text="Date of Birth (YYYY-MM-DD):").pack(pady=5)
        dob_entry = ttk.Entry(dialog, width=40)
        dob_entry.insert(0, student[2].strftime('%Y-%m-%d') if student[2] else '')
        dob_entry.pack()
        
        ttk.Label(dialog, text="Gender (M/F):").pack(pady=5)
        gender_entry = ttk.Entry(dialog, width=40)
        gender_entry.insert(0, student[3])
        gender_entry.pack()
        
        ttk.Label(dialog, text="Email:").pack(pady=5)
        email_entry = ttk.Entry(dialog, width=40)
        email_entry.insert(0, student[4] or '')
        email_entry.pack()
        
        ttk.Label(dialog, text="Phone:").pack(pady=5)
        phone_entry = ttk.Entry(dialog, width=40)
        phone_entry.insert(0, student[5] or '')
        phone_entry.pack()
        
        ttk.Label(dialog, text="Address:").pack(pady=5)
        address_entry = ttk.Entry(dialog, width=40)
        address_entry.insert(0, student[6] or '')
        address_entry.pack()
        
        def update_student():
            try:
                dob = datetime.datetime.strptime(dob_entry.get(), "%Y-%m-%d").date()
                if self.db_ops.update_student(
                    student_id,
                    name_entry.get(),
                    dob,
                    gender_entry.get().upper(),
                    email_entry.get(),
                    phone_entry.get(),
                    address_entry.get()
                ):
                    messagebox.showinfo("Success", "Student updated successfully!")
                    dialog.destroy()
                    self.show_students()
                else:
                    messagebox.showerror("Error", "Failed to update student")
            except ValueError:
                messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD")
        
        ttk.Button(dialog, text="Update", command=update_student).pack(pady=20)

    def delete_student(self, tree):
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a student to delete")
            return
        
        student_id = tree.item(selected_item)['values'][0]
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this student?"):
            if self.db_ops.delete_student(student_id):
                messagebox.showinfo("Success", "Student deleted successfully!")
                self.show_students()
            else:
                messagebox.showerror("Error", "Failed to delete student")

    def show_teachers(self):
        self.clear_main_content()
        
        header_frame = ttk.Frame(self.content_frame)
        header_frame.pack(fill=tk.X, padx=5, pady=(0, 20))
        
        ttk.Label(header_frame, text="Teachers Management", font=('Helvetica', 16, 'bold')).pack(side=tk.LEFT)
        
        button_frame = ttk.Frame(header_frame)
        button_frame.pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(button_frame, text="Add New Teacher", 
                  command=self.show_add_teacher_dialog,
                  style='Action.TButton').pack(side=tk.LEFT, padx=2)
        
        ttk.Button(button_frame, text="Edit Teacher",
                  command=lambda: self.show_edit_teacher_dialog(tree),
                  style='Action.TButton').pack(side=tk.LEFT, padx=2)
        
        ttk.Button(button_frame, text="Delete Teacher",
                  command=lambda: self.delete_teacher(tree),
                  style='Action.TButton').pack(side=tk.LEFT, padx=2)
        
        search_frame = ttk.LabelFrame(self.content_frame, text="Search", padding="5")
        search_frame.pack(fill=tk.X, padx=5, pady=(0, 10))
        
        ttk.Label(search_frame, text="Search by name:").pack(side=tk.LEFT, padx=5)
        search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=search_var, width=40)
        search_entry.pack(side=tk.LEFT, padx=5)
        
        table_frame = ttk.Frame(self.content_frame)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
        
        columns = ("ID", "Name", "Department", "Email", "Phone")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        col_widths = {
            "ID": 60,
            "Name": 180,
            "Department": 150,
            "Email": 180,
            "Phone": 120
        }
        
        for col in columns:
            tree.heading(col, text=col.title())
            tree.column(col, width=col_widths.get(col, 150), minwidth=50)
        
        y_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        x_scroll = ttk.Scrollbar(table_frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
        
        tree.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll.grid(row=1, column=0, sticky="ew")
        
        def filter_teachers(*args):
            search_text = search_var.get().lower()
            
            for item in tree.get_children():
                tree.delete(item)
            
            teachers = self.db_ops.get_all_teachers()
            for teacher in teachers:
                if not search_text or search_text in str(teacher[1]).lower():
                    formatted_values = (
                        teacher[0],
                        teacher[1],
                        teacher[2] or '',
                        teacher[3] or '',
                        teacher[4] or ''
                    )
                    tree.insert("", tk.END, values=formatted_values)
        
        search_var.trace('w', filter_teachers)
        
        context_menu = tk.Menu(tree, tearoff=0)
        context_menu.add_command(label="Edit", command=lambda: self.show_edit_teacher_dialog(tree))
        context_menu.add_command(label="Delete", command=lambda: self.delete_teacher(tree))
        
        def show_context_menu(event):
            item = tree.identify_row(event.y)
            if item:
                tree.selection_set(item)
                context_menu.post(event.x_root, event.y_root)
        
        tree.bind("<Button-3>", show_context_menu)
        
        filter_teachers()

    def show_add_teacher_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Teacher")
        dialog.geometry("400x400")
        
        ttk.Label(dialog, text="Full Name:").pack(pady=5)
        name_entry = ttk.Entry(dialog, width=40)
        name_entry.pack()
        
        ttk.Label(dialog, text="Department:").pack(pady=5)
        department_entry = ttk.Entry(dialog, width=40)
        department_entry.pack()
        
        ttk.Label(dialog, text="Email:").pack(pady=5)
        email_entry = ttk.Entry(dialog, width=40)
        email_entry.pack()
        
        ttk.Label(dialog, text="Phone:").pack(pady=5)
        phone_entry = ttk.Entry(dialog, width=40)
        phone_entry.pack()
        
        def save_teacher():
            if self.db_ops.add_teacher(
                name_entry.get(),
                department_entry.get(),
                email_entry.get(),
                phone_entry.get()
            ):
                messagebox.showinfo("Success", "Teacher added successfully!")
                dialog.destroy()
                self.show_teachers()
            else:
                messagebox.showerror("Error", "Failed to add teacher")
        
        ttk.Button(dialog, text="Save", command=save_teacher).pack(pady=20)

    def show_edit_teacher_dialog(self, tree):
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a teacher to edit")
            return
        
        teacher_id = tree.item(selected_item)['values'][0]
        teacher = self.db_ops.get_teacher(teacher_id)
        if not teacher:
            messagebox.showerror("Error", "Teacher not found")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Teacher")
        dialog.geometry("400x400")
        
        ttk.Label(dialog, text="Full Name:").pack(pady=5)
        name_entry = ttk.Entry(dialog, width=40)
        name_entry.insert(0, teacher[1])
        name_entry.pack()
        
        ttk.Label(dialog, text="Department:").pack(pady=5)
        department_entry = ttk.Entry(dialog, width=40)
        department_entry.insert(0, teacher[5])
        department_entry.pack()
        
        ttk.Label(dialog, text="Email:").pack(pady=5)
        email_entry = ttk.Entry(dialog, width=40)
        email_entry.insert(0, teacher[2] or "")
        email_entry.pack()
        
        ttk.Label(dialog, text="Phone:").pack(pady=5)
        phone_entry = ttk.Entry(dialog, width=40)
        phone_entry.insert(0, teacher[3] or "")
        phone_entry.pack()
        
        def update_teacher():
            if self.db_ops.update_teacher(
                teacher_id,
                name_entry.get(),
                department_entry.get(),
                email_entry.get(),
                phone_entry.get()
            ):
                messagebox.showinfo("Success", "Teacher updated successfully!")
                dialog.destroy()
                self.show_teachers()
            else:
                messagebox.showerror("Error", "Failed to update teacher")
        
        ttk.Button(dialog, text="Update", command=update_teacher).pack(pady=20)

    def delete_teacher(self, tree):
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a teacher to delete")
            return
        
        teacher_id = tree.item(selected_item)['values'][0]
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this teacher?"):
            if self.db_ops.delete_teacher(teacher_id):
                messagebox.showinfo("Success", "Teacher deleted successfully!")
                self.show_teachers()
            else:
                messagebox.showerror("Error", "Failed to delete teacher")

    def show_classes(self):
        self.clear_main_content()
        
        header_frame = ttk.Frame(self.content_frame)
        header_frame.pack(fill=tk.X, padx=5, pady=(0, 20))
        
        ttk.Label(header_frame, text="Classes Management", font=('Helvetica', 16, 'bold')).pack(side=tk.LEFT)
        
        button_frame = ttk.Frame(header_frame)
        button_frame.pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(button_frame, text="Add New Class", 
                  command=self.show_add_class_dialog,
                  style='Action.TButton').pack(side=tk.LEFT, padx=2)
        
        ttk.Button(button_frame, text="View Details",
                  command=lambda: self.show_class_details(tree),
                  style='Action.TButton').pack(side=tk.LEFT, padx=2)
        
        ttk.Button(button_frame, text="Delete Class",
                  command=lambda: self.delete_class(tree),
                  style='Action.TButton').pack(side=tk.LEFT, padx=2)
        
        search_frame = ttk.LabelFrame(self.content_frame, text="Search", padding="5")
        search_frame.pack(fill=tk.X, padx=5, pady=(0, 10))
        
        ttk.Label(search_frame, text="Search by class name:").pack(side=tk.LEFT, padx=5)
        search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=search_var, width=40)
        search_entry.pack(side=tk.LEFT, padx=5)
        
        table_frame = ttk.Frame(self.content_frame)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
        
        columns = ("ID", "Class Name", "Teacher")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        col_widths = {
            "ID": 60,
            "Class Name": 250,
            "Teacher": 250
        }
        
        for col in columns:
            tree.heading(col, text=col.title())
            tree.column(col, width=col_widths.get(col, 150), minwidth=50)
        
        y_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        x_scroll = ttk.Scrollbar(table_frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
        
        tree.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll.grid(row=1, column=0, sticky="ew")
        
        def filter_classes(*args):
            search_text = search_var.get().lower()
            
            for item in tree.get_children():
                tree.delete(item)
            
            classes = self.db_ops.get_all_classes()
            for class_info in classes:
                if not search_text or search_text in str(class_info[1]).lower():
                    formatted_values = (
                        class_info[0],
                        class_info[1],
                        class_info[2] or 'No Teacher'
                    )
                    tree.insert("", tk.END, values=formatted_values)
        
        search_var.trace('w', filter_classes)
        
        context_menu = tk.Menu(tree, tearoff=0)
        context_menu.add_command(label="View Details", command=lambda: self.show_class_details(tree))
        context_menu.add_command(label="Assign Teacher", command=lambda: self.show_assign_teacher_dialog(tree))
        context_menu.add_command(label="Delete", command=lambda: self.delete_class(tree))
        
        def show_context_menu(event):
            item = tree.identify_row(event.y)
            if item:
                tree.selection_set(item)
                context_menu.post(event.x_root, event.y_root)
        
        tree.bind("<Button-3>", show_context_menu)
        tree.bind("<Double-1>", lambda e: self.show_class_details(tree))
        
        filter_classes()

    def show_add_class_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Class")
        dialog.geometry("400x300")
        
        ttk.Label(dialog, text="Class Name:").pack(pady=5)
        name_entry = ttk.Entry(dialog, width=40)
        name_entry.pack()
        
        ttk.Label(dialog, text="Teacher (Optional):").pack(pady=5)
        teachers = self.db_ops.get_all_teachers()
        teacher_var = tk.StringVar()
        teacher_combo = ttk.Combobox(dialog, textvariable=teacher_var, width=37)
        teacher_combo['values'] = ['None'] + [f"{t[0]} - {t[1]}" for t in teachers]
        teacher_combo.set('None')
        teacher_combo.pack()
        
        def save_class():
            teacher_id = None
            if teacher_combo.get() != 'None':
                teacher_id = int(teacher_combo.get().split(' - ')[0])
                
            if self.db_ops.add_class(name_entry.get(), teacher_id):
                messagebox.showinfo("Success", "Class added successfully!")
                dialog.destroy()
                self.show_classes()
            else:
                messagebox.showerror("Error", "Failed to add class")
        
        ttk.Button(dialog, text="Save", command=save_class).pack(pady=20)

    def show_class_details(self, tree):
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a class to view")
            return
        
        class_id = tree.item(selected_item)['values'][0]
        
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Class Details - {tree.item(selected_item)['values'][1]}")
        dialog.geometry("800x600")
        
        notebook = ttk.Notebook(dialog)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        students_frame = ttk.Frame(notebook)
        notebook.add(students_frame, text='Students')
        students_frame.columnconfigure(0, weight=1)
        students_frame.rowconfigure(0, weight=1)
        
        columns = ("ID", "Name", "Gender", "Email")
        students_tree = ttk.Treeview(students_frame, columns=columns, show='headings')
        
        col_widths = {
            "ID": 60,
            "Name": 200,
            "Gender": 80,
            "Email": 200
        }
        
        for col in columns:
            students_tree.heading(col, text=col)
            students_tree.column(col, width=col_widths.get(col, 150), minwidth=50)
        
        y_scroll = ttk.Scrollbar(students_frame, orient="vertical", command=students_tree.yview)
        x_scroll = ttk.Scrollbar(students_frame, orient="horizontal", command=students_tree.xview)
        students_tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
        
        students_tree.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll.grid(row=1, column=0, sticky="ew")
        
        subjects_frame = ttk.Frame(notebook)
        notebook.add(subjects_frame, text='Subjects')
        subjects_frame.columnconfigure(0, weight=1)
        subjects_frame.rowconfigure(0, weight=1)
        
        columns = ("ID", "Subject Name", "Description")
        subjects_tree = ttk.Treeview(subjects_frame, columns=columns, show='headings')
        
        col_widths = {
            "ID": 60,
            "Subject Name": 200,
            "Description": 400
        }
        
        for col in columns:
            subjects_tree.heading(col, text=col)
            subjects_tree.column(col, width=col_widths.get(col, 150), minwidth=50)
        
        y_scroll = ttk.Scrollbar(subjects_frame, orient="vertical", command=subjects_tree.yview)
        x_scroll = ttk.Scrollbar(subjects_frame, orient="horizontal", command=subjects_tree.xview)
        subjects_tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
        
        subjects_tree.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll.grid(row=1, column=0, sticky="ew")
        
        enrollments = self.db_ops.get_class_enrollments(class_id)
        for enrollment in enrollments:
            students_tree.insert("", tk.END, values=enrollment)
        
        subjects = self.db_ops.get_class_subjects(class_id)
        for subject in subjects:
            subjects_tree.insert("", tk.END, values=subject)

    def show_assign_teacher_dialog(self, tree):
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a class")
            return
            
        class_id = tree.item(selected_item)['values'][0]
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Assign Teacher")
        dialog.geometry("400x200")
        
        ttk.Label(dialog, text="Select Teacher:").pack(pady=5)
        teachers = self.db_ops.get_all_teachers()
        teacher_var = tk.StringVar()
        teacher_combo = ttk.Combobox(dialog, textvariable=teacher_var, width=37)
        teacher_combo['values'] = [f"{t[0]} - {t[1]}" for t in teachers]
        teacher_combo.pack()
        
        def assign_teacher():
            if not teacher_combo.get():
                messagebox.showwarning("Warning", "Please select a teacher")
                return
            
            teacher_id = int(teacher_combo.get().split(' - ')[0])
            if self.db_ops.assign_teacher_to_class(class_id, teacher_id):
                messagebox.showinfo("Success", "Teacher assigned successfully!")
                dialog.destroy()
                self.show_classes()
            else:
                messagebox.showerror("Error", "Failed to assign teacher")
        
        ttk.Button(dialog, text="Assign", command=assign_teacher).pack(pady=20)

    def delete_class(self, tree):
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a class to delete")
            return
            
        class_id = tree.item(selected_item)['values'][0]
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this class?"):
            if self.db_ops.delete_class(class_id):
                messagebox.showinfo("Success", "Class deleted successfully!")
                self.show_classes()
            else:
                messagebox.showerror("Error", "Failed to delete class")

    def show_subjects(self):
        self.clear_main_content()
        
        header_frame = ttk.Frame(self.content_frame)
        header_frame.pack(fill=tk.X, padx=5, pady=(0, 20))
        
        ttk.Label(header_frame, text="Subjects Management", font=('Helvetica', 16, 'bold')).pack(side=tk.LEFT)
        
        button_frame = ttk.Frame(header_frame)
        button_frame.pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(button_frame, text="Add New Subject", 
                  command=self.show_add_subject_dialog,
                  style='Action.TButton').pack(side=tk.LEFT, padx=2)
        
        ttk.Button(button_frame, text="Edit Subject",
                  command=lambda: self.show_edit_subject_dialog(tree),
                  style='Action.TButton').pack(side=tk.LEFT, padx=2)
        
        ttk.Button(button_frame, text="Delete Subject",
                  command=lambda: self.delete_subject(tree),
                  style='Action.TButton').pack(side=tk.LEFT, padx=2)
        
        search_frame = ttk.LabelFrame(self.content_frame, text="Search", padding="5")
        search_frame.pack(fill=tk.X, padx=5, pady=(0, 10))
        
        ttk.Label(search_frame, text="Search by subject name:").pack(side=tk.LEFT, padx=5)
        search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=search_var, width=40)
        search_entry.pack(side=tk.LEFT, padx=5)
        
        table_frame = ttk.Frame(self.content_frame)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
        
        columns = ("ID", "Subject Name", "Description")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        col_widths = {
            "ID": 60,
            "Subject Name": 200,
            "Description": 400
        }
        
        for col in columns:
            tree.heading(col, text=col.title())
            tree.column(col, width=col_widths.get(col, 150), minwidth=50)
        
        y_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        x_scroll = ttk.Scrollbar(table_frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
        
        tree.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll.grid(row=1, column=0, sticky="ew")
        
        def filter_subjects(*args):
            search_text = search_var.get().lower()
            
            for item in tree.get_children():
                tree.delete(item)
            
            subjects = self.db_ops.get_all_subjects()
            for subject in subjects:
                if not search_text or search_text in str(subject[1]).lower():
                    formatted_values = (
                        subject[0],
                        subject[1],
                        subject[2] or ''
                    )
                    tree.insert("", tk.END, values=formatted_values)
        
        search_var.trace('w', filter_subjects)
        
        context_menu = tk.Menu(tree, tearoff=0)
        context_menu.add_command(label="Edit", command=lambda: self.show_edit_subject_dialog(tree))
        context_menu.add_command(label="Delete", command=lambda: self.delete_subject(tree))
        
        def show_context_menu(event):
            item = tree.identify_row(event.y)
            if item:
                tree.selection_set(item)
                context_menu.post(event.x_root, event.y_root)
        
        tree.bind("<Button-3>", show_context_menu)
        
        filter_subjects()

    def show_add_subject_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Subject")
        dialog.geometry("400x300")
        
        ttk.Label(dialog, text="Subject Name:").pack(pady=5)
        name_entry = ttk.Entry(dialog, width=40)
        name_entry.pack()
        
        ttk.Label(dialog, text="Description:").pack(pady=5)
        description_text = tk.Text(dialog, width=40, height=5)
        description_text.pack()
        
        def save_subject():
            if self.db_ops.add_subject(
                name_entry.get(),
                description_text.get("1.0", tk.END).strip()
            ):
                messagebox.showinfo("Success", "Subject added successfully!")
                dialog.destroy()
                self.show_subjects()
            else:
                messagebox.showerror("Error", "Failed to add subject")
        
        ttk.Button(dialog, text="Save", command=save_subject).pack(pady=20)

    def show_edit_subject_dialog(self, tree):
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a subject to edit")
            return
        
        subject_id = tree.item(selected_item)['values'][0]
        subject = self.db_ops.get_subject(subject_id)
        if not subject:
            messagebox.showerror("Error", "Subject not found")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Subject")
        dialog.geometry("400x300")
        
        ttk.Label(dialog, text="Subject Name:").pack(pady=5)
        name_entry = ttk.Entry(dialog, width=40)
        name_entry.insert(0, subject[1])
        name_entry.pack()
        
        ttk.Label(dialog, text="Description:").pack(pady=5)
        description_text = tk.Text(dialog, width=40, height=5)
        description_text.insert("1.0", subject[2] or "")
        description_text.pack()
        
        def update_subject():
            if self.db_ops.update_subject(
                subject_id,
                name_entry.get(),
                description_text.get("1.0", tk.END).strip()
            ):
                messagebox.showinfo("Success", "Subject updated successfully!")
                dialog.destroy()
                self.show_subjects()
            else:
                messagebox.showerror("Error", "Failed to update subject")
        
        ttk.Button(dialog, text="Update", command=update_subject).pack(pady=20)

    def delete_subject(self, tree):
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a subject to delete")
            return
        
        subject_id = tree.item(selected_item)['values'][0]
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this subject?"):
            if self.db_ops.delete_subject(subject_id):
                messagebox.showinfo("Success", "Subject deleted successfully!")
                self.show_subjects()
            else:
                messagebox.showerror("Error", "Failed to delete subject")

    def show_enrollments(self):
        self.clear_main_content()
        
        header_frame = ttk.Frame(self.content_frame)
        header_frame.pack(fill=tk.X, padx=5, pady=(0, 20))
        
        ttk.Label(header_frame, text="Enrollments Management", font=('Helvetica', 16, 'bold')).pack(side=tk.LEFT)
        
        button_frame = ttk.Frame(header_frame)
        button_frame.pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(button_frame, text="Add New Enrollment", 
                  command=self.show_add_enrollment_dialog,
                  style='Action.TButton').pack(side=tk.LEFT, padx=2)
        
        ttk.Button(button_frame, text="Edit Enrollment",
                  command=lambda: self.show_edit_enrollment_dialog(tree),
                  style='Action.TButton').pack(side=tk.LEFT, padx=2)
        
        ttk.Button(button_frame, text="Delete Enrollment",
                  command=lambda: self.delete_enrollment(tree),
                  style='Action.TButton').pack(side=tk.LEFT, padx=2)
        
        filter_frame = ttk.LabelFrame(self.content_frame, text="Search and Filters", padding="5")
        filter_frame.pack(fill=tk.X, padx=5, pady=(0, 10))
        
        ttk.Label(filter_frame, text="Search by student:").pack(side=tk.LEFT, padx=5)
        search_var = tk.StringVar()
        search_entry = ttk.Entry(filter_frame, textvariable=search_var, width=20)
        search_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(filter_frame, text="Filter by Class:").pack(side=tk.LEFT, padx=5)
        class_var = tk.StringVar(value='All Classes')
        class_combo = ttk.Combobox(filter_frame, textvariable=class_var, width=30)
        classes = self.db_ops.get_all_classes()
        class_combo['values'] = ['All Classes'] + [c[1] for c in classes]
        class_combo.pack(side=tk.LEFT, padx=5)
        
        table_frame = ttk.Frame(self.content_frame)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
        
        columns = ("Student ID", "Student Name", "Class", "Enrollment Date")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        col_widths = {
            "Student ID": 80,
            "Student Name": 200,
            "Class": 180,
            "Enrollment Date": 150
        }
        
        for col in columns:
            tree.heading(col, text=col.title())
            tree.column(col, width=col_widths.get(col, 150), minwidth=50)
        
        y_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        x_scroll = ttk.Scrollbar(table_frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
        
        tree.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll.grid(row=1, column=0, sticky="ew")
        
        def filter_enrollments(*args):
            search_text = search_var.get().lower()
            class_filter = class_var.get()
            
            for item in tree.get_children():
                tree.delete(item)
            
            enrollments = []
            if class_filter == 'All Classes':
                enrollments = self.db_ops.get_all_enrollments()
            else:
                enrollments = self.db_ops.get_class_enrollments_by_name(class_filter)
            
            for enrollment in enrollments:
                if not search_text or search_text in str(enrollment[1]).lower():
                    formatted_values = (
                        enrollment[0],
                        enrollment[1],
                        enrollment[2],
                        enrollment[3].strftime('%Y-%m-%d') if enrollment[3] else ''
                    )
                    tree.insert("", tk.END, values=formatted_values)
        
        search_var.trace('w', filter_enrollments)
        class_combo.bind('<<ComboboxSelected>>', filter_enrollments)
        
        context_menu = tk.Menu(tree, tearoff=0)
        context_menu.add_command(label="Edit", command=lambda: self.show_edit_enrollment_dialog(tree))
        context_menu.add_command(label="Delete", command=lambda: self.delete_enrollment(tree))
        
        def show_context_menu(event):
            item = tree.identify_row(event.y)
            if item:
                tree.selection_set(item)
                context_menu.post(event.x_root, event.y_root)
        
        tree.bind("<Button-3>", show_context_menu)
        
        filter_enrollments()

    def show_add_enrollment_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("New Enrollment")
        dialog.geometry("400x300")
        
        ttk.Label(dialog, text="Select Student:").pack(pady=5)
        students = self.db_ops.get_all_students()
        student_var = tk.StringVar()
        student_combo = ttk.Combobox(dialog, textvariable=student_var, width=37)
        student_combo['values'] = [f"{s[0]} - {s[1]}" for s in students]
        student_combo.pack()
        
        ttk.Label(dialog, text="Select Class:").pack(pady=5)
        classes = self.db_ops.get_all_classes()
        class_var = tk.StringVar()
        class_combo = ttk.Combobox(dialog, textvariable=class_var, width=37)
        class_combo['values'] = [f"{c[0]} - {c[1]}" for c in classes]
        class_combo.pack()
        
        def save_enrollment():
            if not student_combo.get() or not class_combo.get():
                messagebox.showwarning("Warning", "Please select both student and class")
                return
                
            student_id = int(student_combo.get().split(' - ')[0])
            class_id = int(class_combo.get().split(' - ')[0])
            
            enrollments = self.db_ops.get_class_enrollments(class_id)
            for enrollment in enrollments:
                if enrollment[0] == student_id:
                    messagebox.showerror("Error", "Student is already enrolled in this class")
                    return
            
            try:
                if self.db_ops.enroll_student_in_class(student_id, class_id):
                    messagebox.showinfo("Success", "Student enrolled successfully!")
                    dialog.destroy()
                    self.show_enrollments()
                else:
                    messagebox.showerror("Error", "Failed to enroll student")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to enroll student: {str(e)}")
        
        ttk.Button(dialog, text="Enroll", command=save_enrollment).pack(pady=20)

    def show_edit_enrollment_dialog(self, tree):
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an enrollment to edit")
            return
        
        student_id = tree.item(selected_item)['values'][0]
        current_class = tree.item(selected_item)['values'][2]
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Enrollment")
        dialog.geometry("400x300")
        
        ttk.Label(dialog, text=f"Student: {tree.item(selected_item)['values'][1]}").pack(pady=5)
        ttk.Label(dialog, text=f"Current Class: {current_class}").pack(pady=5)
        
        ttk.Label(dialog, text="Select New Class:").pack(pady=5)
        classes = self.db_ops.get_all_classes()
        class_var = tk.StringVar()
        class_combo = ttk.Combobox(dialog, textvariable=class_var, width=37)
        class_combo['values'] = [f"{c[0]} - {c[1]}" for c in classes]
        class_combo.pack(pady=5)
        
        def update_enrollment():
            if not class_combo.get():
                messagebox.showwarning("Warning", "Please select a class")
                return
            
            new_class_id = int(class_combo.get().split(' - ')[0])
            
            if self.db_ops.delete_enrollment(student_id, current_class) and \
               self.db_ops.enroll_student_in_class(student_id, new_class_id):
                messagebox.showinfo("Success", "Enrollment updated successfully!")
                dialog.destroy()
                self.show_enrollments()
            else:
                messagebox.showerror("Error", "Failed to update enrollment")

    def delete_enrollment(self, tree):
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an enrollment to delete")
            return
        
        student_id = tree.item(selected_item)['values'][0]
        class_name = tree.item(selected_item)['values'][2]
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to remove this student from {class_name}?"):
            if self.db_ops.delete_enrollment(student_id, class_name):
                messagebox.showinfo("Success", "Enrollment deleted successfully!")
                self.show_enrollments()
            else:
                messagebox.showerror("Error", "Failed to delete enrollment")

    def show_grades(self):
        self.clear_main_content()
        print("Initializing grades view...")
        
        header_frame = ttk.Frame(self.content_frame)
        header_frame.pack(fill=tk.X, padx=5, pady=(0, 20))
        
        ttk.Label(header_frame, text="Grades Management", font=('Helvetica', 16, 'bold')).pack(side=tk.LEFT)
        
        button_frame = ttk.Frame(header_frame)
        button_frame.pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(button_frame, text="Add New Grade", 
                  command=self.show_add_grade_dialog,
                  style='Action.TButton').pack(side=tk.LEFT, padx=2)
        
        ttk.Button(button_frame, text="Edit Grade",
                  command=lambda: self.show_edit_grade_dialog(tree),
                  style='Action.TButton').pack(side=tk.LEFT, padx=2)
        
        ttk.Button(button_frame, text="Delete Grade",
                  command=lambda: self.delete_grade(tree),
                  style='Action.TButton').pack(side=tk.LEFT, padx=2)
        
        filter_frame = ttk.LabelFrame(self.content_frame, text="Filters", padding="5")
        filter_frame.pack(fill=tk.X, padx=5, pady=(0, 10))
        
        ttk.Label(filter_frame, text="Filter by Class:").pack(side=tk.LEFT, padx=5)
        class_var = tk.StringVar(value='All')
        class_combo = ttk.Combobox(filter_frame, textvariable=class_var, width=20)
        classes = self.db_ops.get_all_classes()
        class_combo['values'] = ['All'] + [c[1] for c in classes]
        class_combo.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(filter_frame, text="Filter by Subject:").pack(side=tk.LEFT, padx=5)
        subject_var = tk.StringVar(value='All')
        subject_combo = ttk.Combobox(filter_frame, textvariable=subject_var, width=20)
        subjects = self.db_ops.get_all_subjects()
        subject_combo['values'] = ['All'] + [s[1] for s in subjects]
        subject_combo.pack(side=tk.LEFT, padx=5)
        
        table_frame = ttk.Frame(self.content_frame)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=5)
        
        columns = ("ID", "Student", "Class", "Subject", "Grade")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        column_widths = {
            "ID": 80,
            "Student": 200,
            "Class": 180,
            "Subject": 180,
            "Grade": 100
        }
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=column_widths.get(col, 150))
            if col in ["Grade", "ID"]:
                tree.column(col, anchor="center")
        
        y_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        x_scroll = ttk.Scrollbar(table_frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
        
        tree.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll.grid(row=1, column=0, sticky="ew")
        
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        def filter_grades(*args):
            print("Filtering grades...")
            for item in tree.get_children():
                tree.delete(item)
            
            try:
                class_filter = class_var.get()
                subject_filter = subject_var.get()
                print(f"Applying filters - Class: {class_filter}, Subject: {subject_filter}")
                
                grades = self.db_ops.get_filtered_grades(class_filter, subject_filter)
                print(f"Retrieved {len(grades)} grades from database")
                
                for grade in grades:
                    try:
                        formatted_values = (
                            grade[0], 
                            grade[1],  
                            grade[2], 
                            grade[3], 
                            f"{float(grade[4]):.1f}" 
                        )
                        tree.insert("", tk.END, values=formatted_values)
                    except Exception as e:
                        print(f"Error formatting grade data: {str(e)}")
                        print(f"Grade data: {grade}")
            except Exception as e:
                print(f"Error in filter_grades: {str(e)}")
                messagebox.showerror("Error", f"Failed to load grades: {str(e)}")
        
        class_combo.bind('<<ComboboxSelected>>', filter_grades)
        subject_combo.bind('<<ComboboxSelected>>', filter_grades)
        
        print("Loading initial grades data...")
        filter_grades()
        
        context_menu = tk.Menu(tree, tearoff=0)
        context_menu.add_command(label="Edit Grade", command=lambda: self.show_edit_grade_dialog(tree))
        context_menu.add_command(label="Delete Grade", command=lambda: self.delete_grade(tree))
        
        def show_context_menu(event):
            item = tree.identify_row(event.y)
            if item:
                tree.selection_set(item)
                context_menu.post(event.x_root, event.y_root)
        
        tree.bind("<Button-3>", show_context_menu)

    def show_add_grade_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Grade")
        dialog.geometry("400x400")
        
        ttk.Label(dialog, text="Select Class:").pack(pady=5)
        class_var = tk.StringVar()
        class_combo = ttk.Combobox(dialog, textvariable=class_var, width=40)
        classes = self.db_ops.get_all_classes()
        class_combo['values'] = [f"{c[0]} - {c[1]}" for c in classes]
        class_combo.pack()
        
        ttk.Label(dialog, text="Select Subject:").pack(pady=5)
        subject_var = tk.StringVar()
        subject_combo = ttk.Combobox(dialog, textvariable=subject_var, width=40)
        subject_combo.pack()
        
        ttk.Label(dialog, text="Select Student:").pack(pady=5)
        student_var = tk.StringVar()
        student_combo = ttk.Combobox(dialog, textvariable=student_var, width=40)
        student_combo.pack()
        
        def update_subjects(*args):
            if class_var.get():
                class_id = int(class_var.get().split(' - ')[0])
                subjects = self.db_ops.get_class_subjects(class_id)
                subject_combo['values'] = [f"{s[0]} - {s[1]}" for s in subjects]
                subject_var.set('')
        
        def update_students(*args):
            if class_var.get():
                class_id = int(class_var.get().split(' - ')[0])
                students = self.db_ops.get_class_enrollments(class_id)
                student_combo['values'] = [f"{s[0]} - {s[1]}" for s in students]
                student_var.set('')
        
        class_combo.bind('<<ComboboxSelected>>', lambda e: [update_subjects(), update_students()])
        
        ttk.Label(dialog, text="Grade (0-100):").pack(pady=5)
        grade_entry = ttk.Entry(dialog, width=40)
        grade_entry.pack()
        
        def save_grade():
            if not all([class_var.get(), subject_var.get(), student_var.get(), grade_entry.get()]):
                messagebox.showerror("Error", "All fields are required")
                return
            
            try:
                grade = float(grade_entry.get())
                if grade < 0 or grade > 100:
                    raise ValueError("Grade must be between 0 and 100")
                
                class_id = int(class_var.get().split(' - ')[0])
                subject_id = int(subject_var.get().split(' - ')[0])
                student_id = int(student_var.get().split(' - ')[0])
                
                if self.db_ops.add_grade(student_id, class_id, subject_id, grade):
                    messagebox.showinfo("Success", "Grade added successfully!")
                    dialog.destroy()
                    self.show_grades()
                else:
                    messagebox.showerror("Error", "Failed to add grade")
            except ValueError as e:
                messagebox.showerror("Error", str(e))
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add grade: {str(e)}")
        
        ttk.Button(dialog, text="Save", command=save_grade, style='Action.TButton').pack(pady=20)

    def show_edit_grade_dialog(self, tree):
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a grade to edit")
            return
        
        grade_id = tree.item(selected_item[0])['values'][0]
        grade_data = self.db_ops.get_grade(grade_id)
        if not grade_data:
            messagebox.showerror("Error", "Grade not found")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Grade")
        dialog.geometry("400x300")
        
        ttk.Label(dialog, text=f"Student: {grade_data[1]}").pack(pady=5)
        ttk.Label(dialog, text=f"Class: {grade_data[2]}").pack(pady=5)
        ttk.Label(dialog, text=f"Subject: {grade_data[3]}").pack(pady=5)
        
        ttk.Label(dialog, text="Grade (0-100):").pack(pady=5)
        grade_entry = ttk.Entry(dialog, width=40)
        grade_entry.insert(0, str(grade_data[4]))
        grade_entry.pack()
        
        def update_grade():
            try:
                grade = float(grade_entry.get())
                if grade < 0 or grade > 100:
                    raise ValueError("Grade must be between 0 and 100")
                
                if self.db_ops.update_grade(grade_id, grade):
                    messagebox.showinfo("Success", "Grade updated successfully!")
                    dialog.destroy()
                    self.show_grades()
                else:
                    messagebox.showerror("Error", "Failed to update grade")
            except ValueError as e:
                messagebox.showerror("Error", str(e))
        
        ttk.Button(dialog, text="Update", command=update_grade, style='Action.TButton').pack(pady=20)

    def delete_grade(self, tree):
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a grade to delete")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this grade?"):
            grade_id = tree.item(selected_item[0])['values'][0]
            if self.db_ops.delete_grade(grade_id):
                messagebox.showinfo("Success", "Grade deleted successfully!")
                self.show_grades()
            else:
                messagebox.showerror("Error", "Failed to delete grade")

    def show_reports(self):
        self.clear_main_content()
        
        header_frame = ttk.Frame(self.content_frame)
        header_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        ttk.Label(header_frame, text="Reports", font=('Helvetica', 16, 'bold')).pack(side=tk.LEFT, padx=5)
        
        notebook = ttk.Notebook(self.content_frame)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        class_performance_frame = ttk.Frame(notebook, padding="10")
        notebook.add(class_performance_frame, text="Class Performance")
        
        filter_frame = ttk.LabelFrame(class_performance_frame, text="Filters", padding="10")
        filter_frame.pack(fill=tk.X, padx=5, pady=(0, 10))
        
        ttk.Label(filter_frame, text="Select Class:").pack(side=tk.LEFT, padx=5)
        class_var = tk.StringVar()
        class_combo = ttk.Combobox(filter_frame, textvariable=class_var, width=30)
        classes = self.db_ops.get_all_classes()
        class_combo['values'] = [c[1] for c in classes]
        class_combo.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(filter_frame, text="Generate Report", 
                  command=lambda: generate_class_report(),
                  style='Action.TButton').pack(side=tk.LEFT, padx=10)
        
        table_frame = ttk.Frame(class_performance_frame)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=5)
        
        columns = ("Subject", "Average Grade", "Highest Grade", "Lowest Grade", "Students Count")
        class_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        class_tree.heading("Subject", text="Subject")
        class_tree.column("Subject", width=200, anchor="w")
        
        class_tree.heading("Average Grade", text="Average Grade")
        class_tree.column("Average Grade", width=150, anchor="center")
        
        class_tree.heading("Highest Grade", text="Highest Grade")
        class_tree.column("Highest Grade", width=150, anchor="center")
        
        class_tree.heading("Lowest Grade", text="Lowest Grade")
        class_tree.column("Lowest Grade", width=150, anchor="center")
        
        class_tree.heading("Students Count", text="Students Count")
        class_tree.column("Students Count", width=150, anchor="center")
        
        y_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=class_tree.yview)
        x_scroll = ttk.Scrollbar(table_frame, orient="horizontal", command=class_tree.xview)
        class_tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
        
        class_tree.pack(fill='both', expand=True, padx=10, pady=10)
        y_scroll.pack(side='right', fill='y')
        x_scroll.pack(side='bottom', fill='x')
        
        def generate_class_report():
            if not class_var.get():
                messagebox.showwarning("Warning", "Please select a class")
                return
            
            for item in class_tree.get_children():
                class_tree.delete(item)
            
            try:
                performance_data = self.db_ops.get_class_performance_report(class_var.get())
                
                if not performance_data:
                    messagebox.showinfo("Info", "No performance data available for this class")
                    return
                
                for row in performance_data:
                    class_tree.insert("", tk.END, values=(
                        row[0],
                        f"{row[1]:.1f}%",
                        f"{row[2]:.1f}%",
                        f"{row[3]:.1f}%",
                        f"{row[4]}"
                    ))
            except Exception as e:
                messagebox.showerror("Error", f"Failed to generate report: {str(e)}")
        
        teacher_load_frame = ttk.Frame(notebook, padding="10")
        notebook.add(teacher_load_frame, text="Teacher Load")
        
        teacher_filter_frame = ttk.LabelFrame(teacher_load_frame, text="Filters", padding="10")
        teacher_filter_frame.pack(fill=tk.X, padx=5, pady=(0, 10))
        
        ttk.Label(teacher_filter_frame, text="Select Teacher:").pack(side=tk.LEFT, padx=5)
        teacher_var = tk.StringVar()
        teacher_combo = ttk.Combobox(teacher_filter_frame, textvariable=teacher_var, width=30)
        teachers = self.db_ops.get_all_teachers()
        teacher_combo['values'] = [t[1] for t in teachers]
        teacher_combo.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(teacher_filter_frame, text="Generate Report",
                  command=lambda: generate_teacher_report(),
                  style='Action.TButton').pack(side=tk.LEFT, padx=10)
        
        teacher_table_frame = ttk.Frame(teacher_load_frame)
        teacher_table_frame.pack(fill=tk.BOTH, expand=True, padx=5)
        
        columns = ("Class", "Students Count", "Subjects", "Total Hours")
        teacher_tree = ttk.Treeview(teacher_table_frame, columns=columns, show='headings', height=15)
        
        teacher_tree.heading("Class", text="Class")
        teacher_tree.column("Class", width=200, anchor="w")
        
        teacher_tree.heading("Students Count", text="Students Count")
        teacher_tree.column("Students Count", width=150, anchor="center")
        
        teacher_tree.heading("Subjects", text="Subjects")
        teacher_tree.column("Subjects", width=250, anchor="w")
        
        teacher_tree.heading("Total Hours", text="Total Hours")
        teacher_tree.column("Total Hours", width=150, anchor="center")
        
        y_scroll = ttk.Scrollbar(teacher_table_frame, orient="vertical", command=teacher_tree.yview)
        x_scroll = ttk.Scrollbar(teacher_table_frame, orient="horizontal", command=teacher_tree.xview)
        teacher_tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
        
        teacher_tree.pack(fill='both', expand=True, padx=10, pady=10)
        y_scroll.pack(side='right', fill='y')
        x_scroll.pack(side='bottom', fill='x')
        
        def generate_teacher_report():
            if not teacher_var.get():
                messagebox.showwarning("Warning", "Please select a teacher")
                return
            
            for item in teacher_tree.get_children():
                teacher_tree.delete(item)
            
            try:
                load_data = self.db_ops.get_teacher_load_report(teacher_var.get())
                
                if not load_data:
                    messagebox.showinfo("Info", "No load data available for this teacher")
                    return
                
                for row in load_data:
                    teacher_tree.insert("", tk.END, values=(
                        row[0],
                        f"{row[1]}",
                        row[2],
                        f"{row[3]} hrs"
                    ))
            except Exception as e:
                messagebox.showerror("Error", f"Failed to generate report: {str(e)}")
        
        student_performance_frame = ttk.Frame(notebook, padding="10")
        notebook.add(student_performance_frame, text="Student Performance")
        
        student_filter_frame = ttk.LabelFrame(student_performance_frame, text="Filters", padding="10")
        student_filter_frame.pack(fill=tk.X, padx=5, pady=(0, 10))
        
        ttk.Label(student_filter_frame, text="Select Student:").pack(side=tk.LEFT, padx=5)
        student_var = tk.StringVar()
        student_combo = ttk.Combobox(student_filter_frame, textvariable=student_var, width=30)
        students = self.db_ops.get_all_students()
        student_combo['values'] = [s[1] for s in students]
        student_combo.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(student_filter_frame, text="Generate Report",
                  command=lambda: generate_student_report(),
                  style='Action.TButton').pack(side=tk.LEFT, padx=10)
        
        student_table_frame = ttk.Frame(student_performance_frame)
        student_table_frame.pack(fill=tk.BOTH, expand=True, padx=5)
        
        columns = ("Subject", "Grade", "Class", "Date")
        student_tree = ttk.Treeview(student_table_frame, columns=columns, show='headings', height=15)
        
        student_tree.heading("Subject", text="Subject")
        student_tree.column("Subject", width=200, anchor="w")
        
        student_tree.heading("Grade", text="Grade")
        student_tree.column("Grade", width=150, anchor="center")
        
        student_tree.heading("Class", text="Class")
        student_tree.column("Class", width=200, anchor="w")
        
        student_tree.heading("Date", text="Date")
        student_tree.column("Date", width=150, anchor="center")
        
        y_scroll = ttk.Scrollbar(student_table_frame, orient="vertical", command=student_tree.yview)
        x_scroll = ttk.Scrollbar(student_table_frame, orient="horizontal", command=student_tree.xview)
        student_tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
        
        student_tree.pack(fill='both', expand=True, padx=10, pady=10)
        y_scroll.pack(side='right', fill='y')
        x_scroll.pack(side='bottom', fill='x')
        
        def generate_student_report():
            if not student_var.get():
                messagebox.showwarning("Warning", "Please select a student")
                return
            
            for item in student_tree.get_children():
                student_tree.delete(item)
            
            try:
                print(f"Generating report for student: {student_var.get()}")
                performance_data = self.db_ops.get_student_grades(student_var.get())
                
                if not performance_data:
                    messagebox.showinfo("Info", "No performance data available for this student")
                    return
                
                print(f"Retrieved {len(performance_data)} grade records")
                
                for row in performance_data:
                    try:
                        grade_value = row[1]
                        if grade_value is not None:
                            try:
                                grade_display = f"{float(grade_value):.1f}%"
                            except (ValueError, TypeError):
                                grade_display = str(grade_value)
                        else:
                            grade_display = "N/A"
                        
                        date_value = row[3]
                        if date_value:
                            try:
                                date_display = date_value.strftime('%Y-%m-%d')
                            except AttributeError:
                                date_display = str(date_value)
                        else:
                            date_display = ""
                            
                        formatted_values = (
                            row[0] or "Unknown", 
                            grade_display,       
                            row[2] or "Unknown",  
                            date_display          
                        )
                        student_tree.insert("", tk.END, values=formatted_values)
                    except Exception as e:
                        print(f"Error processing row {row}: {str(e)}")
                        
                print("Student report generated successfully")
            except Exception as e:
                print(f"Error generating student report: {str(e)}")
                messagebox.showerror("Error", f"Failed to generate report: {str(e)}")

    def run(self):
        self.root.mainloop()
        
    def show_graphs(self):
        self.clear_main_content()
        
        header_frame = ttk.Frame(self.content_frame)
        header_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        ttk.Label(header_frame, text="Data Visualization & Insights", font=('Helvetica', 16, 'bold')).pack(side=tk.LEFT, padx=5)
        
        notebook = ttk.Notebook(self.content_frame)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        class_performance_frame = ttk.Frame(notebook, padding="10")
        notebook.add(class_performance_frame, text="Class Performance")
        
        subject_performance_frame = ttk.Frame(notebook, padding="10")
        notebook.add(subject_performance_frame, text="Subject Performance")
        
        gender_distribution_frame = ttk.Frame(notebook, padding="10")
        notebook.add(gender_distribution_frame, text="Student Demographics")
        
        enrollment_frame = ttk.Frame(notebook, padding="10")
        notebook.add(enrollment_frame, text="Enrollment Distribution")
        
        grade_distribution_frame = ttk.Frame(notebook, padding="10")
        notebook.add(grade_distribution_frame, text="Grade Distribution")
        
        self._create_class_performance_graph(class_performance_frame)
        self._create_subject_performance_graph(subject_performance_frame)
        self._create_gender_distribution_graph(gender_distribution_frame)
        self._create_enrollment_distribution_graph(enrollment_frame)
        self._create_grade_distribution_graph(grade_distribution_frame)
    
    def _create_class_performance_graph(self, parent_frame):
        try:
            data = self.db_ops.get_class_average_grades()
            if not data:
                ttk.Label(parent_frame, text="No class performance data available", font=('Helvetica', 12)).pack(pady=20)
                return
            
            class_names = [row[0] for row in data]
            avg_grades = [float(row[1]) for row in data]
            
            fig, ax = plt.subplots(figsize=(10, 6))
            bars = ax.bar(class_names, avg_grades, color='skyblue')
            
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                        f'{height:.1f}%', ha='center', va='bottom')
            
            ax.set_title('Average Grade by Class', fontsize=14)
            ax.set_xlabel('Class', fontsize=12)
            ax.set_ylabel('Average Grade (%)', fontsize=12)
            ax.set_ylim(0, 100)  
            ax.grid(True, axis='y', linestyle='--', alpha=0.7)
            
            canvas = FigureCanvasTkAgg(fig, master=parent_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            insights_frame = ttk.LabelFrame(parent_frame, text="Insights", padding=10)
            insights_frame.pack(fill=tk.X, padx=5, pady=10)
            
            if not avg_grades:
                insights_text = "No data available for insights."
            else:
                max_class_index = avg_grades.index(max(avg_grades))
                min_class_index = avg_grades.index(min(avg_grades))
                overall_avg = sum(avg_grades) / len(avg_grades) if avg_grades else 0
                
                insights_text = (
                    f"• Best performing class: {class_names[max_class_index]} with {avg_grades[max_class_index]:.1f}%\n"
                    f"• Class needing improvement: {class_names[min_class_index]} with {avg_grades[min_class_index]:.1f}%\n"
                    f"• Overall average across all classes: {overall_avg:.1f}%"
                )
            
            ttk.Label(insights_frame, text=insights_text, wraplength=600, justify=tk.LEFT).pack(padx=5, pady=5)
            
        except Exception as e:
            print(f"Error creating class performance graph: {str(e)}")
            ttk.Label(parent_frame, text=f"Error creating graph: {str(e)}", foreground='red').pack(pady=20)
    
    def _create_subject_performance_graph(self, parent_frame):
        try:
            data = self.db_ops.get_subject_average_grades()
            if not data:
                ttk.Label(parent_frame, text="No subject performance data available", font=('Helvetica', 12)).pack(pady=20)
                return
            
            subject_names = [row[0] for row in data]
            avg_grades = [float(row[1]) for row in data]
            
            fig, ax = plt.subplots(figsize=(10, 6))
            bars = ax.barh(subject_names, avg_grades, color='lightgreen')
            
            for bar in bars:
                width = bar.get_width()
                ax.text(width + 0.5, bar.get_y() + bar.get_height()/2,
                        f'{width:.1f}%', ha='left', va='center')
            
            ax.set_title('Average Grade by Subject', fontsize=14)
            ax.set_xlabel('Average Grade (%)', fontsize=12)
            ax.set_ylabel('Subject', fontsize=12)
            ax.set_xlim(0, 100)  
            ax.grid(True, axis='x', linestyle='--', alpha=0.7)
            
            canvas = FigureCanvasTkAgg(fig, master=parent_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            insights_frame = ttk.LabelFrame(parent_frame, text="Insights", padding=10)
            insights_frame.pack(fill=tk.X, padx=5, pady=10)
            
            if not avg_grades:
                insights_text = "No data available for insights."
            else:
                max_subject_index = avg_grades.index(max(avg_grades))
                min_subject_index = avg_grades.index(min(avg_grades))
                above_avg_subjects = sum(1 for grade in avg_grades if grade > 70)
                below_avg_subjects = sum(1 for grade in avg_grades if grade < 70)
                
                insights_text = (
                    f"• Strongest subject: {subject_names[max_subject_index]} with {avg_grades[max_subject_index]:.1f}%\n"
                    f"• Subject needing focus: {subject_names[min_subject_index]} with {avg_grades[min_subject_index]:.1f}%\n"
                    f"• {above_avg_subjects} subjects are above 70% average\n"
                    f"• {below_avg_subjects} subjects are below 70% average"
                )
            
            ttk.Label(insights_frame, text=insights_text, wraplength=600, justify=tk.LEFT).pack(padx=5, pady=5)
            
        except Exception as e:
            print(f"Error creating subject performance graph: {str(e)}")
            ttk.Label(parent_frame, text=f"Error creating graph: {str(e)}", foreground='red').pack(pady=20)

    def _create_gender_distribution_graph(self, parent_frame):
        try:
            data = self.db_ops.get_gender_distribution()
            if not data:
                ttk.Label(parent_frame, text="No gender distribution data available", font=('Helvetica', 12)).pack(pady=20)
                return
            
            genders = [row[0] for row in data]
            counts = [int(row[1]) for row in data]
            total = sum(counts)
            
            fig, ax = plt.subplots(figsize=(8, 6))
            
            gender_mapping = {'M': 'Male', 'F': 'Female'}
            labels = [gender_mapping.get(g, g) for g in genders]
            
            wedges, texts, autotexts = ax.pie(
                counts, 
                labels=labels,
                autopct='%1.1f%%',
                startangle=90,
                colors=['lightblue', 'pink', 'lightgray'],
                explode=[0.05] * len(genders),
                shadow=True
            )
            
            plt.setp(autotexts, size=10, weight='bold')
            plt.setp(texts, size=12)
            
            ax.set_title('Student Gender Distribution', fontsize=14)
            ax.axis('equal')  
            
            canvas = FigureCanvasTkAgg(fig, master=parent_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            insights_frame = ttk.LabelFrame(parent_frame, text="Demographics Insights", padding=10)
            insights_frame.pack(fill=tk.X, padx=5, pady=10)
            
            if not counts:
                insights_text = "No data available for insights."
            else:
                gender_percentages = [f"{(count/total)*100:.1f}%" for count in counts]
                
                insights_text = "Student Demographics:\n"
                for i, gender in enumerate(genders):
                    gender_name = gender_mapping.get(gender, gender)
                    insights_text += f"• {gender_name}: {counts[i]} students ({gender_percentages[i]})\n"
                
                if len(counts) >= 2 and counts[1] > 0: 
                    ratio = counts[0] / counts[1]
                    insights_text += f"• Gender ratio (M:F): {ratio:.2f}:1"
            
            ttk.Label(insights_frame, text=insights_text, wraplength=600, justify=tk.LEFT).pack(padx=5, pady=5)
            
        except Exception as e:
            print(f"Error creating gender distribution graph: {str(e)}")
            ttk.Label(parent_frame, text=f"Error creating graph: {str(e)}", foreground='red').pack(pady=20)

    def _create_enrollment_distribution_graph(self, parent_frame):
        try:
            data = self.db_ops.get_class_enrollment_counts()
            if not data:
                ttk.Label(parent_frame, text="No enrollment distribution data available", font=('Helvetica', 12)).pack(pady=20)
                return
            
            class_names = [row[0] for row in data]
            enrollment_counts = [row[1] for row in data]
            
            fig, ax = plt.subplots(figsize=(10, 6))
            bars = ax.bar(class_names, enrollment_counts, color='lightcoral')
            
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                        f'{height}', ha='center', va='bottom')
            
            ax.set_title('Student Enrollment Distribution by Class', fontsize=14)
            ax.set_xlabel('Class', fontsize=12)
            ax.set_ylabel('Number of Students', fontsize=12)
            ax.set_ylim(0, max(enrollment_counts) + 5) 
            ax.grid(True, axis='y', linestyle='--', alpha=0.7)
            
            canvas = FigureCanvasTkAgg(fig, master=parent_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            insights_frame = ttk.LabelFrame(parent_frame, text="Insights", padding=10)
            insights_frame.pack(fill=tk.X, padx=5, pady=10)
            
            max_enrollment_class = class_names[enrollment_counts.index(max(enrollment_counts))]
            min_enrollment_class = class_names[enrollment_counts.index(min(enrollment_counts))]
            total_enrollment = sum(enrollment_counts)
            average_enrollment = total_enrollment / len(enrollment_counts) if enrollment_counts else 0
            
            insights_text = (
                f"• Class with highest enrollment: {max_enrollment_class}\n"
                f"• Class with lowest enrollment: {min_enrollment_class}\n"
                f"• Total enrollment across all classes: {total_enrollment}\n"
                f"• Average enrollment per class: {average_enrollment:.1f}"
            )
            
            ttk.Label(insights_frame, text=insights_text, wraplength=600, justify=tk.LEFT).pack(padx=5, pady=5)
            
        except Exception as e:
            print(f"Error creating enrollment distribution graph: {str(e)}")
            ttk.Label(parent_frame, text=f"Error creating graph: {str(e)}", foreground='red').pack(pady=20)

    def _create_grade_distribution_graph(self, parent_frame):
        try:
            print("Creating grade distribution graph...")
            
            graph_frame = ttk.Frame(parent_frame)
            graph_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            grade_distribution = self.db_ops.get_grade_distribution()
            print(f"Grade distribution data received: {grade_distribution}")
            
            if not grade_distribution or len(grade_distribution) == 0:
                ttk.Label(graph_frame, text="No grade data available to display", foreground='red').pack(pady=20)
                return
                
            labels = [str(row[0]) for row in grade_distribution]  
            values = [int(row[1]) for row in grade_distribution]  
            
            print(f"Labels: {labels}")
            print(f"Values: {values}")
            
            colors = ['#4CAF50', '#8BC34A', '#FFC107', '#FF9800', '#F44336']
            
            fig, ax = plt.subplots(figsize=(8, 6))
            fig.patch.set_facecolor('#F0F0F0')
            
            wedges, texts, autotexts = ax.pie(
                values, 
                labels=None, 
                autopct='%1.1f%%',
                startangle=90,
                colors=colors,
                wedgeprops={'edgecolor': 'white', 'linewidth': 1},
                textprops={'fontsize': 12, 'color': 'white'}
            )
            
            ax.axis('equal')
            ax.set_title('Grade Distribution', fontsize=16, pad=20)
            
            ax.legend(
                wedges, 
                labels,
                title="Grade Ranges",
                loc="center left",
                bbox_to_anchor=(1, 0, 0.5, 1)
            )
            
            canvas = FigureCanvasTkAgg(fig, graph_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            insights_frame = ttk.Frame(parent_frame)
            insights_frame.pack(fill=tk.X, padx=10, pady=10)
            
            total_students = sum(values)
            passing_students = sum([values[i] for i in range(len(values)) if 'F' not in labels[i]])
            pass_rate = (passing_students / total_students) * 100 if total_students > 0 else 0
            
            insights_text = f"Total Grades: {total_students}\n"
            insights_text += f"Passing Grades (D or higher): {passing_students} ({pass_rate:.1f}%)\n\n"
            
            insights_text += "Grade Distribution:\n"
            for i, (label, value) in enumerate(zip(labels, values)):
                percentage = (value / total_students) * 100 if total_students > 0 else 0
                insights_text += f"• {label}: {value} students ({percentage:.1f}%)\n"
            
            ttk.Label(insights_frame, text=insights_text, wraplength=600, justify=tk.LEFT).pack(padx=5, pady=5)
            
        except Exception as e:
            print(f"Error creating grade distribution graph: {str(e)}")
            ttk.Label(parent_frame, text=f"Error creating graph: {str(e)}", foreground='red').pack(pady=20)

if __name__ == "__main__":
    app = SchoolManagementGUI()
    app.run()