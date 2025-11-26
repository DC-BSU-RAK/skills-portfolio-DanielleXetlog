import tkinter as tk
from PIL import ImageTk, Image #PIL and ImageTK handles images and displays on tkinter windows

checkbox_vars=[] # This list stores the checkbox variables for student selection
students_data=[] # This list contains the current student data being displayed and modified
original_students=[] # This list holds the original student data loaded from the file
dropdown_visible=False # This variable tracks whether the sort dropdown menu is currently visible
selected_student=None # This variable stores the currently selected student for editing purposes
error_displayed=False # This flag indicates whether an error message is currently being displayed
individual_dropdown_visible=False # This tracks the visibility state of the individual student dropdown
individual_dropdown_canvas=None # This will hold the canvas for the individual dropdown scrolling
individual_dropdown_frame=None # This will hold the frame for the individual dropdown content

def load_original_data():
    global original_students # This global keyword allows us to modify the original_students variable throughout the program
    try:
        with open("studentMarks.txt","r") as file: # This with statement safely opens and reads the student marks file
            lines=file.readlines()
        original_students.clear()
        for line in lines[1:]:
            data=line.strip().split(',')
            original_students.append({
                'id':data[0],'name':data[1],
                'coursework1':int(data[2]),'coursework2':int(data[3]),
                'coursework3':int(data[4]),'exam':int(data[5])
            })
        reset_to_original()
    except FileNotFoundError:
        print("studentMarks.txt file not found!")

def reset_to_original():
    global students_data
    students_data.clear()
    for student in original_students:
        students_data.append(student.copy()) # This copy method creates a duplicate to avoid modifying the original data directly

def toggle_sort_dropdown():
    global dropdown_visible
    if dropdown_visible:
        sort_dropdown.place_forget() # This method hides the dropdown widget from the screen when called
        sort_button.config(text="Sort                  ▼")
        dropdown_visible=False
    else:
        sort_dropdown.lift() # This method brings the dropdown widget to the front over other widgets
        sort_dropdown.place(relx=0.9,rely=0.4,anchor="n")
        sort_button.config(text="Sort                  ▲")
        dropdown_visible=True

def sort_original():
    reset_to_original()
    display_student_data()
    toggle_sort_dropdown()

def sort_ascending():
    global students_data
    students_data.sort(key=lambda x:x['name']) # This sorts the students alphabetically by their name from A to Z
    display_student_data()
    toggle_sort_dropdown()

def sort_descending():
    global students_data
    students_data.sort(key=lambda x:x['name'],reverse=True) # This sorts the students alphabetically by their name from Z to A in reverse order
    display_student_data()
    toggle_sort_dropdown()

def show_all_records():
    main_frame.pack_forget() # This hides all other screens from view
    add_student_frame.pack_forget()
    edit_student_frame.pack_forget()
    individual_frame.pack_forget()
    highest_frame.pack_forget()
    lowest_frame.pack_forget()
    instructions_frame.pack_forget()
    all_records_frame.pack(fill="both",expand=True) # This displays the all records screen and makes it fill the entire window
    display_student_data()
    if dropdown_visible:
        toggle_sort_dropdown()

def show_main():
    all_records_frame.pack_forget() # This method hides all other screens and shows the main menu screen
    add_student_frame.pack_forget()
    edit_student_frame.pack_forget()
    individual_frame.pack_forget()
    highest_frame.pack_forget()
    lowest_frame.pack_forget()
    instructions_frame.pack_forget()
    main_frame.pack(fill="both",expand=True)

def show_instructions():
    all_records_frame.pack_forget() # This method hides all screens and shows the instructions screen
    main_frame.pack_forget()
    add_student_frame.pack_forget()
    edit_student_frame.pack_forget()
    individual_frame.pack_forget()
    highest_frame.pack_forget()
    lowest_frame.pack_forget()
    instructions_frame.pack(fill="both",expand=True)

def show_add_student():
    all_records_frame.pack_forget() # This method hides all screens and displays the add student form
    main_frame.pack_forget()
    edit_student_frame.pack_forget()
    individual_frame.pack_forget()
    highest_frame.pack_forget()
    lowest_frame.pack_forget()
    instructions_frame.pack_forget()
    add_student_frame.pack(fill="both",expand=True)
    add_student_name_entry.delete(0,tk.END) # This method hides all screens and displays the add student form
    add_student_id_entry.delete(0,tk.END)
    add_coursework1_entry.delete(0,tk.END)
    add_coursework2_entry.delete(0,tk.END)
    add_coursework3_entry.delete(0,tk.END)
    add_exam_entry.delete(0,tk.END)

def show_edit_student():
    global selected_student,error_displayed
    selected_index=get_selected_student_index()
    if selected_index is not None:
        selected_student=students_data[selected_index]
        all_records_frame.pack_forget() # This hides all screens and shows the edit student form
        main_frame.pack_forget()
        add_student_frame.pack_forget()
        individual_frame.pack_forget()
        highest_frame.pack_forget()
        lowest_frame.pack_forget()
        instructions_frame.pack_forget()
        edit_student_frame.pack(fill="both",expand=True)
        student_name_label.config(text=selected_student['name'])
        student_id_entry.delete(0,tk.END) # This clears the entry fields and inserts the current student's data
        student_id_entry.insert(0,selected_student['id'])
        coursework1_entry.delete(0,tk.END)
        coursework1_entry.insert(0,selected_student['coursework1'])
        coursework2_entry.delete(0,tk.END)
        coursework2_entry.insert(0,selected_student['coursework2'])
        coursework3_entry.delete(0,tk.END)
        coursework3_entry.insert(0,selected_student['coursework3'])
        exam_entry.delete(0,tk.END)
        exam_entry.insert(0,selected_student['exam'])
        result_label.config(text="")
        error_displayed=False
    else:
        if error_displayed:
            display_student_data()
            result_label.config(text="")
            error_displayed=False
        else:
            for widget in scrollable_frame.winfo_children(): # This clears the scrollable area and displays an error message
                widget.destroy()
            result_label.config(text="Please select a student first")
            error_displayed=True

