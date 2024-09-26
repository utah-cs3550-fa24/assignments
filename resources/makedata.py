import datetime

import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cs3550.settings")
django.setup()

from django.core.files.base import ContentFile
from grades.models import User, Group, Assignment, Submission

def midnight(month, day):
    if month < 11 or month == 11 and day < 3:
        tz = datetime.timezone(datetime.timedelta(hours=-6), "MDT")
    else:
        tz = datetime.timezone(datetime.timedelta(hours=-7), "MST")
    return datetime.datetime(2024, month, day, 11, 59, 59, 999999, tz)

def check_has_data():
    return Group.objects.all().count() or \
        User.objects.all().count() or \
        Assignment.objects.all().count() or \
        Submission.objects.all().count()

def initial_data():
    tas, _ = Group.objects.get_or_create(name='Teaching Assistants')
    students, _ = Group.objects.get_or_create(name='Students')

    prof = User.objects.create_superuser(
        "pavpan", "pavpan@cs.utah.edu", "pavpan",
        first_name="Prof.", last_name="Panchekha",
    )
    ta1 = User.objects.create_user(
        "g", "g@cs.utah.edu", "g",
        first_name="Garry", last_name="Grader",
    )
    ta2 = User.objects.create_user(
        "h", "h@cs.utah.edu", "h",
        first_name="Helen", last_name="Helper",
    )
    tas.user_set.add(ta1, ta2)

    s1 = User.objects.create_user(
        "a", "a@cs.utah.edu", "a",
        first_name="Alice", last_name="Algorithmer",
    )
    s2 = User.objects.create_user(
        "b", "b@cs.utah.edu", "b",
        first_name="Ben", last_name="Bitdiddle",
    )
    s3 = User.objects.create_user(
        "c", "c@cs.utah.edu", "c",
        first_name="Cody", last_name="Coder",
    )
    s4 = User.objects.create_user(
        "d", "d@cs.utah.edu", "d",
        first_name="Debby", last_name="Debugger",
    )
    students.user_set.add(s1, s2, s3, s4)

    hw0 = Assignment.objects.create(
        title="Github username",
        description="Submit a text file with your github username",
        deadline=midnight(8, 1),
        weight=1,
        points=1
    )
    hw1 = Assignment.objects.create(
        title="Homework 1 (HTML)",
        description="""
<p>In this assignment, you will set up a web server serving HTML web
pages for the grading application:</p>

<ul>
<li>Configure and start a <em>basic web server</em> using Django</li>
<li>Create <em>basic web pages</em> using HTML for data/content</li>
</ul>
        
<p>For example, here is a page <b>you will make</b>, in a file called <code>assignments.html</code>:</p>

<img class='screenshot' src='/static/assignment.png' alt='A screenshot of the assignments page' />
""",
        deadline=midnight(8, 30),
        weight=100,
        points=100
    )
    hw2 = Assignment.objects.create(
        title="Homework 2 (CSS)",
        description="""
<p>In this assignment, you will enhance the visual appearance of your grading application by applying CSS styles:</p>

<ul>
    <li>Create a <em>separate CSS file</em> to manage your styles</li>
    <li>Apply <em>basic styling</em> to your HTML elements (colors, fonts, spacing)</li>
    <li>Implement a <em>responsive layout</em> using flexbox</li>
    <li>Add <em>hover effects</em> to interactive elements</li>
</ul>

<p>Your task is to style the following pages:</p>

<ol>
    <li>Home page</li>
    <li>Assignments list</li>
    <li>Individual assignment view</li>
</ol>

<p>Remember to use <strong>semantic class names</strong> and follow <strong>CSS best practices</strong> for maintainable code.</p>""",
        deadline=midnight(9, 13),
        weight=100,
        points=100
    )
    hw3 = Assignment.objects.create(
        title="Homework 3 (Models and Views)",
        description="""
<p>In this assignment, you will dive into the backend of your grading application by implementing models and views:</p>

<ul>
    <li>Design and create <em>database models</em> using Django's ORM</li>
    <li>Implement <em>simple queries</em> for assignments and submissions</li>
    <li>Set up <em>Django views</em> to handle data processing and rendering</li>
</ul>

<p>You will need to implement the following models:</p>

<ol>
    <li><code>Assignment</code> (title, description, due date, max score)</li>
    <li><code>Submission</code> (student, assignment, submission time, uploaded file)</li>
</ol>

<p>Your views should handle these key functionalities:</p>

<ul>
    <li>Listing all assignments</li>
    <li>Displaying assignment details</li>
</ul>

<p><strong>Note:</strong> Ensure your views are properly connected to your URLs and templates.</p>
""",
        deadline=midnight(9, 27),
        weight=100,
        points=100
    )
    hw4 = Assignment.objects.create(
        title="Homework 4 (Controllers)",
        description="""
<p>In this assignment, you will implement controllers to handle complex operations in your grading application, focusing on assignment submission, grade editing, and auto-assignment features:</p>

<ul>
    <li>Create <em>controllers</em> to manage business logic</li>
    <li>Implement <em>assignment submission</em> functionality</li>
    <li>Develop a system for <em>editing and updating grades</em></li>
    <li>Design an <em>auto-assignment algorithm</em> for distributing grading tasks</li>
</ul>

<p>Your controllers should handle the following key functionalities:</p>

<ol>
    <li><code>submit_file</code>:
        <ul>
            <li>Handle file uploads for assignments</li>
            <li>Validate submission deadlines</li>
            <li>Generate confirmation for successful submissions</li>
        </ul>
    </li>
    <li><code>grade_submissions</code>:
        <ul>
            <li>Allow TAs to input and edit grades</li>
            <li>Implement grade calculation based on rubrics</li>
            <li>Provide an interface for leaving feedback</li>
        </ul>
    </li>
</ol>

<p><strong>Note:</strong> Ensure your controllers interact properly with your models and views from previous assignments.</p>

<p>Bonus: Implement <em>unit tests</em> for your controller methods to ensure reliability and correctness.</p>
""",
        deadline=midnight(10, 25),
        weight=100,
        points=100
    )
    hw5 = Assignment.objects.create(
        title="Homework 5 (Users and Permissions)",
        description="""
<p>In this assignment, you will implement user authentication and authorization features for your grading application, ensuring that different user types (students, TAs, and administrators) have appropriate access and permissions:</p>

<ul>
    <li>Set up <em>user authentication</em> using Django's built-in authentication system</li>
    <li>Implement <em>log-in and log-out</em> functionality</li>
    <li>Define and apply <em>permission sets</em> for different user roles</li>
</ul>

<p>Your tasks include:</p>

<ol>
    <li><strong>User Authentication:</strong>
        <ul>
            <li>Identify the current user</li>
            <li>Implement secure login and logout functionality</li>
        </ul>
    </li>
    <li><strong>Permissions and Access Control:</strong>
        <ul>
            <li>Define permissions for each user role</li>
            <li>Implement view-level permissions (e.g., only TAs can grade assignments)</li>
            <li>Add object-level permissions (e.g., students can only view their own submissions)</li>
        </ul>
    </li>
    <li><strong>Integration:</strong>
        <ul>
            <li>Update existing views to respect user permissions</li>
            <li>Modify templates to show/hide elements based on user role</li>
        </ul>
    </li>
</ol>

<p><strong>Note:</strong> Ensure that all sensitive operations are properly secured and that user data is handled safely.</p>""",
        deadline=midnight(11, 8),
        weight=100,
        points=100
    )
    hw6 = Assignment.objects.create(
        title="Homework 6 (JavaScript)",
        description="""
<p>In this assignment, you will enhance the interactivity and user experience of your grading application by implementing client-side JavaScript features:</p>

<ul>
    <li>Create <em>asynchronous forms</em> for seamless data submission</li>
    <li>Develop a <em>grade projection widget</em> for students to estimate their final grade</li>
    <li>Use <em>modern JavaScript practices</em> including ES6+ syntax and Promises/async-await</li>
</ul>

<p>Your tasks include:</p>

<ol>
    <li><strong>Asynchronous Forms:</strong>
        <ul>
            <li>Convert existing forms (e.g., assignment submission, grading) to use AJAX</li>
            <li>Implement real-time form validation</li>
            <li>Display loading indicators and success/error messages without page reloads</li>
            <li>Use the Fetch API for making HTTP requests</li>
        </ul>
    </li>
    <li><strong>Grade Projection Widget:</strong>
        <ul>
            <li>Create an interactive widget allowing students to input hypothetical grades for future assignments</li>
            <li>Calculate a projected final grade based on current grades and user input</li>
        </ul>
    </li>
    <li><strong>General JavaScript Enhancements:</strong>
        <ul>
            <li>Implement dynamic sorting and filtering of assignment lists</li>
        </ul>
    </li>
</ol>

<p><strong>Requirements:</strong></p>
<ul>
    <li>Use the jQuery library for DOM manipulation and AJAX requests</li>
    <li>Implement error handling for all asynchronous operations</li>
    <li>Ensure your JavaScript works across modern browsers (Chrome, Firefox, Safari, Edge)</li>
</ul>

<p><strong>Note:</strong> Remember to update your Django views to handle AJAX requests and return appropriate JSON responses.</p>
""",
        deadline=midnight(11, 22),
        weight=100,
        points=100
    )
    hw6 = Assignment.objects.create(
        title="Homework 7 (AWS)",
        description="""
<p>In this final assignment, you will deploy your grading application to the cloud using Amazon Web Services (AWS) EC2:</p>

<ul>
    <li>Set up an <em>AWS account</em> and navigate the AWS Management Console</li>
    <li>Launch and configure an <em>EC2 instance</em></li>
    <li><em>Deploy your Django application</em> to the EC2 instance</li>
    <li>Configure <em>security settings</em> and <em>networking</em> for your deployed application</li>
</ul>

<p>Your tasks include:</p>

<ol>
    <li><strong>AWS Setup:</strong>
        <ul>
            <li>Create an AWS account (if you don't already have one)</li>
            <li>Explore the AWS Management Console</li>
            <li>Set up IAM users and configure appropriate permissions</li>
        </ul>
    </li>
    <li><strong>EC2 Instance Setup:</strong>
        <ul>
            <li>Launch an EC2 instance with an appropriate Amazon Machine Image (AMI)</li>
            <li>Configure security groups to allow necessary inbound/outbound traffic</li>
            <li>Generate and use a key pair for secure SSH access</li>
        </ul>
    </li>
    <li><strong>Application Deployment:</strong>
        <ul>
            <li>Install necessary software on the EC2 instance (e.g., Python, Django, database)</li>
            <li>Transfer your application code to the EC2 instance</li>
            <li>Configure your Django settings for production environment</li>
        </ul>
    </li>
    <li><strong>Web Server Configuration:</strong>
        <ul>
            <li>Install and configure a web server (Nginx)</li>
            <li>Configure your web server to proxy requests to the Django server</li>
        </ul>
    </li>
    <li><strong>Final Steps:</strong>
        <ul>
            <li>Set up a domain name (optional) and configure DNS</li>
            <li>Implement basic monitoring and logging</li>
        </ul>
    </li>
</ol>

<h2>Requirements:</2>
<ul>
    <li>Document each step of your deployment process</li>
    <li>Implement proper security measures (HTTPS)</li>
    <li>Ensure your application is accessible and functioning correctly on the public internet</li>
</ul>

<p><strong>Note:</strong> Be cautious with AWS resources to avoid unexpected charges. Remember to shut down resources when not in use.</p>
""",
        deadline=midnight(11, 22),
        weight=100,
        points=100
    )
    
    Submission.objects.create(
        assignment=hw0,
        author=s1,
        grader=ta1,
        file=ContentFile("Github username for Alice Algorithm", name="a.txt"),
        score = 1.0,
    )
    Submission.objects.create(
        assignment=hw0,
        author=s2,
        grader=ta2,
        file=ContentFile("Github username for Ben Bitdiddle", name="b.txt"),
        score = 1.0,
    )
    Submission.objects.create(
        assignment=hw0,
        author=s3,
        grader=ta1,
        file=ContentFile("Github username for Cody Coder", name="c.txt"),
        score = None,
    )

    Submission.objects.create(
        assignment=hw1,
        author=s1,
        grader=ta1,
        file=ContentFile("HW1 for Alice Algorithm", name="a1.txt"),
        score = 93.0,
    )
    Submission.objects.create(
        assignment=hw1,
        author=s2,
        grader=ta2,
        file=ContentFile("HW1 for Ben Bitdiddle", name="b1.txt"),
    )
    Submission.objects.create(
        assignment=hw2,
        author=s1,
        grader=ta1,
        file=ContentFile("HW2 for Alice Algorithm", name="c2.txt"),
    )

if __name__ == "__main__":
    if check_has_data():
        print("""It looks you've already run the makedata.py script.
If you've changed the model and want to rerun the script, run:
        
    python3 manage.py makemigrations
    rm db.sqlite3
    python3 manage.py migrate
    python3 makedata.py
""")
        exit(1)
    initial_data()

