CS 3550 Assignment 2 (CSS)
==========================

**Status**: Final \
**Due**: Phase 1 due **6 Sep**, Phase 2--5 due **13 Sep**

About
-----

In this assignment you'll write a CSS file to style the HTML pages you
wrote for [Homework 1](hw1.md). Your pages will then exactly match the
typography, appearance, and layout of elements in the screenshots
provided. You will thereby demonstrate that you can:

- Write valid CSS code and serve it from a web server
- Modify HTML code to make it accessible from CSS selectors
- Convert visual designs into web page stylesheets
- Build moderately complex layouts using flex-box

The assignment is due Friday, 13 Sep before midnight. The course's
normal extension policy applies. Hand in your finished assignment by
pushing it to your repository on Github.

It may be useful to address any feedback you received on Homework 1
before or as you work on this assignment.

Phase 1: Serving a CSS file
---------------------------

Create a file named `main.css` in your `static/` directory. Add the
following contents:

    * { color: red; }

This CSS makes (almost) all text on the page red. Start your server
and test that http://localhost:8000/static/main.css shows exactly this
contents.

Edit your `index.html` file and add a `<link>` element pointing to the
`stylesheet` at `/static/main.css`. Open your `index.html` page. Make
sure that the text is red. If not, seek help.

Now edit the CSS file to replace `red` with `yellow`, and refresh the
`index.html` page in your browser. The text is likely *still red*, not
yellow. (If it's already yellow, that's OK too.) This is due to
*caching*: your browser remembers the CSS from before and is saving
time by not re-requesting it. If you direct your browser to the
`main.css` file directly and refresh, you'll see it now say `yellow`,
and if you then refresh the `index.html` file it will now have yellow
text. Be careful of caching as you do this assignment!

Go through the other four HTML files and add the same `<link>` element
to all of them. If all five total pages now have yellow text, commit
everything to Github. You should see the Github Action turn green. If
so, Phase 1 is done. If you do not, get help.

General rules
-------------

You can remove the yellow-text line from your CSS now. (You will
continue to pass Phase 1.)

When writing any CSS for the phases below, stick to the following
rules. You don't need to memorize them: refer back here as you do the
assignment.

- All lengths should use `rem` units, except borders and shadows,
  which should use `px`, and a few widths where you should use `%`
- Always use unitless multipliers for `line-height`
- Do not use any `display` mode except the default one and `flex`
- Do not use tables for layout. (You should still use them for tabular data.)
- Do not use any colors besides `black`, `#444`, `gray`, `#ddd`, and
  `white`, plus `#204a87` and `#b1c3de`
- Include external fonts using `@import` instead of `<link>` elements.
- Never use `style` attributes on HTML elements or `<style>` elements.
- All five HTML pages should share the same CSS file. Where page
  elements are repeated, the same CSS rule should apply on each page.
- Minimize your use of the `class` and `id` attributes. Prefer
  selecting things based on tag names and containment.
- Do not use negative `margin` values or the `float` or `position`
  properties.

You may need to modify your HTML, but the modifications should be
quite limited---mostly adding `class` and `id` attributes, and `div`
and `span` elements, a handful of times. Keep your HTML valid and
semantically-meaningful. Limit the number of `class` and `id`
attributes and `div` and `span` elements that you use.

Try to organize your CSS file so that each Phase below is clearly
separated in the file. If possible, add a comment indicating which CSS
rules are for which Phase. This helps the TAs grade your assignment.

It's helpful to have names for the various parts of the page. Pages
contain:

- A gray *navigation banner* at the top of each page. The text inside
  it ("CS 3550", "Assignments", and "Profile") is called the contents
  of the navigation banner.
- The rest of the page is called the *main contents*
- At the top of the main content is a *page title* and *subtitle*. The
  title is text like "Homework 1 (HTML)" or "Your grades", and the
  subtitle is the smaller text below that like "Due September 08" or
  "All grades out of 100". All pages have a page title, but not all of
  them have a subtitle.
- Two pages have blue boxes with text and links inside. These are
  called *action blocks*
- Pages that have tables always have a *header row* at the top

Phase 2: Typography
-------------------

Start by styling the text. All text on the page should use the [IBM
Plex Sans][ibm-plex-sans] font, except for code, which should use [IBM
Plex Mono][ibm-plex-mono]. Include both fonts on the page; they are
available on Google Fonts. Use the `@import` method instead of the
`<link>` method. Do not create a separate `<style>` element in your
HTML. Instead, note that the `<style>` element suggested by Google
Fonts has a single long `@import` line. Copy that `@import` line into
your `main.css` file.

[ibm-plex-sans]: https://fonts.google.com/specimen/IBM+Plex+Sans
[ibm-plex-mono]: https://fonts.google.com/specimen/IBM+Plex+Mono