def toggle_individual_dropdown():
    global individual_dropdown_visible
    if individual_dropdown_visible:
        individual_dropdown.place_forget()
        individual_dropdown_button.config(text="Select Student                ▼")
        individual_dropdown_visible=False
    else:
        update_individual_dropdown()
        individual_dropdown.lift()
        individual_dropdown.place(relx=0.92,rely=0.25,anchor="n")
        individual_dropdown_button.config(text="Select Student                ▲")
        individual_dropdown_visible=True

def select_student(student):
    for widget in individual_display_frame.winfo_children(): # This clears the previous student display from the individual frame
        widget.destroy()
    total_coursework=student['coursework1']+student['coursework2']+student['coursework3']
    total_marks=total_coursework+student['exam']
    overall_percentage=(total_marks/160)*100
    grade=calculate_grade(overall_percentage)
    student_info=f"{student['name']:<18}    {student['id']:<12}    {total_coursework:<15}    {student['exam']:<15}   {overall_percentage:.1f}%{'':<8}           {grade}" # This formats the student information with fixed spacing for alignment
    student_label=tk.Label(individual_display_frame,text=student_info,font=("Courier New",11),bg="#121b30",fg="#f1f5f9",anchor="w") # This creates a label with the formatted text, aligned to the left
    student_label.pack(pady=2)
    individual_result_label.config(text="")
    toggle_individual_dropdown()

def update_individual_dropdown():
    for widget in individual_dropdown.winfo_children(): # This removes all the old dropdown items before adding new ones
        widget.destroy()
    for student in students_data: # This creates a button for each student in the dropdown
        btn=tk.Button(individual_dropdown,text=student['name'],font=("Arial",10),relief="flat",borderwidth=0,bg="#f1f5f9",fg="#121b30",activebackground="#e2e8f0",activeforeground="#121b30",command=lambda s=student: select_student(s),anchor="w",width=15) # This packs the button to fill the available width with some padding
        btn.pack(fill="x",padx=1,pady=1)

def show_individual_record():
    all_records_frame.pack_forget()
    main_frame.pack_forget()
    add_student_frame.pack_forget()
    edit_student_frame.pack_forget()
    highest_frame.pack_forget()
    lowest_frame.pack_forget()
    instructions_frame.pack_forget()
    individual_frame.pack(fill="both",expand=True)
    for widget in individual_display_frame.winfo_children(): # This clears the individual student display area
        widget.destroy()
    individual_result_label.config(text="")
    if individual_dropdown_visible:
        toggle_individual_dropdown()

def show_highest_mark():
    all_records_frame.pack_forget()
    main_frame.pack_forget()
    add_student_frame.pack_forget()
    edit_student_frame.pack_forget()
    individual_frame.pack_forget()
    lowest_frame.pack_forget()
    instructions_frame.pack_forget()
    highest_frame.pack(fill="both",expand=True)
    display_highest_student()

def show_lowest_mark():
    all_records_frame.pack_forget()
    main_frame.pack_forget()
    add_student_frame.pack_forget()
    edit_student_frame.pack_forget()
    individual_frame.pack_forget()
    highest_frame.pack_forget()
    instructions_frame.pack_forget()
    lowest_frame.pack(fill="both",expand=True)
    display_lowest_student()

def display_highest_student():
    for widget in highest_display_frame.winfo_children(): # This clears the highest student display area before showing new data
        widget.destroy()
    
    highest_student=None
    highest_percentage=0
    
    for student in students_data: # This loop finds the student with the highest overall percentage
        total_coursework=student['coursework1']+student['coursework2']+student['coursework3']
        total_marks=total_coursework+student['exam']
        overall_percentage=(total_marks/160)*100
        
        if overall_percentage>highest_percentage:
            highest_percentage=overall_percentage
            highest_student=student
    
    if highest_student:
        total_coursework=highest_student['coursework1']+highest_student['coursework2']+highest_student['coursework3']
        total_marks=total_coursework+highest_student['exam']
        grade=calculate_grade(highest_percentage)
        
        ranking_label.config(text="#1")
        student_name_big.config(text=highest_student['name'])
        percentage_label.config(text=f"Overall Percentage: {highest_percentage:.2f}%")
        
        student_info=f"{highest_student['name']:<18}      {highest_student['id']:<12}    {total_coursework:<15}  {highest_student['exam']:<15}   {highest_percentage:.1f}%{'':<8}           {grade}"
        student_label=tk.Label(highest_display_frame,text=student_info,font=("Courier New",11),bg="#121b30",fg="#f1f5f9",anchor="w")
        student_label.pack(pady=2)

