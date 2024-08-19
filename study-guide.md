Study Guide
===========

This document lists vocabulary, concepts, and syntax that you're
expected to know for the midterm and final. You should use this
document to study outside of class.

HTML
----

You should be able to use HTML to:

- Write valid HTML using the doctype, `<meta>`, `<link>`, `<title>`
- Style text using `<a>`, `<em>`, `<strong>`, `<code>`, `<img>`
- Structuring text using `<p>`, `<h1>` through `<h6>`, `<pre>`
- Structure pages using `<nav>`, `<header>`, `<footer>`, `<main>`
- Separate sections with `<article>`, `<section>`, `<aside>`
- Write lists using `<ul>`, `<ol>`, `<menu>`, `<li>`
- Write tables using `<table>`, `<thead>`, `<tfoot>`, `<tr>`, `<td>`, and `<th>`
- Use `&lt;`, `&gt;`, `&amp;`, `&quot;` escapes and `<!-- -->` comments

You should be able to look at a screenshot of a website or application
and write valid, semantically-meaningful HTML for it using standard
tags.

You should know key accessibility requirements, such as proper heading
hierarchies, textual alternatives for images, and language attributes.
You should be able to identify when HTML code is missing these
accessiblity requirements.

CSS
---

You should be able to write CSS code that uses tag, ID, and class
selectors, plus the `:hover` pseudo-class, and compound selectors
using the space combination type. You should be able to write
selectors to select various elements on an HTML page.

You should know the following CSS properties:

- `font-family`, `font-weight`, `font-style`, `font-size`, and
  `text-decoration`
- `color`, `background-color`, and `opacity`
- `border` (the three-value form) and its subproperties like
  `border-bottom` or `border-left-width`
- `border-radius` (the one-value form)

You should be able to explain the cascading rule, inheritance, and
shorthand properties.

You should be able to use the following types of values:

- For lengths, the `px`, `rem`, `vw`, and `vh` units
- For colors, hex colors or named colors
- For `line-height`, numeric multipliers

Flex-box
--------

You should be able to create flex containers and identify their flex
items to create complex layouts, including nested layouts with rows
and columns, using the `display: flex` and `flex-direction`
properties.

You should be able to assign widths and heights to flex items using
`width` and `height`. You should be able to use `flex-grow` and
`flex-shrink` to flexibly resize flex items. You should be able to
control white-space using `justify-content`, `gap`, and `align-items`.

