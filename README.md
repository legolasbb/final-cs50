<h2>About project:</h2>
My project implements app for schools with multiple functionalities.  App divides into two parts, staff and students and has following functionalities
<h4>Funcionalities:</h4>
<ul>
    <li>Plan page allows staff to add new lessons. Each lesson has day, time, subject and teacher attached to it. Always when trying to add new lesson, its time is checked for collisions with other lessons that this class or teacher have. Switching between plan and lesson add form is done on client side, using javascript. Both students and staff can display their plan. For students it displays all lessons that group that they are assigned to has, for teacher all lessons that they teach.</li>
    <li>
    Homework page allows staff to give homework to any group in school.  Each homework is made of subject, content and deadline. On students page they can display all of the homeworks that are before the deadline. Staff is able to display all of the homework that they given and give grades based on the answers of the students. Staff can also edit given grades. Switching between given homework and watching submissions add form is done on server side. Switching between submissions page and singular submission add form is done on client side, using javascript.
    </li>
    <li>
    Grades page display grades. For teacher it displays all subjects that they gave grades from. Students see all of the subjects and grades that they received together with calculated average for each subject. I used javascript to change color of grades based on their value (low grades - red/yellow, good grades - green)
    </li>
    <li>
    Home page displays upcoming homework (by deadline) for both students and staff and latest grades (only for students)
    </li>
    <li>
    Register page allows user to choose their account type, school, and group. Creating new groups and schools can only be done on admin page.
    </li>
<hr>
<h2>Distinctiveness and Complexity:</h2>
<h5>Complex data architecture</h5>
I had to create 7 database models (School, Group, User, Lesson, Homework, Submission, Grade), which all are connected with each other. Every student belongs to a group which must belong to school. Same for grades which are connected to specific submission and other models. It required me to create much more complicated queries than in any other project before.
<h5>Dual role interface</h5>
App includes two distinct types of users (Staff, Student). It required me to implement proper access controls, so some features aren’t accessed by wrong group. The staff side includes adding, grading and editing homework, creating new lessons. On the other side students are able to submit their homework. It also required me to tailor some ui designs for specific group.
<h5>Hybrid client-side/server-side implementation</h5>
Some UI transitions are handled on client side (e.g., switching between schedule display and lesson-add form) are handled client-side with JavaScript; other transitions (e.g., between homework overview and grading view) are managed server-side. 
<hr>
<h2>Files:</h2>
<ul>
    <li>
    homework.html -display all homework and form to add new
    </li>
    <li>
    plan.html -displaying plan and form to add new lesson
    </li>
    <li>
    su_grade.html - displaying grades and averages of student viewing the page
    </li>
    <li>
    st_grade.html - displaying grades from subjects that staff member has given homework
    </li>
    <li>
    submission.html - displaying contents of homework and allowing students to send submission
    </li>
    <li>
    submissions.html - displaying submissions of students and ability to grade them
    </li>
    <li>
    colors.js - color grading grades based on their value in st_grade.html and su_grade.html
    </li>
    <li>
    grade.js - switching between submissions and grading form in submissions.html
    </li>
    <li>
    homework.js - switching between displaying homework and adding form (for staff) in homework.js
    </li>
    <li>
    plan.js - switching between displaying plan and adding form (for staff) in plan.html
    </li>
    <li>
    register.js - displaying different input fields based on chosen user type in register.html
    </li>
</ul>
<hr>
<h2>Mobile responsivity:</h2>
I implemeted stacking instead of inline display and dropdown menu instead of regular navigation bar for smaller screens.