def display_lowest_student():
    for widget in lowest_display_frame.winfo_children(): # This clears the lowest student display area before showing new data
        widget.destroy()
    
    lowest_student=None
    lowest_percentage=100
    
    for student in students_data: # This loop finds the student with the lowest overall percentage
        total_coursework=student['coursework1']+student['coursework2']+student['coursework3']
        total_marks=total_coursework+student['exam']
        overall_percentage=(total_marks/160)*100
        
        if overall_percentage<lowest_percentage:
            lowest_percentage=overall_percentage
            lowest_student=student
    
    if lowest_student:
        total_coursework=lowest_student['coursework1']+lowest_student['coursework2']+lowest_student['coursework3']
        total_marks=total_coursework+lowest_student['exam']
        grade=calculate_grade(lowest_percentage)
        
        lowest_ranking_label.config(text=f"#{len(students_data)}") # This sets the ranking to the last position in the student list
        lowest_student_name_big.config(text=lowest_student['name'])
        lowest_percentage_label.config(text=f"Overall Percentage: {lowest_percentage:.2f}%")
        
        student_info=f"{lowest_student['name']:<18}      {lowest_student['id']:<12}    {total_coursework:<15}  {lowest_student['exam']:<15}   {lowest_percentage:.1f}%{'':<8}           {grade}"
        student_label=tk.Label(lowest_display_frame,text=student_info,font=("Courier New",11),bg="#121b30",fg="#f1f5f9",anchor="w")
        student_label.pack(pady=2)

def update_student():
    global selected_student
    if selected_student:
        selected_student['id']=student_id_entry.get() # This updates the student data with the values from the form fields
        selected_student['coursework1']=int(coursework1_entry.get())
        selected_student['coursework2']=int(coursework2_entry.get())
        selected_student['coursework3']=int(coursework3_entry.get())
        selected_student['exam']=int(exam_entry.get())
        show_all_records()

def add_new_student():
    new_student={
        'name':add_student_name_entry.get(),
        'id':add_student_id_entry.get(),
        'coursework1':int(add_coursework1_entry.get()),
        'coursework2':int(add_coursework2_entry.get()),
        'coursework3':int(add_coursework3_entry.get()),
        'exam':int(add_exam_entry.get())
    }
    students_data.append(new_student)
    show_all_records()

def delete_student():
    selected_index=get_selected_student_index()
    if selected_index is not None:
        students_data.pop(selected_index) # This removes the selected student from the students_data list
        display_student_data()
        result_label.config(text="")
    else:
        if result_label.cget("text") == "Please select a student first":
            display_student_data()
            result_label.config(text="")
        else:
            for widget in scrollable_frame.winfo_children():
                widget.destroy()
            result_label.config(text="Please select a student first")

def clear_entry(event):
    event.widget.delete(0,tk.END) # This function clears an entry field when it is clicked by the user
    event.widget.config(fg="#172959")

def get_selected_student_index():
    for i,var in enumerate(checkbox_vars):
        if var.get():
            return i
    return None

def search_student():
    search_text=search_entry.get().strip()
    if search_text=="":
        display_student_data()
        result_label.config(text="")
    else:
        display_search_results(search_text)

def calculate_grade(percentage):
    if percentage>=70:return'A'
    elif percentage>=60:return'B'
    elif percentage>=50:return'C'
    elif percentage>=40:return'D'
    else:return'F'

def display_search_results(search_text):
    global checkbox_vars
    for widget in scrollable_frame.winfo_children(): # This clears the previous search results from the display
        widget.destroy()
    checkbox_vars.clear()
    display_students=[]
    for student in students_data:
        total_coursework=student['coursework1']+student['coursework2']+student['coursework3']
        total_marks=total_coursework+student['exam']
        overall_percentage=(total_marks/160)*100
        grade=calculate_grade(overall_percentage)
        display_students.append({
            'name':student['name'],'id':student['id'],
            'coursework':total_coursework,'exam':student['exam'],
            'percentage':overall_percentage,'grade':grade
        })
    found_students=[s for s in display_students if search_text.lower() in s['name'].lower() or search_text.lower() in s['id'].lower()] # This finds students whose name or ID matches the search text
    if found_students:
        for i,student in enumerate(found_students):
            checkbox_var=tk.BooleanVar()
            checkbox_vars.append(checkbox_var)
            checkbox=tk.Checkbutton(scrollable_frame,variable=checkbox_var,bg="#121b30",activebackground="#121b30")
            checkbox.grid(row=i,column=0,sticky="w",padx=10,pady=2)
            # FIXED: Removed extra spacing that was pushing exam marks and overall grades out of view
            student_info=f"{student['name']:<18}        {student['id']:<12}     {student['coursework']:<15}   {student['exam']:<15}{student['percentage']:.1f}%{'':<8}        {student['grade']}"
            student_label=tk.Label(scrollable_frame,text=student_info,font=("Courier New",11),bg="#121b30",fg="#f1f5f9",anchor="w")
            student_label.grid(row=i,column=1,sticky="w",padx=10,pady=2)
        result_label.config(text="")
    else:
        result_label.config(text="Student not found")
    scrollable_frame.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all")) # This updates the scrollable area to fit the new content

