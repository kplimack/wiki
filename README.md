wiki
====
Rewriting this from scratch again

Aboot
===
The goal of this wiki is to be as simple as possible.
A wiki really only needs one function (not counting the classes), it serves the requested page or it 404's.  Thanks to Django, we can do that very easily using <i>get_object_or_404</i> and <i>handler404</i>, where the <i>404 page</i> lets you create a new page.  We also need to know how to render pages look and feel.  Bootstrap will take care of that, we'll just render the links the way we want them.