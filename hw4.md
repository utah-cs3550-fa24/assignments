CS 3550 Assignment 4 (Forms and Controllers)
============================================

**Status**: Final \
**Due**: Phase 1 due **18 Oct**, Phase 2--5 due **25 Oct**

About
-----

In this assignment you'll extend the Django application you wrote in
[Assignment 3](hw3.md) to allow uploading submissions and grading
them. You will:

- Write HTML forms to allow for file and grade submission
- Handle form submissions and update the database in response
- Produce human-readable error messages for invalid form submissions

The assignment is due Friday, 18 Oct before midnight. The course's
normal extension policy applies. Hand in your finished assignment by
pushing it to your repository on Github.


Phase 1: Form submission
------------------------

Open up your `submissions.html` template. Check that all of the
`<input>` elements and also the `<button>` element are inside a single
`<form>` element. If you did [Assignment 1](hw1.md) correctly, this
should already be the case.

Add an `action` attribute to that `<form>` element whose value is the
URL `/N/submissions`, where `N` is the assignment ID. This is the URL
of the submissions page. Also add a `method` attribute with value
`post`. Add the line `{% csrf_token %}` somewhere inside the form.

Modify your `submissions` function to add an `if` statement to the
beginning, like this:

```python
def submissions(request, assignment_id):
    if request.method == "POST":
        return redirect(f"/{assignment_id}/submissions")
    # ...
```

You can import `redirect` from `django.shortcuts`. Make sure that
submitting the form causes your browser to reload the page, with no
errors. You can test this by typing something into one of the input
boxes; clicking "Submit" should clear it.

Once everything works, commit everything to Github. You should see the
Github Action turn green. If so, Phase 1 is done. If you do not, get
help.


Phase 2: Saving grades
----------------------

One big flaw with our grading application is that you can't actually
grade submissions yet. Let's fix that.

Each `<input>` element in the submissions template needs a unique
`name` attribute. Name each one `grade-N`, where `N` is the submission
ID. Inside the `submissions` controller, the `request.POST` field
contains the value for each input field. It is basically a hash table
that maps the field's `name` to its `value`.

Iterate through `request.POST`. Note that in Python, when you iterate
over a hash table, you get each *key* in the hash table. Skip any keys
that don't start with `grade-`. If you'd like, you can put all this
iteration into a separate function that you call from `submissions`;
this can make your code a little more organized.

For each input field, extract the submission ID from the key. You can
use Python's `removeprefix` method on strings and the `int` built-in
function to convert a string to an integer.

For each input field, look up its `Submission` using the ID you
extract.

Use `request.POST[key]` to get the value the TA typed into the score
field and call the `float` function on it to convert it to a
floating-point number. Set the submission's score to this number. If
the field is an empty string, set the submission's score to `None`
instead.

Remember to `save` any model object that you change. Or, if you'd
like, you can try using the `bulk_update` method instead; this method
is faster because each `save` issues a database query to update a
single object, while `bulk_update` updates lots of objects in a single
query.

Phase 3: Validating grades
--------------------------