def display_student_data():
    global checkbox_vars
    for widget in scrollable_frame.winfo_children(): # This clears the student list display before showing updated data
        widget.destroy()
    checkbox_vars.clear()
    specific_order=["John Curry","Sam Sturtivant","Lee Scott","Matt Thompson","Ron Herrema","Jake Hobbs","Jo Hyde","Gareth Southgate","Alan Shearer","Les Ferdinand"]
    display_students=[]
    for student in students_data:
        total_coursework=student['coursework1']+student['coursework2']+student['coursework3']
        total_marks=total_coursework+student['exam']
        overall_percentage=(total_marks/160)*100
        grade=calculate_grade(overall_percentage)
        display_students.append({
            'name':student['name'],'id':student['id'],
            'coursework':total_coursework,'exam':student['exam'],
            'percentage':overall_percentage,'grade':grade
        })
    is_original_order=(len(students_data)==len(original_students) and all(students_data[i]['name']==original_students[i]['name'] for i in range(len(students_data)))) # This checks if the data is still in the original order from the file
    if is_original_order:
        ordered_students=[]
        for name in specific_order:
            for student in display_students:
                if student['name']==name:
                    ordered_students.append(student)
                    break
    else:
        ordered_students=display_students
    total_percentage=0
    for i,student in enumerate(ordered_students):
        checkbox_var=tk.BooleanVar() # This creates a checkbox for each student in the list
        checkbox_vars.append(checkbox_var)
        checkbox=tk.Checkbutton(scrollable_frame,variable=checkbox_var,bg="#121b30",activebackground="#121b30")
        checkbox.grid(row=i,column=0,sticky="w",padx=10,pady=2)
        student_info=f"{student['name']:<18}         {student['id']:<12}     {student['coursework']:<15}  {student['exam']:<15}{student['percentage']:.1f}%{'':<8}        {student['grade']}"
        student_label=tk.Label(scrollable_frame,text=student_info,font=("Courier New",11),bg="#121b30",fg="#f1f5f9",anchor="w")
        student_label.grid(row=i,column=1,sticky="w",padx=10,pady=2)
        total_percentage+=student['percentage']
    if ordered_students:
        average_percentage=total_percentage/len(ordered_students)
        summary_text=f"Total Students: {len(ordered_students)} | Average Percentage: {average_percentage:.1f}%"
        summary_label=tk.Label(all_records_frame,text=summary_text,font=("Arial",14,"bold"),bg="#121b30",fg="#f1f5f9")
        summary_label.place(relx=0.6,rely=0.96,anchor="center")
    scrollable_frame.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all")) # This updates the scrollable area to fit all the student entries

def on_mousewheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)),"units") # This function enables scrolling with the mouse wheel

def quit_program():
    with open("studentMarks.txt","w") as file: # This function saves the current data back to the file before closing
        file.write("ID,Name,Coursework1,Coursework2,Coursework3,Exam\n")
        file.write("1345,John Curry,8,15,7,45\n")
        file.write("2345,Sam Sturtivant,14,15,14,77\n")
        file.write("9876,Lee Scott,17,11,16,99\n")
        file.write("3724,Matt Thompson,19,11,15,81\n")
        file.write("1212,Ron Herrema,14,17,18,66\n")
        file.write("8439,Jake Hobbs,10,11,10,43\n")
        file.write("2344,Jo Hyde,6,15,10,55\n")
        file.write("9384,Gareth Southgate,5,6,8,33\n")
        file.write("8327,Alan Shearer,20,20,20,100\n")
        file.write("2983,Les Ferdinand,15,17,18,92\n")
    root.destroy()

load_original_data() # This loads the original student data when the program starts
root=tk.Tk() # This creates the main application window
root.title("Exercise 3 - Student Manager")
root.geometry("1920x1080")
root.iconbitmap("Logo 3.ico")

main_frame=tk.Frame(root) # This creates separate frames for each screen in the application
all_records_frame=tk.Frame(root)
add_student_frame=tk.Frame(root)
edit_student_frame=tk.Frame(root)
individual_frame=tk.Frame(root)
highest_frame=tk.Frame(root)
lowest_frame=tk.Frame(root)
instructions_frame=tk.Frame(root) # This creates a new frame for the instructions screen

# This sets up the main menu screen with background and title
main_frame.pack(fill="both",expand=True)
bg_image=ImageTk.PhotoImage(Image.open("Student Management.png"))
bg_label=tk.Label(main_frame,image=bg_image)
bg_label.place(x=0,y=0,relwidth=1,relheight=1)
tk.Label(main_frame,text="STUDENT MANAGER",font=("Arial",45,"bold"),bg="#0f172a",fg="#f1f5f9").place(relx=0.76,rely=0.3,anchor="center")
tk.Label(main_frame,text="Click the options on the right side navigation bar to begin",font=("Arial",12,"bold"),bg="#0f172a",fg="#6c86a0").place(relx=0.71,rely=0.35,anchor="center")

# This sets up the instructions screen with background and text
instructions_image=ImageTk.PhotoImage(Image.open("Instructions2.png"))
instructions_bg=tk.Label(instructions_frame,image=instructions_image)
instructions_bg.place(x=0,y=0,relwidth=1,relheight=1)
tk.Label(instructions_frame,text="INSTRUCTIONS",font=("Arial",45,"bold"),bg="#121b30",fg="#f1f5f9").place(relx=0.62,rely=0.27,anchor="center")
tk.Label(instructions_frame,text="Hello and welcome to my Student Manager! In this application you will be managing and analysing student mark data \n from your class. You will also be seeing features in the application such as:",font=("Arial",12,"bold"),bg="#121b30",fg="#f1f5f9").place(relx=0.62,rely=0.35,anchor="center")
instructions_text=tk.Label(instructions_frame,text="""》 The sentences who have (+) are the additional features that I added myself.\n\n➧ FEATURES\n- Search button: Where the user can search a student's name to make it easier to find the students data.\n- (+) Checkbox button: Where the user can select a student so the user will know who they selected.\n- Delete button: Where the user can select a student using the checkbox button and easily deleting their name using the Delete button just in case if the user put in a \n student that doesn't belong to your class.\n- Edit button: To edit a students data such as their ID#, total marks, exam marks, overall and the student grade. (+) I also added a feature where you can see their \n previous/old data. After editing the students information you can press the Update button to update the students data and will automatically update it from all records.\n- Sort button: This button sorts the students names from A-Z (Ascending) if you click the Ascending button and Z-A if you click the Descending button. This helps you \n organize the students. (+) I also added a button called \"Original\" which will organize it to its original order.\n- Add student button: Where you can add new student and fill their data such as the students name, students ID#, coursework mark 1, coursework mark 2, coursework \n mark 3 and exam mark. After filling it all in you can just press the save button to save the data and updates it to all records.\n\n(+) I also added a feature on the \"Quit\" button so when clicking this button it exist the whole application like a normal quit button but when clicking it not only exits the \n quit button it also reset the whole students record which will only show the student name that were original to the .txt file which was given.\n\n\n Good luck and have fun managing the student manager!""",font=("Arial",10),bg="#121b30",fg="#f1f5f9",justify="left",anchor="w")
instructions_text.place(relx=0.6,rely=0.6,anchor="center",relwidth=0.65,relheight=0.4)

