CS 3550 Assignment 4 (Forms and Controllers)
============================================

**Status**: Draft \
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
URL `/N/grade`, where `N` is the assignment ID. Also add a `method`
attribute with value `post`. Add the line `{% csrf_token %}` somewhere
inside the form.

Define a new view function called `grade`, with the following
contents:

```python
def grade(request, assignment_id):
    return redirect(f"/{assignment_id}/submissions")
```

You can import `redirect` from `django.shortcuts`.

Update `urls.py` to map the `/N/grade` URL to this new view function.
Make sure that submitting the form causes your browser to reload the
page.

Once everything works, commit everything to Github. You should see the
Github Action turn green. If so, Phase 1 is done. If you do not, get
help.


Phase 2: Saving grades
----------------------

One big flaw with our grading application is that you can't actually
grade submissions yet. Let's fix that.

Each `<input>` element in the submissions template needs a unique
`name` attribute. Name each one `grade-N`, where `N` is the submission
ID. Inside the `grade` controller, the `request.POST` field contains
the value for each input field. It is basically a hash table that maps
the field's `name` to its `value`.

Iterate through `request.POST`. Note that in Python, when you iterate
over a hash table, you get each **key** in the hash table. Skip any
keys that don't start with `grade-`.

For each input field, extract the submission ID from the key. You can
use Python's `split` method to split a string into substrings and
`int` to convert a string to an integer.

For each input field, look up its `Submission` using the ID you
extract.

Use `request.POST[key]` to get the value the TA typed into the score
field and call the `float` function on it to convert it to a
floating-point number. Set the submission's score to this number.

Remember to `save` any model object that you change. Or, if you'd
like, you can try using the `bulk_update` method instead; this method
is faster because each `save` issues a database query to update a
single object, while `bulk_update` can update lots of objects in a
single query.

Phase 3: Validating grades
--------------------------

Your `grade` view function needs to handle various kinds of errors.
First, it needs to make sure grades are numbers. Second, they must be
positive numbers between 0 and the number of points offered on that
assignment. Finally, the grades have to be for submission IDs that
actually exist.

Handle each of these errors. In Python, you can do this with
`try`/`except` blocks like so:

```python
try:
    # stuff that might error
except ExceptionType:
    # exception handler code
```

The `ExceptionType` might be `ValueError` if you parsing a string as a
float fails, or `Submission.DoesNotExist` if you try to load a
non-existant submission, or something else.

As you loop through `request.POST`, use this or a similar technique to
detect all three types of error listed above. Do not save invalid
grades, but do save valid ones. (In other words, if one submission is
given an invalid grade but another one is given a valid grade, save
the valid grade but not the invalid one). Then, instead of redirecting
to the submissions page, render your submissions template directly.

Record each error you come across in a data structure of some kind;
you might try a dictionary mapping submission IDs to a possibly-empty
list of errors. When you rerender the submissions page, use this data
structure to show error messages in the template. Put each error
message in an `<output>` element, and put all the `<output>` elements
for a submission in a new `<td>` element that you add to the end of
each row in the submissions table. You might need to do some data
transformations before passing the list of submissions and errors to
the template.

If you ever see an input field with in invalid submission ID, that
error message doesn't correspond to any specific submission on the
page. Instead, put a generic error message in an `<output>` element
before the table of submissions.

In your `main.css`, make `<output>` elements bold and red.

Make sure the `<input>` elements on the submissions page have the
right `type` attribute. Add `min` and `max` attributes. Add a rule
your `main.css` giving invalid input elements a 2 pixel, solid red
border.

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

- "Current submission: filename.pdf", where `filename.pdf` is a link
  to `submission.file.url`; or
- "No current submission", if there's no current submission.

Note that you'll need to look up Alice's submission, if any, in the
`assignment` controller.

Below that paragraph should be a new form. It should submit to
`/N/submit` and contain a file input (use `type=file`) and a button to
submit the form. Don't forget the `{% csrf_token %}`.

Add a `submit` controller and route `/N/submit` to it in `urls.py`.
Inside this controller, you will need to:

- Look up the assignment from the ID in the URL
- Get the submitted file object from `request.FILES`
- Look up Alice's submission for that assignment
- If a submission exists, change its `file` field to the submitted
  file object
- If a submission does not exist, create one.
- Save the submission
- Redirect back to the assignment page

Note that, when creating a new submission, you will need to assign a
grader and a score for the submission. The score is easy: new
submissions haven't been graded, so leave the score `None`. Assign
Garry Grader as the grader. (Poor Garry!)

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
       path('uploads/<str:filename>/, views.show_upload),
    ]

Define a `show_upload` controller, which takes the normal `request`
argument and also a `filename` argument, which will be a string.

Inside this controller, look up the submission whose file's `name`
field is equal to the `filename` argument from the URL. Then execute
this code (which assumes that the submission is stored in
`submission`):

    def show_upload(request, filename):
        # ...
        return HttpResponse(submission.file.open())

This code is basically it opens the file and sends its contents in the
HTTP response.

Test that you can now view submissions, both on the submissions page
and on the assignment page.


Write a cover sheet
-------------------

Run your server and view each page on your website in your browser.
Read through the requirements of Phases 1--5 and ensure that all
requirements are met. Visit invalid URLs and submit invalid grades.

If you find any problems, use the browser developer tools to
understand and correct the problem.

Once you are sure everything works correctly, copy-and-paste the
following text into a new empty text file called "HW4.md":

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

[ ] I solemly swear that I wrote every line of code submitted as part
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

**Phase 6** is worth 20 points. It is graded on:

- Form element on submissions page has correct `action` and `method`.
- `grade` view defined and accessible from a URL
- Submitting grades works
- It is possible to submit an empty grade
- Invalid grades (like the word "hello") are treated as if empty
- After successful grade submission, user is redirected back to
  submissions page
- Invalid requests receive appropriate error codes.

**Cover Sheet** is worth 5 points. It is graded on:

- Cover sheet is formatted correctly.
- All questions on the cover sheet have coherent answers.

Note that if your cover sheet does not list all people you discussed
the assignment with, or misrepresents others' work as your own, that
is academic misconduct and can result in severe sanctions beyond the 5
points the cover sheet is worth. In the most severe cases, the
sanction for academic misconduct is failing this course.