The [Notes](notes.md#flex-box) have a short checklist you can follow
to build complex flex-box layouts. You should feel comfortable using
this checklist to create layouts from screenshots or wireframes.

You should be able to name the components of the CSS box model (width,
padding, border, margin) correctly. You should know the order of top,
right, bottom, and left in properties like `margin`.

Back-ends
---------

You should be able to define clients, servers, the client-server
architecture, message-passing, requests, and responses.

You should be able to identify the parts of a URL: the protocol (or
scheme), hostname (or domain), port, and path (or page).

You should be able to explain what components of a web server are
provided by Django. You should be able to explain the roles of the
model, view, and controller in a MVC-style web application. You should
be able to explain the roles of standard Django project files like
`settings.py`, `urls.py`, `models.py`, `views.py`, the `migrations/`
folder, the `static/` folder, and the `templates/` folder.

Models
------

You should know the following Django field types:

- `IntegerField`, `FloatField`, and `DecimalField`
- `CharField` and `TextField`
- `DateField` and `DateTimeField`
- `FileField` and `ImageField`

You should be able to identify which field is appropriate in various
situations, and also be able to use the `max_length`, `blank`, `null`,
and `default` attributes.

You should be able to model complex relationships in web application
state using `ForeignKey` relationships, including choosing `on_delete`
behavior.

You should be able to create, save, and query Django model objects.
Specifically, you should know the following query operators:

- `filter`, `exclude`, `union`, `intersection`, and `distinct`
- `order_by` and `reverse`
- `count` and `aggregate`
- `first` and `last`
- `contains` and `exists`

You should be able to explain the "1 + N" problem and be able to use
`select_related` to fix it.

You should be able to explain migrations, when they are created, when
they are run, and what problem they solved.

----------------------------------------------------

Topics below this line are not on the midterm, even if they were
covered in class before the midterm was assessed.

Views
-----

You should know the `for`, `if`, `with`, and `include` Django template
blocks. You should know the following Django template filters:

- `default`
- `floatformat`, `date`, `timesince`
- `join`, `length`, `pluralize`

You should know the syntax for defining URLs, including parameterized
URLs. You should know how to use the `render` function.

You should know how to catch errors raised by queries and how to
return 404 or other error pages.

You should know how to make a valid HTML form, including the `<form>`,
`<label>`, `<input>`, `<button>`, and `<output`> elements. You should
know what the `action`, `method`, and `enctype` parameters do on
forms, and be able explain the difference between the `get` and `post`
values for `method` and choose the right one for various forms. (You
are not expected to know what values to put for `enctype`, but you are
expected to know in what case you need to set a non-default
`enctype`.)

You should know the `type`, `id`, `name`, `value`, and `disabled`
attributes on input elements. You should know the following `type`s of
input elements:

- `text`, `number`, `password`, `hidden`
- `checkbox`, `radio`, `file`
- `date`, `time`, `email`, `tel`

You should be able to write a Django view function (controller) that
receives form data and saves it to the database. You should know how
to use the `request.GET`, `request.POST`, and `request.FILES`
dictionaries to access form data. You should be able to describe the
risks associated with file uploads.

You should be able to use the following input element attributes for
client-side validation:

- `required`
- `min` / `max`
- `minlength` / `maxlength`
- `pattern`
- `accept`

You should also be able to use `:valid` / `:invalid` to style HTML
forms.

You should be able to handle errors when validating form data in a
Django view function and be able to either re-display the form with an
error message or redirect the user when the form submits successfully.

Security
========

You should be able to describe a realistic threat model for a small
web application, including attackers, goals, and capabilities. You
should be able to suggest security policies for simple web
applications like the ones in your assignments.

You should be able to define both authorization and authentication.
You should be able to explain how cookies are used to create client
identity and how session data is stored by the server. You should be
able to describe simple security policies in terms of objects,
actions, users, and groups.

You should be able to use `request.session` and `request.user` in
Django controllers. You should be able to use the `authenticate`,
`login`, and `logout` functions for logging users in and out. You
should be able to test if a Django `User` is a member of a `Group` and
raise `PermissionDenied` if an authorization check fails.

You should be able to explain what an injection vulnerability is, and
what the benefits and risks are of using `|safe` or `.raw()` in
Django. You should be able to explain what CSRF is, what `{%
csrf_token %}` outputs, and what the risks are of using
`@csrf_exempt`. You should be able to explain what an open redirect
is, and what to look for in your code to find it. You should be able
to explain what CVEs are and what the OWASP top 10 are.

JavaScript
==========

You should be able to include JavaScript into an HTML page. You should
know the syntax of a `<script>` tag, how to write inline JS, and what
the `defer` and `async` parameters do. You should also know what
`type=module` does, at least at a high level (allows `import`,
separate namespace). You should be able to explain the idea of
progressive enhancement.

You should be comfortable with basic JavaScript syntax. You should
also know what to avoid: type mixing, accidental globals, `var`
declarations, `for` loops with undeclared or `var`-declared variables,
`for`/`in` loops, `function` inline functions. You should know
`Arrays.from` and the difference between arrays and array-like objects.
You should be able to identify bugs arising from the use of `this` and
be able to fix them by switching to arrow functions.

You should be able to use jQuery's `$` for wrapping, selecting, and
creating elements. You should be able to use the following jQuery APIs
for manipulating elements:

- `append`, `prepend`, `before`, `after`, `remove`, `replace`
- `addClass`, `removeClass`, `val`, `attr`
- `children`, `parent`, `find`, `next`, `previous`
- `text`
- `data`

You should be able to attach event handlers with jQuery's `on` method
and know the `target` field and `preventDefault` method on events.

You should know about the `$.ajax` function, including at least the
`method` and `data` fields in the options object. You should be able
to make asynchronous requests using the `success` callback. You should
be able to handle errors using the `error` callback. You should be
able to use `$.ajax` as a promise with `await`. You should be know how
to move `await` calls later in the code to enable more parallelism.

Deploy
------

You should know rough orders of magnitude for how many websites there
are and how many internet users there are. You should know how old the
internet and the web are (to within the decade). You should be able to
explain the difference between the internet and the web. You should be
able to list the most common web browsers.

You should be able to explain the relationship between hostnames (also
called domains), IP addresses, and packet routes. You should be able
to give examples of each. You should also be familiar with what kind
of information is provided by 1) DNS lookup tools; 2) IP lookup tools;
3) traceroute.

You should be able to explain the role of a registrar. You should know
what A and AAAA records do in DNS. You should be able to give the
price, within an order of magnitude, of a domain ($5-20/yr), an IPv4
address ($40-60), an IPv6 address ($0), inbound bandwidth ($0),
outbound traffic ($50-100/TB), and an HTTPS certificate ($0). You
should be able to explain why you need an IPv4 address.

You should be able to name the top three could providers. You should
be able to explain the difference between a "virtualized" and
"bare-metal" cloud computer. You should be able to name some key cloud
computing instance parameters, such as CPU architecture, CPU cores,
available memory, available disk, and available accelerators like
GPUs.

You should be able to explain the roles of AWS and its EC2 and Elastic
IP services. You should be give the cost, within an order of
magnitude, of the deployment you were asked to create as part of
Assignment 4 (about $9/mo). You should be able to explain the terms
"instance" and "instance type".

You should be able to define a Service Level Agreement and explain
what a "two nines" or "five nines" availability level means. You
should be able to explain the benefits of operating redundant services
in multiple regions.

You should be able describe briefly what Linux, SystemD, APT, SSH,
BASH, and JournalCtl do. You should be able to explain the role of the
gateway server and name popular gateway servers. You should be
able to explain the role of the database server and name popular
database servers.

You should be able to explain what the `DEBUG` and `ALLOWED_HOSTS`
settings in Django do and why they differ between development and
deployment.