# This sets up the all records screen with its background and labels
all_records_image=ImageTk.PhotoImage(Image.open("All Records.png"))
all_records_bg=tk.Label(all_records_frame,image=all_records_image)
all_records_bg.place(x=0,y=0,relwidth=1,relheight=1)
tk.Label(all_records_frame,text="Student List",font=("Arial",24,"bold"),bg="#0f172a",fg="#f1f5f9").place(relx=0.31,rely=0.2,anchor="center")
tk.Label(all_records_frame,text="Student Records",font=("Arial",12,"bold"),bg="#0f172a",fg="#434a5a").place(relx=0.29,rely=0.24,anchor="center")
tk.Label(all_records_frame,text="Student Information",font=("Arial",24,"bold"),bg="#121b30",fg="#f1f5f9").place(relx=0.36,rely=0.37,anchor="center")

table_header=tk.Label(all_records_frame,text="STUDENTS NAMES          ID#       TOTAL MARKS     EXAM MARKS       OVERALL           GRADE",font=("Courier New",12),bg="#142142",fg="#f1f5f9",anchor="w")
table_header.place(relx=0.3,rely=0.46,relwidth=0.6,anchor="w")

# This creates a scrollable canvas area for the student list
canvas=tk.Canvas(all_records_frame,bg="#121b30",highlightthickness=0)
# This positions the canvas in the top-left corner of its container
canvas.place(relx=0.26,rely=0.52,relwidth=0.65,relheight=0.4,anchor="nw")
scrollbar=tk.Scrollbar(all_records_frame,orient="vertical",command=canvas.yview)
scrollbar.place(relx=0.94,rely=0.51,relheight=0.42,anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)
scrollable_frame=tk.Frame(canvas,bg="#121b30")
canvas.create_window((0,0),window=scrollable_frame,anchor="nw")
canvas.bind("<Configure>",lambda e:canvas.configure(scrollregion=canvas.bbox("all")))
# This binds the mouse wheel event to the scroll function
canvas.bind_all("<MouseWheel>",on_mousewheel)

sort_button=tk.Button(all_records_frame,text="Sort                  ▼",font=("Arial",12),relief="flat",borderwidth=0,bg="#1e3a8a",fg="#f1f5f9",activebackground="#1e3a8a",activeforeground="#f1f5f9",command=toggle_sort_dropdown)
sort_button.place(relx=0.9,rely=0.37,anchor="center")

sort_dropdown=tk.Frame(all_records_frame,bg="#f1f5f9",relief="solid",borderwidth=1,width=120)
original_btn=tk.Button(sort_dropdown,text="Original",font=("Arial",10),relief="flat",borderwidth=0,bg="#f1f5f9",fg="#121b30",activebackground="#e2e8f0",activeforeground="#121b30",command=sort_original,anchor="w",width=15)
original_btn.pack(fill="x",padx=1,pady=1)
ascending_btn=tk.Button(sort_dropdown,text="Ascending",font=("Arial",10),relief="flat",borderwidth=0,bg="#f1f5f9",fg="#121b30",activebackground="#e2e8f0",activeforeground="#121b30",command=sort_ascending,anchor="w",width=15)
ascending_btn.pack(fill="x",padx=1,pady=1)
descending_btn=tk.Button(sort_dropdown,text="Descending",font=("Arial",10),relief="flat",borderwidth=0,bg="#f1f5f9",fg="#121b30",activebackground="#e2e8f0",activeforeground="#121b30",command=sort_descending,anchor="w",width=15)
descending_btn.pack(fill="x",padx=1,pady=1)
sort_dropdown.place_forget() # This hides the dropdown menu initially when the program starts

search_entry=tk.Entry(all_records_frame,font=("Arial",14),relief="flat",borderwidth=0,bg="#f1f5f9",fg="#121b30",width=16,justify="left")
search_entry.place(relx=0.62,rely=0.37,anchor="center")
search_button=tk.Button(all_records_frame,text="⌕",font=("Arial",16,"bold"),relief="flat",borderwidth=0,bg="#f1f5f9",fg="#121b30",command=search_student)
search_button.place(relx=0.55,rely=0.37,anchor="center")
result_label=tk.Label(all_records_frame,text="",font=("Arial",14),bg="#121b30",fg="#f1f5f9")
result_label.place(relx=0.6,rely=0.7,anchor="center")

edit_button=tk.Button(all_records_frame,text="Edit",font=("Arial",12),relief="flat",borderwidth=0,bg="#1e3a8a",fg="#f1f5f9",activebackground="#1e3a8a",activeforeground="#f1f5f9",command=show_edit_student)
edit_button.place(relx=0.79,rely=0.37,anchor="center")

delete_button=tk.Button(all_records_frame,text="Del",font=("Arial",12),relief="flat",borderwidth=0,bg="#1e3a8a",fg="#f1f5f9",activebackground="#1e3a8a",activeforeground="#f1f5f9",command=delete_student)
delete_button.place(relx=0.71,rely=0.37,anchor="center")

