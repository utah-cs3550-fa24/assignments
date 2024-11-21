CS 3550 Assignment 5 (Permissions)
==================================

**Status**: Final \
**Due**: Phase 1 due **1 Nov**, Phase 2--5 due **8 Nov**

About
-----

In this assignment you'll add user authentication and authorization to
your application. You'll also fill out the student side of the
application. Specifically, you will:

- Set up a login system for users
- Customize what a user sees based on their identity
- Enforce a security policy for all existing views / actions
- Set up file uploads and secure them

The assignment is due Friday, 8 Nov before midnight. The course's
normal extension policy applies.

Phase 1: Enabling logins
------------------------

In your `views.py` file, add the following line to the top:

    from django.contrib.auth import authenticate, login, logout

Next, open up the `login.html` template. It should contain an HTML
form; make sure this form makes a `POST` request to `/profile/login/`
and contains the mandatory `{% csrf_token %}` block somewhere inside.
As usual, this form submits to the same URL that it is served from.
Also make sure that each `<input>` inside that form has a `name` and
an appropriate `type`.

Find your `login_form` controller. Modify it so that, for `POST`
requests, it:

1. Extracts the username and password from the POST request;
2. Then calls [Django's `authenticate` function][docs-auth]
   (this function either returns a `User` object or `None`);
3. If authentication succeeds,
   calls [Django's `login` function][docs-login]
   and then redirects to the `/profile/` page.
4. If authentication fails, re-renders the form,
   same as if it were a `GET` request.

You are expected to follow the links above to learn how to call
`authenticate` and `login` correctly. Note that it is possible that
the `POST` request does not contain a username or a password. You can
handle this using Python's `get` method on hash tables:

    username = request.POST.get("username", "")

This returns the `username` value in `request.POST` if there is one,
or the empty string if there isn't. There's no user with an empty
username, so in this case `authenticate` will fail.

In your `profile` view, pass `request.user` to the template. In the
`profile.html` template, in the action card, display the user's
`get_full_name`. This step is important because it allows you to test
whether or not you actually logged in.

Test that you can log in and see the user you've logged in as on the
profile page. If you've run `makedata.py`, you can log in as:

- The admin user `pavpan`
- The TAs `g` and `h`
- The students `a`, `b`, `c`, and `d`

Each user's password is the same as their username.

Next, define a `logout_form` controller. This controller should call
[Django's `logout` function][docs-logout] and redirect to
`/profile/login/`. Modify `urls.py` so that `/profile/logout/` routes to
this new `logout_form` controller. Modify the `profile.html` template
so that the "Log out" link takes the user to `/profile/logout`.

Test that logging out works correctly. When you are logged out, you
should either see no name or "AnonymousUser" on the profile page.

If you can log in, see your user's name on the profile page, and log
out, you should be done with this phase. You can confirm by using the
auto-tester. If the auto-tester passes, you are done with this phase.

[docs-auth]: https://docs.djangoproject.com/en/4.2/topics/auth/default/#django.contrib.auth.authenticate
[docs-login]: https://docs.djangoproject.com/en/4.2/topics/auth/default/#django.contrib.auth.login
[docs-logout]: https://docs.djangoproject.com/en/4.2/topics/auth/default/#django.contrib.auth.logout

Computing Grades
----------------

Since this is a grading application, we need to talk about how grades
are computed (at least in this series of homework assignments). It
should match what most actual professors do in your actual classes.

Basically, the grade for a student is computed by considering each
assignment in turn and looking at the student's submission for that
assignment. The student's submission could be in one of four states:

- Submitted and graded
- Submitted but not yet graded
- Not submitted, because the assignment isn't due yet
- Missing, because the assignment is past due and there's no submission

A submitted and graded assignment has a score, which is written as a
percentage (the score on the submission divided by the maximum points
offered by that assignment). Missing assignments are treated as if the
score is a 0. Ungraded or not due assignments are ignored for the
purpose of grade calculation.

To put this more formally, you can compute a student's grade by
looping over assignments and tracking their available and earned grade
points:

- Graded assignments contribute their weight to available grade points
  and the grade percentage times the weight to earned grade points.
- Missing assignments contribute their weight to available grade
  points and nothing to earned grade points.
- Ungraded and not due assignments contribute nothing to either.

Here are some example assignments for a given student showing the
weight and points of each assignment, the status of the student's
submission for each assignment, their score (if graded), and the
contribution of that assignment to the student's available and earned
points.

| Assignment | Weight | Points | Status   | Score | Available | Earned |
|------------|--------|--------|----------|-------|-----------|--------|
| HW1        | 100    | 75     | Graded   | 70    | 100       | 93.33  |
| HW2        | 50     | 75     | Missing  |       | 50        | 0      |
| HW3        | 60     | 100    | Graded   | 73    | 60        | 43.8   |
| HW4        | 74     | 90     | Ungraded |       |           | 0      |
| HW5        | 100    | 50     | Not Due  |       |           | 0      |

In total, this student had 210 available points and earned 137.13, for
a current grade of 65.3%.

A student with zero available grade points (because no assignments are
due yet, for example) is considered to have a current grade of 100%.

Phase 2: Customizing views
--------------------------

Now that users can log in, this Phase consists in modify each view to
customize it to the currently-logged-in user. To do so, you will need
to use a few Django features.

Recall that the currently-logged-in user is `request.user`. Note that
if the user is _not_ logged in, this will be an `AnonymousUser`. You
can tell whether a user is the `AnonymousUser` by looking at the
`User`'s `is_authenticated` field, which is `True` for real users and
`False` for the `AnonymousUser`.

You will need to determine what kind of user someone is. You can do so
by examining the `groups` field on a `User`. This is a `ForeignKey`
style field, so, for example, if you want to know if a user is a
student, you can check if the user's `groups` contain any objects with
a `name` of `"Students"`, like this:

```
def is_student(user):
    return user.groups.filter(name="Students").exists()
```

Besides students and TAs, there is also the `AnonymousUser` (which you
can check for with `is_authenticated`, as above) and also the
administrative user named `pavpan`, which you can test for with the
`is_superuser` field. In most cases, the anonymous user is treated
like a student while the administrative user is treated like a TA.

To customize a view, you may want to pass an `is_student` or `is_ta`
variable from the controller to the view.

Now let's customize each view.

The `assignments` view (you might call it `index`) does not need any
customization.

The `assignment` view should change which "action card" is shown based
on the logged in user. Students and the `AnonymousUser` should see the
action card that allows uploading files. TAs and the administrative
user should see the action card that shows total submissions. In
either case, the card and form handling should be specialized to the
current user, not Alice Algorithm or Garry Grader. One additional
complication is that for the administrative user, instead of showing
total submissions assigned to the current grader, it should show total
submissions.

The `submissions` view should show all submissions assigned to the
current user when viewed by a TA, or just all submissions when viewed
by the administrative user.

The `profile` view is most complex, and we'll handle it next.

Phase 3: Computing Grades
-------------------------

When viewed by a TA, the profile should show the number of submissions
graded by and assigned to the current user for each assignment, like
it does now. (Though make sure you're using the current user, not
Garry Grader.) When viewed by the administrative user, it should show
the graded and total number of submissions (ignoring who grades each
submission).

When viewed by a student, it should show a totally different table.
The table body should have one row per assignment, and for each
assignment it should show the assignment name (linked to the
assignment page) and the status of the current student's submission
for the assignment (with graded submissions showing the submission's
percentage grade), as in the following screenshot:

![](screenshots/profile-student.png)

Additionally, there should be an extra table footer containing a
single "current grade" row showing the student's computed current
grade.

Let's add status information to the `assignment.html` page as well. In
the action box, show different text depending on the submission
status:

- For a submitted, graded assignment, show the text "Your submission,
  filename.pdf, received X/Y points (Z%)".
- For a submitted, ungraded, past due assignment, show the text "Your
  submission, filename.pdf, is being graded".
- For a submitted, not due assignment, show the text "Your current
  submission is filename.pdf".
- For a not submitted, not due assignment, show the text "No current
  submission".
- For a not submitted, past due assignment, show the text "You did not
  submit this assignment and received 0 points".

In each case, `filename.pdf` should be the submission's file's `name`.
The X, Y, and Z values should be correctly computed. Show the form
only if the assignment isn't due yet. Also, in your `assignment`
controller, before saving an upload make sure the deadline has not
passed. Otherwise, return an `HttpResponseBadRequest`, which you can
import from `django.http`. (As usual, we must repeat every check both
on the server side, where the upload is handled, and on the client
side, when generating the form.)

At the moment, every submission is assigned to Garry. That's not nice!
Write a `pick_grader` function. You can do that by just writing a new
`def` line in `views.py`. It's just a function, not a controller! It
only becomes a controller if you route URLs to it, which we won't.

`pick_grader` should take one argument, an `Assignment`, and return
one `User` object, the TA which should grade a new submission to that
assignment. Specifically, it should return the TA with the fewest
submissions to grade for that assignment. We want to find this TA in
one query. To do so:

- Select the "Teaching Assistants" group
- Take its `user_set`
- Use the [Django `annotate` function][docs-annotate] to annotate each
  TA with a field called `total_assigned` which counts its `graded_set`.
- Then order by `total_assigned`, to get the TAs in order of assigned
  submissions
- Get the `first` TA, which should now be the one with the fewest
  `total_assigned` submissions.

[docs-annotate]: https://docs.djangoproject.com/en/4.2/ref/models/querysets/#annotate

We haven't talked about the `annotate` function in class, and this is
a more advanced use of the Django query functionality. But you should
be able to follow the recipe above using the documentation. The
benefit of this approach is that the `pick_grader` method issues a
single query and is thus faster.

Now set the grader for new submissions using `pick_grader`. However,
if a student has *already* submitted an assignment, and is simply
replacing the file, don't change the assigned TA.

Test that you can log in as a student and submit a submission to a
not-yet-due assignment (such as "Homework 5"). Then use the Django
admin to figure out which TA was assigned to grade that submission,
log in as that TA, and check that the submission appears on the
assignment's submissions page. Make sure new submissions get assigned
to both TAs, Helen and Garry.


Phase 4: Protecting your views
------------------------------

Some of the views don't really make sense for some users, so we should
restrict who can view them.

First of all, our application is for logged-in users. Let's enforce
that. Add the following line to your `views.py`:

    from django.contrib.auth.decorators import login_required

You can now use the [`login_required` decorator][docs-logreq] to mark
certain views as being inaccessible to `AnonymousUser`. You should
make every view `login_required` except the `login_form` and
`logout_form` views.

[docs-logreq]: https://docs.djangoproject.com/en/4.2/topics/auth/default/#the-login-required-decorator

To make this work correctly, we'll need to make a few other changes.
First, open your `settings.py` and add this line to the bottom:

    LOGIN_URL = "/profile/login/"
    
You should now be able to log out, attempt to visit the profile or
assignments page, and be sent back to the login page.

We can make this redirect process a little smoother. Ideally, after
you log in, you should be redirected back to whatever page you were
originally trying to access. Django supports this: when the
`login_required` decorator sends you to the login page, it includes a
`GET` parameter called `next` containing the URL that the user should
be redirected to upon successful login.

Note the chain of events here---the user is first sent to the login
page, and in this first `GET` request there's a `next` parameter. Then
they fill out the form, making a *second* `POST` request, and we need
to redirect at that point. So we need to plumb this `next` parameter
from the first request to the second.

So, when the `login_form` controller gets a `GET` request, extract the
`next` variable from the `request.GET` parameters and pass that to the
`login.html` template. (If there's no `next` variable, use `/profile/`
as the default.)

Then, in the `login.html` template add a `hidden` input element named
`next`. Modify `login_form` so it redirects to the value of this input
element instead of always redirecting to `/profile/`. If the login
fails, make sure to pass in the `next` parameter when re-rendering the
login form.

Test that you can log out, attempt to go to the assignments page, be
asked to log in, log in, and be automatically redirected back to the
assignments page.

While we're editing `login_form`, let's also add an error message when
login fails. When login fails, pass an `error` parameter to the
template containing the string "Username and password do not match".
In the `login.html` template, use an HTML `<output>` element
containing the `error` string if an `error` string is passed. It
should show up bold and red.

[docs-upt]: https://docs.djangoproject.com/en/4.2/topics/auth/default/#django.contrib.auth.decorators.user_passes_test

Before redirecting to the `next` parameter, we need to make sure this
URL is to our own server; otherwise we'd have an "open redirect"
vulnerability. This is a little tricky; the code needs to look like
this:

```
def login_form(request):
    if request.method == "POST":
        # ...
        next_url = request.POST["next"]
        if url_has_allowed_host_and_scheme(next_url, None):
            return redirect(next_url)
        else:
            return redirect("/")
```

Here the `url_has_allowed_host_and_scheme` function checks whether the
redirect is to our own server, which is necessary to prevent open
redirects. If the URL includes a hostname, and is thus dangerous, this
function will return `False` and in this case we redirect to the main
page instead of the attacker-supplied URL. You can test this by
logging in to, say, `/profile/login/?next=http%3A%2F%2Fgoogle.com`;
you should not be redirected to Google.

Finally, let's make sure the submissions page is locked down. Only TAs
should be able to access the submissions page. Also, TAs should only
be able to change grades for submissions they are assigned.

To enforce the first rule, test that the current user is a TA and
raise the `PermissionDenied` exception, which you can import from
`django.core.exceptions`, if not. (Alternatively, you can use the
`user_passes_test` decorator if you'd like.)

The second rule is more complex, so add a `change_grade` method to
your `Submission` model. It should take in a `User` object and a new
`grade` and raise a `PermissionDenied` exception if the user is not
allowed to change the grade. (If the user is allowed to change the
grade, update the `grade` field but don't call `save`.) Call this
method in the `submissions` controller instead of accessing the
`grade` field directly. This way, the security policy is defined and
enforced in a single place, and you're less likely to make a mistake
in your code that subverts the security policy.


Phase 5: Protecting file uploads
--------------------------------

Finally, we need to make sure that uploaded files can only be viewed
by the right people. Specifically, we want to make sure that the only
people who can view a submission are the student who submitted it, the
TA assigned to grade it, and the administrative user.

Add a `view_submission` method on the `Submission` model. It should
take in a `User` object and return the submission's `file` field. In
this method, check that the current user is either 1) the submission's
`author`, or 2) the submission's `grader`, or 3) the administrative
user. If not, raise the `PermissionDenied` exception. Once again, we
define this security policy in a single, centralized place to make it
less likely that we get it wrong somewhere.

Use this method in the `show_upload` controller. Also add the
`login_required` decorator---this doesn't enforce security (since the
anonymous user won't pass the test above) but it does help with the
log-in-and-redirect logic you implemented in Phase 3.

Check that if you log in as a TA, copy the URL for a submitted file,
and then log out (or log in as a different TA or student), you get a
"Permission denied" page when you attempt to go to that URL. This is
important, because the file names for uploaded files are guessable,
and you wouldn't want students looking at each other's submissions.

We also want to make sure file uploads do not harm our server. We
should already be putting those files in a separate `uploads/` folder,
which is a good start. (We will make sure never to store anything
important or sensitive in here.) Let's also limit uploaded files to
64MiB. In your `assignment` controller, test the `size` field of the
uploaded file. If it is too large (that is, over 64 MiB), do not save
the uploaded file in the submission. Instead, re-render the assignment
page with an error message. Put the error message in an `<output>`
element at the start of the submission form. It's important that we
use the `size` field instead of trying to read the file: if an evil
user uploaded a really big file, reading that file might use a lot of
memory or disk space. So we must check the file size before we check
the file's contents.

Let's also make sure we only accept PDF uploads. In your `submit`
controller, before storing the uploaded file inside a submission,
check that its `name` field ends with `.pdf`. Also, make sure the
uploaded file starts with the string `%PDF-`. You can check that
property with `next(file.chunks()).startswith(b'%PDF-')`. Most tools
will treat files with an extension of `.pdf` and starting with those
five bytes as PDF files. If either of these checks fails, don't store
the uploaded file in a submission. This will keep it from being saved
to disk. Instead, re-render the assignment page with an error message.

To make this more convenient for users, also add the `accept`
attribute to the file input in the upload form. You should only accept
`application/pdf` files.

Finally, let's make sure uploaded files don't harm other users who
view them (like TAs). In your `show_upload` controller, repeat the two
checks above---that the file extension is `.pdf` and that the file
contains `%PDF-` as its first five bytes---before showing it to the
user. (You might want to put these checks in an `is_pdf` function.)
The dummy files aren't PDFs, so you can test those. The reason we're
doing these tests twice (once on upload and once when viewing) is so
that, if we ever add more checks, they'll apply retroactively to
already-uploaded files. Raise an `Http404` error if any of these tests
fail. (You can import it from `django.http`.)

Finally, we don't want the user's browser to try to *guess* what type
of file the upload is. It might guess wrong, with bad results. Modify
your `show_upload` controller to construct the `HttpResponse` on one
line and return it on another. Before returning the response, set two
headers on it:

- `Content-Type` should be set to `application/pdf`, so the browser
  knows it is a PDF file.
- `Content-Disposition` should be set to `attachment; filename="..."`
  where the `...` is the submission's file name. This indicates to the
  browser that it should treat this as a "download", not a "page
  navigation".
  
This is not a complete list of steps you'd need to take to make this
grades application safe (for example---is it really safe for the
grader to view arbitrary, untrusted PDF files?) but it's pretty good.
This might seem like quite a lot of work. Yes! Support for file
uploads and especially downloads opens you up to a lot of possible
attacks, some of them difficult to prevent.

In many cases the best solution isn't extensive technical protections
but logging and out-of-band enforcement mechanisms. For example, you
might imagine that if a student does upload a PDF file that somehow
hacks the grader's computer, this would be addressed with university
disciplinary action, not with ever-more-elaborate checks. Though this
out-of-band enforcement mechanism would itself want to check logs
(say, to determine who in fact uploaded the file), which would then
also need to be protected from attackers. Security is very hard!


Write a cover sheet
-------------------

Run your server and view each page on your website in your browser.
Read through the requirements of Phases 1--5 and ensure that all
requirements are met. Test logging in as students, TAs, and the
professor and using various portions of the site.

Once you are sure everything works correctly, copy-and-paste the
following text into a new empty text file called "HW5.md" in the root
of your repository:

```
Homework 5 Cover Sheet
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

Once you are done, commit everything and push it to Github.

How you will use this
---------------------

Almost any large web application has a notion of identities,
authentication, and authorization. The specific implementation here is
simple but is sufficient for most small and even medium-sized
applications. And we followed best practices, like having a
centralized security policy, that are helpful when applications get
larger and have more-complex security policies.

More complex authorization and authentication schemes, as necessary in
applications with plugins or for integration between different
systems, are still grounded in core ideas like identity and
permission. Moreover, file uploads almost always come with extensive
security checks, similar or even more stringent than the ones used
here. You should be quite careful about allowing users to upload
arbitrary files to your server.

Grading Rubrik
--------------

This assignment is worth 100 points. The different phases are worth
different weights:

**Phase 1** is worth 5 points. It is graded on:

- It is possible to log in with a username and password
- Invalid usernames or passwords don't log in
- The profile page shows your username once you've logged in
- It is possible to log out

**Phase 2** is worth 15 points. It is graded on:

- The assignment page shows the correct action box for each user.
- On the submissions page, TAs only see submissions they are assigned
  to grade.
- On the submissions page, the admin user sees all submissions.
- Students are offered the option of submitting assignments

**Phase 3** is worth 20 points. It is graded on:

- On the profile page, TAs only see counts of submissions they are
  assigned to grade
- On the profile page, the admin user sees counts of all submissions
- On the profile page, students see their grade for each submission
- The profile page correctly calculates students' current grades
- Submissions are only allowed if the assignment is not yet due
- Submitted assignments are automatically assigned a TA

**Phase 4** is worth 25 points. It is graded on:

- All pages redirect to the login page if you're not logged in
- "Next" redirects from the login page are handled correctly
- Invalid logins show an error message
- The submissions view is not available to students
- TAs cannot change grades of submissions they are not assigned, even
  by constructing a special HTTP POST request.
- The security policy is enforced in model methods.

**Phase 5** is worth 30 points. It is graded on:

- Only the student author and the assigned TA can view a submission
- The security policy is enforced in model methods.
- Only PDF files can be uploaded (checked with file name and initial bytes)
- Only files below 64 MiB can be uploaded
- Only PDF files can be viewed, even if uploaded
- The `Content-Type` and `Content-Disposition` headers are sent

**Cover Sheet** is worth 5 points. It is graded on:

- Cover sheet is formatted correctly.
- All questions on the cover sheet have coherent answers.

Note that if your cover sheet does not list all people you discussed
the assignment with, or misrepresents others' work as your own, that
is academic misconduct and can result in severe sanctions beyond the 5
points the cover sheet is worth. In the most severe cases, the
sanction for academic misconduct is failing this course.