Your `submissions` view function needs to handle various kinds of
errors. First, it needs to make sure grades are numbers. Second, they
must be positive numbers between 0 and the number of points offered on
that assignment. (We won't support extra credit in our application.)
Finally, the grades have to be for submission IDs that actually exist
and are for the correct assignment.

Handle each of these errors. In Python, you can do this with
`try`/`except` blocks like so:

```python
try:
    # stuff that might error
except ExceptionType:
    # exception handler code
```

The `ExceptionType` might be `ValueError` if parsing a string as a
float fails, or `Submission.DoesNotExist` if you try to load a
non-existant submission, or they can be something else. You'll see the
name printed in your terminal if you don't catch an error.

As you loop through `request.POST`, use this or a similar technique to
detect all four types of error listed above. Do not save invalid
grades, but do save valid ones. (In other words, if one submission is
given an invalid grade but another one is given a valid grade, save
the valid grade but not the invalid one). Then, instead of redirecting
to the submissions page, re-render your submissions template directly.

Record each error you come across in a data structure of some kind;
you might try a dictionary mapping submission IDs to a possibly-empty
list of errors. When you rerender the submissions page, show these
error messages in the template. Put each error message in an
`<output>` element, and put all the `<output>` elements for a
submission in a new `<td>` element that you add to the end of each row
in the submissions table. You might need to do some data
transformations before passing the list of submissions and errors to
the template.

Write good, or at least not bad, error messages.

If you ever see an input field with in invalid submission ID, that
error message doesn't correspond to any specific submission on the
page. Instead, put a generic error message in an `<output>` element,
placed before the table of submissions, for each invalid submission
ID.

In your `main.css`, make `<output>` elements bold and red.

Make sure the `<input>` elements on the submissions page have the
right `type` attribute. Add `min`, `max`, and `step` attributes. Allow
arbitrary fractions. Add a rule your `main.css` giving invalid input
elements a 2 pixel, solid red border. Make sure that typing in a
non-number, or too-big or too-small a number, prevents form submission
and gives the input field a red border.

Clearly label these rules in your `main.css` file, such as with a
comment reading "Homework 4 changes here".


Phase 4: Enabling file uploads
------------------------------

Another flaw with the grading application is that you can't yet submit
homework assignments. Let's fix that too.

Modify the `assignment.html` template and add a second action card
before the already-existing one. This will be the action card students
see, but since we don't yet handle login/logout in our application,
we'll just show the action card for Alice Algorithm (username `a`) to
everyone.

The action card should contain one paragraph and one form. The
paragraph should read either

- "Current submission: filename.pdf", where the filename is
  `submission.file.name`; or
- "No current submission", if there's no current submission for Alice
  for the assignment in question.

Note that you'll need to look up Alice's submission, if any, in the
`assignment` controller.

Below that paragraph should be a new form. It should submit to `/N/`
using the `POST` method and the `multipart/form-data` value for its
`enctype` attribute. The form should contain a file input (use
`type=file`) and a button to submit the form. Don't forget to add the
`{% csrf_token %}`.

Handle `POST` requests in the `assignment` controller. You will need to:

- Look up the assignment from the ID in the URL
- Get the submitted file object from `request.FILES`
- Look up Alice's submission for that assignment
- If a submission exists, change its `file` field to the submitted
  file object
- If a submission does not exist, create one.
- Save the submission
- Redirect back to the assignment page

Note that, when creating a new submission, you will need to assign a
grader and a score for the submission. New submissions haven't been
graded, so leave the score `None`. Assign Garry Grader as the grader.
(Poor Garry!)

Test that you can submit a submission to a not-yet-due assignment
(such as Homework 5) and that a link to this submission then shows up
on the action card. However, the link won't work yet.


Phase 5: Serving file uploads
-----------------------------

Finally, we need to make sure that we can actually view uploaded
files.

Edit your `settings.py` and add the following two lines:

    MEDIA_ROOT = "uploads/"
    MEDIA_URL = "uploads/"
    
Delete and re-create the database, and re-create the dummy data.

Edit `submissions.html` and make sure each row in the table links to
the submission's file's `url` field. Because of your changes in
`settings.py`, this `url` field will now start with `/uploads/`.
Similarly, in `assignment.html`, make sure the submission file name
links to the submission's file's `url` field. These links won't work
yet.

We now need to add a controller to serve these uploaded files. Add the
following line to your `urls.py`:

    urlpatterns = [
       # ...
       path('uploads/<str:filename>', views.show_upload),
    ]

Define a `show_upload` controller, which takes the normal `request`
argument and also a `filename` argument, which will be a string.

Inside this controller, look up the submission whose file's `name`
field is equal to the `filename` argument from the URL. This is a
unique field on files. Then execute this code (which assumes that the
submission is stored in `submission`):

    def show_upload(request, filename):
        # ...
        return HttpResponse(submission.file.open())

This code basically reads the file and sends its contents in the HTTP
response. Test that you can now view submissions, both on the
submissions page and on the assignment page.


Write a cover sheet
-------------------

Run your server and view each page on your website in your browser.
Read through the requirements of Phases 1--5 and ensure that all
requirements are met. Visit invalid URLs and submit invalid grades.

If you find any problems, use the browser developer tools to
understand and correct the problem.

Once you are sure everything works correctly, copy-and-paste the
following text into a new empty text file called "HW4.md" in the root
of your repository:

```
Homework 4 Cover Sheet
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

Naturally, any web application has to handle form submissions to
collect or modify data from users. Moreover, handling invalid data is
a big part of the polish that makes applications easy to use, and are
a large part of the effort of developing applications. The error
hanlding here is actually still more limited than ideal---for example,
it doesn't preserve invalid grades when re-displaying the form---but
it at least protects the database from invalid data.

One thing we did not focus on in this assignment is security. Handling
user uploads is risky, especially if you don't trust your users, and
serving user uploads to others also opens up a host of both technical
and legal liabilities. We'll address some of these issues in the next
assignment, but the version in *this* assignment is probably too
dangerous to make publicly available.

Grading Rubrik
--------------

This assignment is worth 100 points. The different phases are worth
different weights:

**Phase 1** is worth 5 points. It is graded on:

- Your web server must start up without error
- Your web server must serve all pages, including the submission page
- Form element on submissions page has correct `action` and `method`.
- Clicking the "Submit" button should reload the page without any errors
  
If you pass all auto-tests, then you have completed this phase.

**Phase 2** is worth 20 points. It is graded on:

- Grade fields all have unique `name` attributes
- Submitted grades show up when page is re-visited
- It is possible to save fractional grades
- It is possible to save an empty grade
- New grades are actually saved to the databse
- After successful grade submission, user is redirected back to
  submissions page

**Phase 3** is worth 30 points. It is graded on:

- Invalid grades (like the word "hello") are not saved
- Grades that are too big (1000 points) or too small (-5 points) are
  also not saved
- Grades for invalid submission IDs (modify the page using the
  developer tools to test this) are also not saved and do not lead to
  errors
- The submissions form is re-rendered with error messages if an
  invalid grade is submitted
- The error messages are placed near the appropriate input box
- Error messages for invalid submission IDs are shown at the top of
  the form
- Error messages are bold and red
- Invalid input fields turn red and block submission

**Phase 4** is worth 30 points. It is graded on:

- A second action card is shown on the assignment page
- The action card shows the current submission's file name or "No
  current submission" appropriately
- The action card shows a file submission form
- Submitting a submission works and updates the database
- New submissions are assigned Garry as a grader and have an empty
  score

**Phase 5** is worth 10 points. It is graded on:

- Uploaded files and dummy data files are saved in `uploads/`
- The submissions and assignment pages link to submissions
- Viewing uploaded files works

**Cover Sheet** is worth 5 points. It is graded on:

- Cover sheet is formatted correctly.
- All questions on the cover sheet have coherent answers.

Note that if your cover sheet does not list all people you discussed
the assignment with, or misrepresents others' work as your own, that
is academic misconduct and can result in severe sanctions beyond the 5
points the cover sheet is worth. In the most severe cases, the
sanction for academic misconduct is failing this course.
