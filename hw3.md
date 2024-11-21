CS 3550 Assignment 3 (Models and Views)
=======================================

**Status**: Final \
**Due**: Phase 1 due **20 Sep**, Phase 2--5 due **27 Sep**

About
-----

In this assignment you'll write a backend for the frontend you
developed in [Assignments 1](hw1.md) [and 2](hw2.md). The grading
application will then generate all pages using a database, which we'll
initialize with some data. You will:

- Create models in Django to describe your application's data
- Query those models to extract view-relevant data
- Use templates to generate views from data

The assignment is due Friday, 27 Sep before midnight. The course's
normal extension policy applies. Hand in your finished assignment by
pushing it to your repository on Github.

Phase 1: Setup
--------------

Create a Django application called `grades` by running:

    python3 manage.py startapp grades

As usual, you may need to use `python` or `py` instead of `python3`,
or give the full path to your Python executable, just as you did for
[Homework 1](hw1.md). See the [installation guide](install.md) for
more.

This command should succeed and create a directory called `grades`
with files inside it called `models.py`, `admin.py`, and `views.py`.
(It will also contain `tests.py`, which we won't be using.)

Open the `settings.py` file in your `cs3550` directory. Find the
lines that define `INSTALLED_APPS` and add the string `'grades'` to
the list. This means that the `grades` app you just created is now
part of the project.

Inside the `grades` directory create a subdirectory called `templates`.
Move all of the HTML files in `static` to this new `templates` folder.
(You can also delete `test.html`, if you still have it.)

Open `views.py` in the `grades` directory and add the following line
to the top of the file:

    from . import models
    
Add the following lines to the bottom:

    def index(request):
        return render(request, "index.html")

Make similar definitions for the other four pages (`assignment`,
`submissions`, `profile`, and `login_form`). For the `assignment` and
`submissions` view, the function should take an additional parameter,
`assignment_id`. Make sure to use the correct function name and the
correct template name. (Note that `login` is already a Django function
that we'll need later, so that function must be named `login_form`.)

Open the `urls.py` file in the `cs3550` directory and add the
following line to the top:

    from grades import views

Now add these entries to the `urlpatterns` list:

```python
path("", views.index),
path("<int:assignment_id>/", views.assignment),
path("<int:assignment_id>/submissions/", views.submissions),
path("profile/", views.profile),
path("profile/login/", views.login_form),
```

If you get an `AttributeError`, make sure you defined all five methods
in `views.py` and you gave each of them the correct name.

You should now be able to run your server, visit the following URLs,
and see the results:

- http://localhost:8000/
- http://localhost:8000/1/
- http://localhost:8000/1/submissions
- http://localhost:8000/profile
- http://localhost:8000/profile/login

If you see a `TypeError` check that your `assignment` and
`submissions` functions take two arguments: `request` and
`assignment_id`.

Once everything works, commit everything to Github, including the new
`grades` folder and the contents of the `migrations` folder inside it.
If you have one **do not** commit your `db.sqlite3` file. (This should
be the default, thanks to the `.gitignore` file in the repository. If
you accidentally do commit your database file, delete it and commit
again.) You should see the Github Action turn green. If so, Phase 1 is
done. If you do not, get help.

Phase 2: Writing a model
------------------------

Open up `models.py`. Add the following line to the top:

    from django.contrib.auth.models import User, Group

This imports the authentication system's `User` class, which we'll be
using to represent students and TAs, both of whom will be users of our
website. (It also imports a `Group` class, which we won't use in our
models.)

Define two classes in this file called `Assignment` and `Submission`.
Both should inherit from `models.Model` and contain `models.Field`
classes.

The `Assignment` class should have these fields:

- A short string (less than 200 characters) for the assignment `title`
- A long string for the assignment `description`
- A `deadline`, which is a date and a time
- An integer `weight` (which is how much the assignment is worth
  toward the final grade)
- An integer number of maximum `points` (which is how much this
  assignment is graded out of)
  
A `Submission` class should have these fields:

- The `assignment` it is a submission for
- The `author` who submitted the assignment
- The `grader` who is grading the assignment
- A `file` containing the submission itself
- A `score`, which is a floating-point number

Note that Django will automatically also add a unique,
auto-incrementing `id` field to each model.

As you define these fields, think carefully about:

1. Which fields have to allow blanks or nulls
2. Which fields should have defaults and what those defaults should be
3. For `ForeignKey` fields, what should happen if the related object
   is deleted

When defining the `grader` field, you will need to pass the
`related_name='graded_set'` argument to `ForeignKey`. (This is because
when class `X` has a `ForeignKey(Y)` field, then the `Y` class also
gains a field calls `x_set`. Normally this is fine, but since a
`Submission` has two users associated with it, Django needs to defined
two different sets of submissions for each `User` and we need to
supply the name of the second one.)

When you're finished, run:

    python3 manage.py makemigrations
    python3 manage.py migrate

This Phase will be graded by running a dummy data script, which you
can find [here](resources/makedata.py). You can run it on your own
machine by saving it to the same directory as `manage.py` and then
running:

    python3 makedata.py

If you need to edit your model (because you made a mistake) you must
remember to run:

    python3 manage.py makemigrations
    rm db.sqlite3
    python3 manage.py migrate
    python3 makedata.py

This deletes all existing data and reruns the script.

The dummy data script creates a superuser account with a username and
password of `pavpan`. It also creates two TAs (`g` and `h`) and four
students (`a`, `b`, `c`, `d`), eight assignments, and a number of
submissions. Each user's password is their username. Single-letter
usernames and passwords aren't realistic, of course, but later on this
will make it easy for you to log in and out as different users.

Register `Assignment` and `Submission` with the Django Admin, as
discussed in class. Make sure you can log in to the admin interface as
`pavpan` and then add, remove, or edit assignments and submissions.

Phase 3: All assignments view
-------------------------

Let's now implement the grades application. We won't yet be
implementing authentication, so for now we will only implement the
grader side of the application, specifically as if Garry Grader
(username `g`) is logged in. We'll make the five views you have right
now (index, assignments, submissions, profile, and login) generated
from templates and have those templates get their data from the
database.

Open `views.py` and add the following line to the top of the file (if
it's not there already):

    from . import models

This allows your view functions (a.k.a. controllers) to use the models
you defined.

Modify the `index` view function to retrieve all assignments and pass
them to the `index.html` template.

Now open up your `index.html` file. It should contain a table.
Delete all the content rows (not the header row) from the table; these
rows should be generated from the list of all assignments passed in by
the view. Specifically:

- The "Assignment" column should be the assignment's `title`
- Also the assignment title should link to `/N/`, where `N` is the
  assignment ID
- The "Due date" column should be the assignment's `deadline`,
  formatted appropriately. (Match the screenshot.)
- The "Weight" column should be the assignment's `weight`

Run your server with:

    python3 manage.py runserver

You should now be able to navigate to `http://localhost:8000/` and see
the assignments page. If it looks like the screenshot, move on to the
next phase.

If it happens to contain no rows, make sure you've run the `makedata`
script. If you haven't, run it:

    python3 manage.py migrate
    python3 makedata.py

If you now see data, you can move on. If you still don't see data,
it's probably some other bug---find and fix it before you move on.

Phase 4: Assignment view
------------------------

For the `assignment` view, you will need to look up the assignment
based on the assignment ID and pass that to the template.

The assignment description is supposed to contain HTML. When adding it
to the template, make sure to use the `safe` filter to allow raw HTML
to be directly added to the HTML.

For the action card, you will also need to look up:

1. How many total submissions there are to this assignment
2. How many of submissions are assigned to "you"
3. How many total students there are

For items (1) and (2) use the `submission_set` and `graded_set`
fields, which are the "reverse" of `ForeignKey`s that you added in
your model. Do not loop over submissions one by one; use the `count`
query operator instead. For item (3), you can use the following code
to find the total number of students:

    models.Group.objects.get(name="Students").user_set.count()

You can pass all of this data as additional template parameters.

Make sure the word "submissions" in the action card is correctly
pluralized. That is, it should say either "1 submission assigned to
you" or "2 submissions assigned to you". Also make sure all other
plurals are correctly pluralized; for example, an example worth one
point total should not say "1 points" in the subtitle, and if only 1
student exists the action card should not say that "1/1 submissions"
(pluralize based on the second number).

Make sure the `grade` link in the action card points to
`/N/submissions`, where `N` is the assignment ID.

Test that various assignments look normal. Test what happens if you
the visit the URL for an invalid assignment, like
http://localhost:8000/123456789/; this should show a 404 page instead
of a crash page. (Crash and 404 pages look similar in "debug mode",
but behave quite different once deployed.)

Phase 5: Submissions and Profile view
-------------------------------------

Write the `profile` view. The table should contain one row per
assignment. For each assignment, the "Graded" column should count how
many submissions are assigned to `g` and how many of those are graded
(which means a non-null `score` for that submission).

Do not count submissions, or graded submissions, by looping through
them; use the `count` query operator.

Write the `submissions` view. Like with the `assignment` view, you
will need to look up the `Assignment` in question by its ID and then
request all `Submission`s to that assignment whose `grader` is set to
`g`. The template should generate the table so that:

- The "Student" column has the submission's author's full name; use
  the `get_full_name()` method on `User`.
- The "Submission" link should point to the submission's `file.url`
  field. This link won't work, however, until Homework 5.
- The input field's `value` attribute should be the submission's
  `score`, if any.
  
The rows should be sorted by `author`'s `username`. The "All grades
out of" text at the top should show the assignment's `points` field
and the "Back to assignment" link should go back to the page for the
same assignment.

In each template, the navigation banner is the same. Create a new file
called `header.html` containing just this navigation banner. For the
tab title use the `title` template parameter. In each template,
replace the navigation banner with an `include` of `header.html`,
passing in the correct tab title. This should make your templates much
shorter.

Write a cover sheet
-------------------

Run your server and view each page on your website in your browser.
Read through the requirements of Phases 1--5 and ensure that all
requirements are met. Visit invalid URLs and submit invalid grades.

If you find any problems, use the browser developer tools to
understand and correct the problem.

Once you are sure everything works correctly, copy-and-paste the
following text into a new empty text file called "HW3.md":

```
Homework 3 Cover Sheet
----------------------

In this assignment, I completed:

- [ ] Phase 1
- [ ] Phase 2
- [ ] Phase 3
- [ ] Phase 4
- [ ] Phase 5

I discussed this assignment with:

- ...
- ...
- ...

[ ] I solemnly swear that I wrote every line of code submitted as part
of this assignment (except that auto-generated by Django).

The most interesting thing I learned in this assignment was ...

The hardest thing in this assignment was ...
```

In the first list, replace `[ ]` with `[x]` for each phase of the
assignment you completed.

In the second list, replace the `...`s with the name of your partner
as well as any other person (student, friend, family, online stranger)
that you discussed this assignment with.

In the oath below that, check the box. Recall that, while you may
discuss the assignment in broad strokes, you must write every line of
code submitted by you, as stated in the oath below this list. This
includes the use of AI tools such as ChatGPT.

In the last two paragraphs, replace the `...` with the most
interesting and the most difficult aspect of this assignment. Don't
just make them a single sentence; the instructors use your answers to
make these assignments more interesting and easier.

Once you are done, commit everything and push it to Github. **Make
sure to include the text "Please grade" in your final commit message**
to help TAs identify the right commit to grade.

How you will use this
---------------------

Web applications have backends just like this one, though typically
with many more model classes, views, and actions. However, the core
ideas, including models, views, and controllers, as well as concepts
like queries and templates, are the same, even in frameworks other
than Django and languages other than Python.

One thing we did not focus on in this assignment is performance. This
grading application would probably never see enough requests that
performance would be a problem, but widely-used web applications have
to focus intensely on performance to reduce costs. Performance is a
big focus in CS 4550 Web Software Development II.

Grading Rubrik
--------------

This assignment is worth 100 points. The different phases are worth
different weights:

**Phase 1** is worth 10 points. It is graded on:

- Your web server must start up without error
- Your web server must serve all the main URLs
- Your web server must continue to serve all static files, including
  the favicon, the CSS file, and the image on the assignment page.
  
If you pass all auto-tests, then you have completed this phase.

**Phase 2** is worth 30 points. It is graded on:

- You must define all of the necessary classes and fields.
- The correct field type should be used for each field.
- All fields must have the correct lengths, nullness, and blank
  settings, and fields with defaults should have reasonable defaults.
- Foreign key fields should have reasonable `on_delete` behaviors.

**Phase 3** is worth 10 points. It is graded on:

- The assignments view must be dynamically generated.
- Assignments for the assignments view are correctly queried from the
  database.
- Each column in the table uses the correct field.
- The due date is printed correctly.
- The assignment name links to the correct URL.

**Phase 4** is worth 20 points. It is graded on:

- The assignment view is dynamically generated.
- Assignment name, due date, and points are printed correctly.
- The total submissions and total students are printed correctly.
- Assignment description is correctly rendered (we should not see HTML
  tags on the page)
- "Grade" link goes to the correct page.

**Phase 5** is worth 25 points. It is graded on:

- The profile and submissions view is dynamically generated.
- Profile view contains one row per assignment.
- Profile view contains correct counts of assigned and graded
  submissions.
- Counts only refer to submissions assigned to `g`.
- Profile view uses queries, not loops, to count submissions.
- Submissions view contains one row per submission.
- All columns in the submission view are correctly generated.
- Only submissions for the current assignment are shown.
- Submissions are sorted by username.
- Other dynamically-generated parts of the Submissions page are
  correctly generated.
- Navigation banner is located only in `header.html` and never
  duplicated in templates.

**Cover Sheet** is worth 5 points. It is graded on:

- Cover sheet is formatted correctly.
- All questions on the cover sheet have coherent answers.

Note that if your cover sheet does not list all people you discussed
the assignment with, or misrepresents others' work as your own, that
is academic misconduct and can result in severe sanctions beyond the 5
points the cover sheet is worth. In the most severe cases, the
sanction for academic misconduct is failing this course.