add_student_button=tk.Button(all_records_frame,text="+ Add Students",font=("Arial",14),relief="flat",borderwidth=0,bg="#3b82f6",fg="#f1f5f9",activebackground="#3b82f6",activeforeground="#f1f5f9",command=show_add_student)
add_student_button.place(relx=0.9,rely=0.22,anchor="center")

# This sets up the add student screen with background and form fields
add_student_image=ImageTk.PhotoImage(Image.open("Add Student.png"))
tk.Label(add_student_frame,image=add_student_image).place(x=0,y=0,relwidth=1,relheight=1)
tk.Label(add_student_frame,text="Add Student Record",font=("Arial",24,"bold"),bg="#0f172a",fg="#f1f5f9",anchor="w").place(relx=0.34,rely=0.2,anchor="center")
tk.Label(add_student_frame,text="Fill in the student's details below and click the save button",font=("Arial",14),bg="#0f172a",fg="#6c86a0",anchor="w").place(relx=0.4,rely=0.25,anchor="center")
tk.Label(add_student_frame,text="STUDENTS NAME",font=("Arial",20),bg="#172959",fg="#f1f5f9",anchor="w").place(relx=0.35,rely=0.37,anchor="center")
tk.Label(add_student_frame,text="STUDENT ID #",font=("Arial",20),bg="#172959",fg="#f1f5f9",anchor="w").place(relx=0.34,rely=0.47,anchor="center")
tk.Label(add_student_frame,text="COURSEWORK MARK 1",font=("Arial",20),bg="#172959",fg="#f1f5f9",anchor="w").place(relx=0.38,rely=0.56,anchor="center")
tk.Label(add_student_frame,text="COURSEWORK MARK 2",font=("Arial",20),bg="#172959",fg="#f1f5f9",anchor="w").place(relx=0.38,rely=0.64,anchor="center")
tk.Label(add_student_frame,text="COURSEWORK MARK 3",font=("Arial",20),bg="#172959",fg="#f1f5f9",anchor="w").place(relx=0.38,rely=0.74,anchor="center")
tk.Label(add_student_frame,text="EXAM MARK",font=("Arial",20),bg="#172959",fg="#f1f5f9",anchor="w").place(relx=0.33,rely=0.83,anchor="center")
add_student_name_entry=tk.Entry(add_student_frame,font=("Arial",20),relief="flat",borderwidth=0,bg="#f1f5f9",fg="#ced4df",width=15,justify="left")
add_student_name_entry.place(relx=0.62,rely=0.37,anchor="center")
# This binds a click event to clear the entry field when clicked
add_student_name_entry.bind("<Button-1>",clear_entry)
add_student_id_entry=tk.Entry(add_student_frame,font=("Arial",20),relief="flat",borderwidth=0,bg="#f1f5f9",fg="#ced4df",width=15,justify="left")
add_student_id_entry.place(relx=0.62,rely=0.46,anchor="center")
add_student_id_entry.bind("<Button-1>",clear_entry)
add_coursework1_entry=tk.Entry(add_student_frame,font=("Arial",20),relief="flat",borderwidth=0,bg="#f1f5f9",fg="#ced4df",width=15,justify="left")
add_coursework1_entry.place(relx=0.62,rely=0.55,anchor="center")
add_coursework1_entry.bind("<Button-1>",clear_entry)
add_coursework2_entry=tk.Entry(add_student_frame,font=("Arial",20),relief="flat",borderwidth=0,bg="#f1f5f9",fg="#ced4df",width=15,justify="left")
add_coursework2_entry.place(relx=0.62,rely=0.64,anchor="center")
add_coursework2_entry.bind("<Button-1>",clear_entry)
add_coursework3_entry=tk.Entry(add_student_frame,font=("Arial",20),relief="flat",borderwidth=0,bg="#f1f5f9",fg="#ced4df",width=15,justify="left")
add_coursework3_entry.place(relx=0.62,rely=0.73,anchor="center")
add_coursework3_entry.bind("<Button-1>",clear_entry)
add_exam_entry=tk.Entry(add_student_frame,font=("Arial",20),relief="flat",borderwidth=0,bg="#f1f5f9",fg="#ced4df",width=15,justify="left")
add_exam_entry.place(relx=0.62,rely=0.82,anchor="center")
add_exam_entry.bind("<Button-1>",clear_entry)
save_button=tk.Button(add_student_frame,text="SAVE",font=("Arial",16),relief="flat",borderwidth=0,bg="#3b82f6",fg="#f1f5f9",activebackground="#3b82f6",activeforeground="#f1f5f9",command=add_new_student)
save_button.place(relx=0.63,rely=0.93,anchor="center")