*Note:* This `@import` method is less efficient than adding the
`<link>`, so you wouldn't want to do it in a production website. It
forces the browser to download your CSS file before it can start to
download fonts, whereas with `<link>` it can start both in parallel.
However, `@import` is much simpler for us to grade, and the speed
impact isn't large, so `@import` is required for this assignment.

You will need to include three styles for the Sans font (regular,
regular italic, and bold) and one style for the Mono font (regular).
We don't have any bold italic text or any other weights, so don't
include any others. Including fewer styles makes for a smaller font
file, which makes it download faster and saves mobile data for your
users. In some fonts, you can also turn on or off alphabets to save
even more space, but this isn't the case for the IBM Plex family.

Add a CSS rule to set all text on the page to use IBM Plex Sans. Add a
rule to make source code (like the text `assignments.html`, included
in the page `assignment.html`) use IBM Plex Mono. Make sure to add a
"fall-back" to a system font using the CSS keyword fonts.

Set the `line-height` to 1.25× for all text on the page. However,
inside tables, it is helpful to have a larger spacing between rows,
because a table row has large gaps between columns, which makes it
harder for your eye to follow a single row. Set the `line-height` to
1.5× inside tables.

In the page navigation banner (the part that contains the text CS 3550
and the links to "Assignments" and "Profile"), set all text to the
same size, which is 25% larger than the default font size. Set the
links in the navigation banner to be dark gray. Make the text "CS
3550" bold, while leaving all of the links not bold.

In the page title (the part that changes for different pages), set the
title to be 50% larger than the default font size.

Set the "Description" header in `assignment.html` to be the default
font size.

Set all text inside the login form to be 25% larger than the default
font size. This includes the "Username:" and "Password:" labels; the
"Log in" label inside the button; and any text the user types into the
username and password fields.

Phase 3: Styling Links, Forms, and Tables
-----------------------------------------

Make it so that when you hover over a link in the navigation banner,
but not when you're not hovering over it, the link has an underline.
This hints to people that the link is clickable.

Ensure that all tables span the whole width of the main content. You
may use `%` units for this.

Make table columns that contain numbers right-aligned. These include
the "weight" column in `index.html` and the "graded" column in
`profile.html`. You will need to add the same `class` to each cell in
that column. (This is tedious now, but once we generate some of this
HTML with templates, some of the code duplication will go away.) The
header for that column should also be right-aligned. The other headers
should be left-aligned.

Now consider two pages that contain forms: the `submissions.html` page
and the `login.html` page.

In `login.html`, the login form should contain three rows (for the
username, password, and button) with a gap of `1rem` between rows.
Both text entries and the submission button should be half as wide as
the main content. The text entries should be aligned to the right edge
of the main content, while the button should be centered. You may need
to add more HTML elements wrapping each label and text entry to
accomplish this. You may use `%` units if you'd like.

In `submissions.html`, leave the text entries in the "grade" column
and the "Submit" button at their default widths.

Make sure the "Submit" and "Back to assignment" links are horizontally
adjance to each other.

Phase 4: Borders, backgrounds, and whitespace
---------------------------------------------

Remove any default `margin`s or `padding` on the `html` and `body`
elements. This way, the very first element on the page (the navigation
banner) touches the top, left, and right of the browser window.

Give the navigation banner at the top of the page a gray background.
Make the main "CS 3550" text black and bold, but the other links
should be slightly lighter and have regular weight. (Use the list of
colors in the "General rules" to determine the correct color.) Give
the navigation banner a gray shadow. It should have no offset in
either the *x* or *y* directions and have a 5 pixel blur radius.

Two of the pages (`assignment.html` and `profile.html`) have action
cards. Set their border, background, and padding to match the
screenshots.

Make sure there are `3rem` of whitespace between the page title and
the navigation banner.

Make sure there is `0.5rem` of whitespace above and below the text in
the navigation header. Make sure there is `1rem` of space to the left
and right of text in the navigation header and to the left and right
of text in the main content. Importantly, this whitespace should be
added inside the navigation header; its gray background should stretch
all the way to the edge of the page.

Make sure there is `1rem` of whitespace between most other elements on
in the main content, including: after the page title/subtitle; around
action cards; in `assignment.html`, before and after the "Description"
heading; between paragraphs and list items; and before and after
tables and figures.

Add a light gray horizontal line below the page title. It should go
*between* the page title and subtitle. There should not be any extra
whitespace before or after this horizontal line. Do not use an `<hr>`
element.


Phase 5: Flexible Box Layout
----------------------------

Ensure that the navigation banner has all of its contents in a
horizontal row. Use flex-box. The text "CS 3550" and the "Assignments"
link should be on the left, while the "Profile" link should be on the
right. There should be a gap of `1rem` between the "CS 3550" text and
the "Assignments" link.

