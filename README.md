**Beets - Lidarr Fields**
=========================

This is a plugin for [Beets](https://github.com/beetbox/beets).
It provides some template fields to customize your path formats in
a more [Lidarr](https://github.com/lidarr/Lidarr) way.
It works faster than using the built-in inline plugin because it
evaluates those fields only once per album (same value for all tracks).
Currently, this plugin provides three template fields:

* releasegroupartist  
  It refers to the "Release Group Artist" (or the first one if multiple)
  which is whom Lidarr links a release to.

* lidarralbum  
  Original album name, but with illegal characters replaced
  the same way Lidarr does it.
  
* audiodisctotal  
  Similar to beet's 'disctotal' field, only it ignores video medias like
  Blu-ray, DVD, etc.

*Plugin only lightly tested by me. Use at your own risk!*


**Install**
===========

To install it, use pip:

    pip install beets-lidarr-fields

or

    git clone https://github.com/rafaelparente/beets-lidarr-fields.git
    cd beets-lidarr-fields
    python setup.py install


**Configuration**
=================

Enable the plugin in beets' config.yaml

    plugins: lidarrfields

How to use it
-------------

Use it to build your path formats in beet's config.yaml,
like it's explained in the [Beets Docs](https://beets.readthedocs.io/en/stable/reference/pathformat.html).
To make it look like Lidarr's default format, set it like:

    paths:
        default: $releasegroupartist/$lidarralbum ($year)/%if{$audiodisctotal,$disc - }${track}. $title
        
    per_disc_numbering: yes

Be aware that the ``aunique`` template function will
(most likelly) **not** work on lidarralbum.