# This sets up the edit student screen with background and form fields
edit_student_image=ImageTk.PhotoImage(Image.open("Update.png"))
tk.Label(edit_student_frame,image=edit_student_image).place(x=0,y=0,relwidth=1,relheight=1)
tk.Label(edit_student_frame,text="Update Student Record",font=("Arial",24,"bold"),bg="#0f172a",fg="#f1f5f9",anchor="w").place(relx=0.35,rely=0.2,anchor="center")
tk.Label(edit_student_frame,text="Select a student to update their record",font=("Arial",14),bg="#0f172a",fg="#6c86a0",anchor="w").place(relx=0.34,rely=0.25,anchor="center")
tk.Label(edit_student_frame,text="STUDENTS NAME",font=("Arial",20),bg="#172959",fg="#f1f5f9",anchor="w").place(relx=0.35,rely=0.37,anchor="center")
tk.Label(edit_student_frame,text="STUDENT ID #",font=("Arial",20),bg="#172959",fg="#f1f5f9",anchor="w").place(relx=0.34,rely=0.47,anchor="center")
tk.Label(edit_student_frame,text="COURSEWORK MARK 1",font=("Arial",20),bg="#172959",fg="#f1f5f9",anchor="w").place(relx=0.38,rely=0.56,anchor="center")
tk.Label(edit_student_frame,text="COURSEWORK MARK 2",font=("Arial",20),bg="#172959",fg="#f1f5f9",anchor="w").place(relx=0.38,rely=0.64,anchor="center")
tk.Label(edit_student_frame,text="COURSEWORK MARK 3",font=("Arial",20),bg="#172959",fg="#f1f5f9",anchor="w").place(relx=0.38,rely=0.74,anchor="center")
tk.Label(edit_student_frame,text="EXAM MARK",font=("Arial",20),bg="#172959",fg="#f1f5f9",anchor="w").place(relx=0.33,rely=0.83,anchor="center")
student_name_label=tk.Label(edit_student_frame,text="",font=("Arial",20),bg="#f1f5f9",fg="#172959",anchor="w")
student_name_label.place(relx=0.61,rely=0.37,anchor="center")
student_id_entry=tk.Entry(edit_student_frame,font=("Arial",20),relief="flat",borderwidth=0,bg="#f1f5f9",fg="#ced4df",width=15,justify="left")
student_id_entry.place(relx=0.62,rely=0.46,anchor="center")
student_id_entry.bind("<Button-1>",clear_entry)
coursework1_entry=tk.Entry(edit_student_frame,font=("Arial",20),relief="flat",borderwidth=0,bg="#f1f5f9",fg="#ced4df",width=15,justify="left")
coursework1_entry.place(relx=0.62,rely=0.55,anchor="center")
coursework1_entry.bind("<Button-1>",clear_entry)
coursework2_entry=tk.Entry(edit_student_frame,font=("Arial",20),relief="flat",borderwidth=0,bg="#f1f5f9",fg="#ced4df",width=15,justify="left")
coursework2_entry.place(relx=0.62,rely=0.64,anchor="center")
coursework2_entry.bind("<Button-1>",clear_entry)
coursework3_entry=tk.Entry(edit_student_frame,font=("Arial",20),relief="flat",borderwidth=0,bg="#f1f5f9",fg="#ced4df",width=15,justify="left")
coursework3_entry.place(relx=0.62,rely=0.73,anchor="center")
coursework3_entry.bind("<Button-1>",clear_entry)
exam_entry=tk.Entry(edit_student_frame,font=("Arial",20),relief="flat",borderwidth=0,bg="#f1f5f9",fg="#ced4df",width=15,justify="left")
exam_entry.place(relx=0.62,rely=0.82,anchor="center")
exam_entry.bind("<Button-1>",clear_entry)
update_button=tk.Button(edit_student_frame,text="UPDATE",font=("Arial",16),relief="flat",borderwidth=0,bg="#3b82f6",fg="#f1f5f9",activebackground="#3b82f6",activeforeground="#f1f5f9",command=update_student)
update_button.place(relx=0.63,rely=0.93,anchor="center")

# This sets up the individual record screen with background and dropdown
individual_image=ImageTk.PhotoImage(Image.open("Individual Record.png"))
tk.Label(individual_frame,image=individual_image).place(x=0,y=0,relwidth=1,relheight=1)
tk.Label(individual_frame,text="Individual Student Record",font=("Arial",24,"bold"),bg="#0f172a",fg="#f1f5f9",anchor="w").place(relx=0.36,rely=0.2,anchor="center")
tk.Label(individual_frame,text="Select a student to view their individual record.",font=("Arial",14),bg="#0f172a",fg="#6c86a0",anchor="w").place(relx=0.36,rely=0.25,anchor="center")
individual_dropdown_button=tk.Button(individual_frame,text="Select Student                ▼",font=("Arial",14),relief="flat",borderwidth=0,bg="#3b82f6",fg="#f1f5f9",activebackground="#3b82f6",activeforeground="#f1f5f9",command=toggle_individual_dropdown)
individual_dropdown_button.place(relx=0.89,rely=0.22,anchor="center")
individual_dropdown=tk.Frame(individual_frame,bg="#f1f5f9",relief="solid",borderwidth=1,width=120)
individual_dropdown.place_forget()
individual_table_header=tk.Label(individual_frame,text="STUDENTS NAMES       ID#       TOTAL MARKS     EXAM MARKS         OVERALL              GRADE",font=("Courier New",12),bg="#172959",fg="#f1f5f9",anchor="w")
individual_table_header.place(relx=0.29,rely=0.37,relwidth=0.6,anchor="w")
individual_display_frame=tk.Frame(individual_frame,bg="#121b30")
individual_display_frame.place(relx=0.26,rely=0.52,relwidth=0.65,relheight=0.4,anchor="nw")
individual_result_label=tk.Label(individual_frame,text="",font=("Arial",14),bg="#121b30",fg="#f1f5f9",anchor="w")
individual_result_label.place(relx=0.6,rely=0.44,anchor="center")