Also make sure that the link inside each action card is at the right
end of the card.

As of now, the main content and page header should be as wide as the
screen, less `1rem` of whitespace on the left and right. However, this
doesn't look good on large displays, where the page becomes too wide.
Instead, we want to limit the width of both contents of the navigation
header and the main content to `50rem`.

If the page is wider than `52rem`, the navigation header contents and
main content should be `50rem` wide, centered on the page, with extra
whitespace on the left and right. The gray background of the
navigation banner and its shadow should always span the whole width of
the browser window.

If the page is narrower than `52rem`, the navigation header contents
and main content should shrink, always leaving exactly `1rem` of extra
space on left and right. There should be no scroll bar, at least not
until the main content is as wide as the screenshot on
`assignment.html`.

Here are some screenshots of the page with wider and narrower browsers:

|                                                                                |                                              |                                                                            |
|--------------------------------------------------------------------------------|----------------------------------------------|----------------------------------------------------------------------------|
| ![The profile page in a narrow browser window](screenshots/profile-narrow.png) | ![The profile page](screenshots/profile.png) | ![The profile page in a wide browser window](screenshots/profile-wide.png) |

This effect is tricky to replicate and may require nested `flex-box`
containers. Make sure that the navigation banner and main content
behaves correctly in all five HTML pages.

Make sure no other layout issues are affected by page width; for
example, the input boxes on the `login.html` page should stay half the
page width even as the page changes size. Likewise, the link inside
the action card should always be on the right side of the action card,
even as the page changes width.

Write a cover sheet
-------------------

Run your server and view each page on your website in your browser.
Make sure that each page looks as close as possible to the screenshots
above. Read through the requirements of Phases 1--5 and ensure that
all requirements are met. Moreover, make sure that your website HTML
still passes all the requirements of [Assignment 1](../hw1/index.md)
despite any changes you may have made.

If you find any problems, use the browser developer tools to
understand and correct the problem.

Once you are sure everything works correctly, copy-and-paste the
following text into a new empty text file called "HW2.md":

```
Homework 2 Cover Sheet
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

Real-world websites use CSS to change how they look; writing CSS is
part of just about any website. The specific stylistic features you
worked on---such as headers, navigation bars, text, forms, and
tables---are common.

Of course, real-world websites tend to have more pages, necessitating
more HTML, and may have more complex layouts including overlapping
elements, pop-up menus, and so on. These are also implemented with
CSS, and the CSS skills you've developed here are a foundation you can
build on to achieve more complex layouts.

Also, a real-world website needs to be designed before that design can
be implemented. Here, the design is given to you directly, and in
larger companies there may be a dedicated designer who then hands off
the design to you to implement. But in smaller firms, you may be
responsible for design as well.

Grading Rubrik
--------------

This assignment is worth 100 points. The different phases are worth
different weights:

**Phase 1** is worth 5 points. It is graded on:

- Your web server must serve a CSS file at
  http://localhost:8000/static/main.css
- You must not have any other CSS files, `style` attributes, or
  `<style>` elements.
- All five HTML pages created in [Homework 1](hw1.md) must link to
  that CSS file.
  
If you pass all auto-tests, then you have completed this phase.

**Phase 2** is worth 15 points. It is graded on:

- Pages must use IBM Plex Sans for all text except code, and IBM Plex
  Mono for all code
- Line heights must be set appropriately for both text and tables
- Font sizes, weights, and colors must be set appropriately for each
  element

**Phase 3** is worth 20 points. It is graded on:

- Hovering and clicking links in the navigation banner should change
  underlining and color as required
- Tables should span the whole width of the main content, and columns
  must be aligned appropriately.
- The login form must be laid out with the required widths and gaps.
- On the submissions page the form elements and links must have the
  required widths, layout, and gaps.

**Phase 4** is worth 25 points. It is graded on:

- The navigation banner must have the required background and shadow
- Action cards must have the appropriate background, border, and
  padding
- Margins and paddings must be set on all elements as required.
- Both main content and navigation banner must have the required
  gap from the edge of the viewport.
- There must be a light gray horizontal line between the page title
  and subtitle, or after the page title, on each page

**Phase 5** is worth 30 points. It is graded on:

- The main content must have the required width on both narrow and
  wide viewports.
- The navigation banner must stretch the whole width of the viewport,
  and its content must have the required width on both narrow and wide
  viewports.
- Links inside action cards must be at the right edge of the action
  card.

**Cover Sheet** is worth 5 points. It is graded on:

- Cover sheet is formatted correctly.
- All questions on the cover sheet have coherent answers.

Note that if your cover sheet does not list all people you discussed
the assignment with, or misrepresents others' work as your own, that
is academic misconduct and can result in severe sanctions beyond the 5
points the cover sheet is worth. In the most severe cases, the
sanction for academic misconduct is failing this course.
