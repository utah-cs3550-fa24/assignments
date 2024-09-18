Checklists
==========

This document has helpful checklists that help you develop various
parts of a web application. You won't ever be tested directly on the
checklist, but you will be tested on doing the task the checklist
helps with, and it's probably helpful to know and practice using each
checklist here.

Flex-box
--------

Start by drawing (or finding) a picture of what you want the final
layout to look like. As you go, you'll need to draw in additional
annotations on this picture.

Start at the outermost element. For a full-page layout, this is the
page as a whole (usually the `<body>` element); for a component it'll
be the element that contains the whole component. You'll work from the
outside in.

**Step 0: Diagramming.** Draw the boundaries of the current element.
Then, draw a rectangle around each item it contains. You should end up
with a width/height for each item and also some whitespace between
items.

**Step 1: Rows and columns.** Are the items arrange horizontally or
vertically? Use that to decide if the current element is a row or a
column. Assign `display: flex` and the appropriate `flex-direction`.

How many items are there? If the number of HTML child elements is
different, you'll need to add new wrapper elements (usually `<div>`s).

**Step 2: main direction lengths.** Next, figure out how long, in the
main direction, each item is. The "main direction" is horizontally for
rows and vertically for columns. A lot of elements will be "sized to
content", which is the default, but some might have fixed widths.
Assign the appropriate `width`/`height` property.

Then ask yourself whether each child can grow or shrink from this
size. Assign the appropriate `flex-grow` and `flex-shrink` value.

**Step 3: main direction whitespace.** Now figure out how big the
whitespace between items in the main direction should be.

First, assign the appropriate `gap` between items and `padding`
between those items and the container. This is the "default" or
"minimum" gap. Then ask yourself whether any gaps should be flexible
and change size with the container. If yes, also assign an appropriate
`justify-content` value.

In some cases you will want whitespace distributed in some unusual way
(such as, one third over here and two third over there). If this
happens, you need to return to step 0 and diagram the element
differently, usually grouping elements with wrappers.

**Step 4: other direction.** Now figure out how big each item should
be in the other direction (so, height inside row containers and width
inside column containers). The default is to stretch across the whole
container, but if it should be different, first set `align-items` to
determine where the whitespace goes and then `height`/`width` to
indicate centering / start / end.
