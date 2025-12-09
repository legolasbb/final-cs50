# Gradebook / School Management System

A comprehensive web application designed for school management, facilitating interaction between Staff (teachers) and Students. This system manages schedules, homework assignments, submissions, and grading with a robust dual-role authentication system.

## Distinctiveness and Complexity

I chose to build a School Management System (LMS) for my capstone because I wanted to tackle a project that relies heavily on **relational data and permissions**, rather than just broadcasting content like the social network or wiki projects we built earlier in the course.

### Why this project is distinct
Most of the previous projects in CS50W (like "Network" or "Wiki") function on the premise that content is generally public or shared among peers. My project required a completely different architectural approach:

* **Role-Based Access is Central:** Unlike "Network," where every user can see every post, this application relies on strict data privacy. A major design goal was ensuring that **Staff** and **Students** have completely different experiences. A student logging in sees their personal grades and homework; a teacher logging in sees grading tools and lesson plans. This required me to implement conditional logic throughout my views and templates that simply wasn't necessary in previous projects.
* **Structured Data vs. Free Text:** While "Wiki" was about storing text blobs, this project is about storing structured, interconnected academic data. I moved away from simple listings (like in "Commerce") to building a weekly schedule system that mimics real-world school timetables, requiring me to manage data across specific days and timeslots.

### Why this project is complex
The complexity in this application comes from the backend logic required to maintain data integrity and the relationships between the 7 different database models.

* **The "Double-Booking" Problem:** One of the hardest features to implement was the scheduling system. I couldn't just let users post lessons whenever they wanted. I had to write a backend algorithm in `views.py` that checks for **collisions**—verifying if a specific group already has a lesson at a specific day and time before saving. This validation step adds a layer of complexity significantly higher than standard CRUD operations.
* **Relational Database Management:** Managing the data for this app was complex because almost every model depends on another. A `Grade` isn't just a number; it is tied to a `Student`, a `Lesson` (Subject), and a `Submission`. Retrieving this data to display a gradebook required writing complex Django queries to filter and join these tables efficiently.
* **Dynamic Calculations:** I didn't want the frontend to just display static numbers. In the backend, I implemented logic to dynamically calculate a student's average grade per subject every time the page loads. Additionally, I used JavaScript on the frontend to parse these values and apply color-coding (Green/Red) in real-time, giving immediate visual feedback on performance.

## File Structure and Contents

### Main Application (`classroom/`)
* **`models.py`**: I designed 7 models to handle the data relationships:
    * `User`: Extends the standard user to add specific flags for Student vs. Staff roles.
    * `School` & `Group`: Models to organize users into cohorts.
    * `Lesson`: Holds the schedule data (Day, Time, Subject).
    * `Homework` & `Submission`: Handles the assignment logic and file uploads.
    * `Grade`: Connects a student's work to a numerical score.
* **`views.py`**: This file contains the core controllers.
    * `index`: The entry point that checks `request.user` to decide whether to render the Student Dashboard or Staff Dashboard.
    * `plan`: Manages the schedule. It contains the validation logic to prevent time collisions when adding new lessons.
    * `grades`: A complex view that aggregates data. For students, it calculates averages; for teachers, it handles the input forms for updating scores.
    * `homework`: Handles both the creation of assignments (Staff) and the submission of work (Student).
* **`urls.py`**: Maps the application routes.
* **`admin.py`**: configured to allow superusers to manage the foundational `School` and `Group` data.

### Static Files (`classroom/static/classroom/`)
* **`styles.css`**: Custom styling to ensure the gradebook tables are readable and the mobile layout stacks correctly.
* **`colors.js`**: I wrote this script to scan the gradebook table, parse the integers, and assign a CSS class (green/yellow/red) based on the score.
* **`grade.js`**: Handles the UI switching on the grading page so teachers can toggle between viewing submissions and entering grades without a page reload.
* **`register.js`**: Makes the registration form dynamic. If a user clicks "Student," it asks for a Group Code; if they click "Staff," it asks for a Teacher ID.
* **`plan.js`** & **`homework.js`**: Helper scripts to toggle visibility of "Add" forms on the planning and homework pages.

### Templates (`classroom/templates/classroom/`)
* **`layout.html`**: The main skeleton of the site. It includes logic to show different navbar links depending on if the user is a Student or Staff.
* **`index.html`**: The dashboard showing recent activity.
* **`plan.html`**: A table view of the weekly schedule.
* **`homework.html`**: Displays active assignments.
* **`submission.html`**: The student interface for uploading work.
* **`submissions.html`**: The teacher interface for reviewing class work.
* **`st_grade.html`** & **`su_grade.html`**: Two separate templates for the Gradebook—one for teachers (editing) and one for students (viewing).

## How to Run

1.  **Install Django:**
    * `pip install Django`
2.  **Make migrations:**
    * `python manage.py makemigrations classroom`
    * `python manage.py migrate`
3.  **Create a Superuser (Crucial Step):**
    * `python manage.py createsuperuser`
    * Follow the prompts to create an admin account.
4.  **Run the development server:**
    * `python manage.py runserver`
5.  **Initialize Database (Required for functionality):**
    * Go to `http://127.0.0.1:8000/admin` and log in with the superuser account created in Step 3.
    * Click on **Schools** and create a new School object (e.g., "Harvard High").
    * Click on **Groups** and create a new Group object (e.g., "Class 1A").
    * **Why is this necessary?** The user registration form on the main site requires users to select an existing School and Group to join. Without creating these objects in the Admin panel first, new users cannot register.
6.  **Access the application:**
    * Navigate to `http://127.0.0.1:8000/` and register a new user (Staff or Student).