# This sets up the highest mark screen with background and display areas
highest_image=ImageTk.PhotoImage(Image.open("Highest Mark.png"))
tk.Label(highest_frame,image=highest_image).place(x=0,y=0,relwidth=1,relheight=1)
tk.Label(highest_frame,text="Highest Overall Mark",font=("Arial",24,"bold"),bg="#0f172a",fg="#f1f5f9",anchor="w").place(relx=0.35,rely=0.2,anchor="center")
tk.Label(highest_frame,text="Student with the highest overall mark",font=("Arial",14),bg="#0f172a",fg="#6c86a0",anchor="w").place(relx=0.35,rely=0.25,anchor="center")
ranking_label=tk.Label(highest_frame,text="#1",font=("Arial",20,"bold"),bg="#3b82f6",fg="#f1f5f9",anchor="w")
ranking_label.place(relx=0.89,rely=0.47,anchor="center")
student_name_big=tk.Label(highest_frame,text="",font=("Arial",50,"bold"),bg="#172959",fg="#f1f5f9",anchor="w")
student_name_big.place(relx=0.4,rely=0.42,anchor="center")
percentage_label=tk.Label(highest_frame,text="",font=("Arial",20),bg="#172959",fg="#f1f5f9",anchor="w")
percentage_label.place(relx=0.38,rely=0.48,anchor="center")
highest_table_header=tk.Label(highest_frame,text="STUDENTS NAMES       ID#       TOTAL MARKS     EXAM MARKS         OVERALL              GRADE",font=("Courier New",12),bg="#172959",fg="#f1f5f9",anchor="w")
highest_table_header.place(relx=0.29,rely=0.65,relwidth=0.6,anchor="w")
highest_display_frame=tk.Frame(highest_frame,bg="#121b30")
highest_display_frame.place(relx=0.26,rely=0.75,relwidth=0.65,relheight=0.4,anchor="nw")

# This sets up the lowest mark screen with background and display areas
lowest_image=ImageTk.PhotoImage(Image.open("Lowest Mark.png"))
tk.Label(lowest_frame,image=lowest_image).place(x=0,y=0,relwidth=1,relheight=1)
tk.Label(lowest_frame,text="Lowest Overall Mark",font=("Arial",24,"bold"),bg="#0f172a",fg="#f1f5f9",anchor="w").place(relx=0.35,rely=0.2,anchor="center")
tk.Label(lowest_frame,text="Student with the lowest overall mark",font=("Arial",14),bg="#0f172a",fg="#6c86a0",anchor="w").place(relx=0.35,rely=0.25,anchor="center")
lowest_ranking_label=tk.Label(lowest_frame,text="#10",font=("Arial",20,"bold"),bg="#3b82f6",fg="#f1f5f9",anchor="w")
lowest_ranking_label.place(relx=0.89,rely=0.47,anchor="center")
lowest_student_name_big=tk.Label(lowest_frame,text="",font=("Arial",50,"bold"),bg="#172959",fg="#f1f5f9",anchor="w")
lowest_student_name_big.place(relx=0.45,rely=0.42,anchor="center")
lowest_percentage_label=tk.Label(lowest_frame,text="",font=("Arial",20),bg="#172959",fg="#f1f5f9",anchor="w")
lowest_percentage_label.place(relx=0.38,rely=0.48,anchor="center")
lowest_table_header=tk.Label(lowest_frame,text="STUDENTS NAMES       ID#       TOTAL MARKS     EXAM MARKS         OVERALL              GRADE",font=("Courier New",12),bg="#172959",fg="#f1f5f9",anchor="w")
lowest_table_header.place(relx=0.29,rely=0.65,relwidth=0.6,anchor="w")
lowest_display_frame=tk.Frame(lowest_frame,bg="#121b30")
lowest_display_frame.place(relx=0.26,rely=0.75,relwidth=0.65,relheight=0.4,anchor="nw")

# This sets up the navigation sidebar with all the menu buttons
nav_frame=tk.Frame(root,bg="#1e3a8a")
nav_frame.place(relx=0.05,rely=0.13,relwidth=0.15,relheight=1)
tk.Button(nav_frame,text="Home",font=("Arial",16),relief="flat",borderwidth=0,bg="#1e3a8a",fg="#6478af",activeforeground="#f1f5f9",activebackground="#1e3a8a",command=show_main).place(relx=0.19,rely=0.09,anchor="center")
tk.Button(nav_frame,text="Instructions",font=("Arial",16),relief="flat",borderwidth=0,bg="#1e3a8a",fg="#6478af",activeforeground="#f1f5f9",activebackground="#1e3a8a",command=show_instructions).place(relx=0.3,rely=0.19,anchor="center")
tk.Button(nav_frame,text="All Records",font=("Arial",16),relief="flat",borderwidth=0,bg="#1e3a8a",fg="#6478af",activeforeground="#f1f5f9",activebackground="#1e3a8a",command=show_all_records).place(relx=0.3,rely=0.29,anchor="center")
tk.Button(nav_frame,text="Individual Record",font=("Arial",16),relief="flat",borderwidth=0,bg="#1e3a8a",fg="#6478af",activeforeground="#f1f5f9",activebackground="#1e3a8a",command=show_individual_record).place(relx=0.4,rely=0.39,anchor="center")
tk.Button(nav_frame,text="Highest Mark",font=("Arial",16),relief="flat",borderwidth=0,bg="#1e3a8a",fg="#6478af",activeforeground="#f1f5f9",activebackground="#1e3a8a",command=show_highest_mark).place(relx=0.31,rely=0.49,anchor="center")
tk.Button(nav_frame,text="Lowest Mark",font=("Arial",16),relief="flat",borderwidth=0,bg="#1e3a8a",fg="#6478af",activeforeground="#f1f5f9",activebackground="#1e3a8a",command=show_lowest_mark).place(relx=0.31,rely=0.59,anchor="center")
tk.Button(nav_frame,text="Quit",font=("Arial",16),relief="flat",borderwidth=0,bg="#1e3a8a",fg="#f1f5f9",activeforeground="#f1f5f9",activebackground="#1e3a8a",command=quit_program).place(relx=0.1,rely=0.79,anchor="center")

# This binds a click event to close the dropdown when clicking outside of it
all_records_frame.bind("<Button-1>",lambda e: toggle_sort_dropdown() if dropdown_visible and e.widget != sort_button else None)

# This starts the main event loop that runs the application
root.mainloop()