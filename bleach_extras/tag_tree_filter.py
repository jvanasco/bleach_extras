from bleach.html5lib_shim import Filter
from bleach.sanitizer import (
    ALLOWED_ATTRIBUTES,
    ALLOWED_PROTOCOLS,
    ALLOWED_STYLES,
    ALLOWED_TAGS,
    Cleaner,
)
from six import text_type


# ==============================================================================


TAG_TREE_TAGS = ('script', 'style', )


class TagTreeFilter(Filter):
    """
    To adjust the tags to strip or replacement text use a subclass:

        class CustomFilter1(bleach_extras.TagTreeFilter):
            tags_strip_content = ['script', 'style', 'iframe', ]

        class CustomFilter2(bleach_extras.TagTreeFilter):
            tag_replace_string = '&lt;unsafe/&gt;'
    """

    """a list of tags which should be stripped along with their content/children."""
    tags_strip_content = TAG_TREE_TAGS
    _tags_strip_content = None  # memoized on __init__

    """if defined in a subclass, a string to replace the content with."""
    tag_replace_string = None
    _tag_replace = None   # memoized on __init__

    def __init__(self, source):
        """
        Creates a TagTreeFilter instance.

        This instance will strip the tag and the content tree of tags appearing
        in ``tags_strip_content``.

        :arg Treewalker source: stream
        """
        if not self.tags_strip_content:
            raise ValueError('must have `tags_strip_content` on the class')
        self._tags_strip_content = [t.lower() for t in self.tags_strip_content]
        if self.tag_replace_string is not None:
            self._tag_replace = {'data': text_type(self.tag_replace_string),
                                 'type': 'Characters',
                                 }
        self._in_strip_content = 0
        return super(TagTreeFilter, self).__init__(source)

    def __iter__(self):
        for token in Filter.__iter__(self):
            _name = token.get('name', '').lower()
            if _name in self._tags_strip_content:
                if token.get('type') == 'StartTag':
                    self._in_strip_content += 1
                elif token.get('type') == 'EndTag':
                    self._in_strip_content -= 1
                continue
            if self._in_strip_content:
                if self._tag_replace:
                    if (self._in_strip_content):
                        yield self._tag_replace
                continue
            yield token


def clean_strip_content(
    text, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES,
    styles=ALLOWED_STYLES, protocols=ALLOWED_PROTOCOLS, strip=False,
    strip_comments=True, filters=None,
):
    """Clean an HTML fragment of malicious content and return it

    This function is paired to `bleach.clean` and the only intended difference
    is to support the concept of stripping the content of tags, and not just the
    tag itself.

    # The below docstrings were taken from bleach https://github.com/mozilla/bleach
    # bleach is covered by the Apache License, Version 2.0

    .. Note::

       If you're cleaning a lot of text and passing the same argument values or
       you want more configurability, consider using a
       :py:class:`bleach.sanitizer.Cleaner` instance.

    :arg str text: the text to clean

    :arg list tags: allowed list of tags; defaults to
        ``bleach.sanitizer.ALLOWED_TAGS``

    :arg dict attributes: allowed attributes; can be a callable, list or dict;
        defaults to ``bleach.sanitizer.ALLOWED_ATTRIBUTES``

    :arg list styles: allowed list of css styles; defaults to
        ``bleach.sanitizer.ALLOWED_STYLES``

    :arg list protocols: allowed list of protocols for links; defaults
        to ``bleach.sanitizer.ALLOWED_PROTOCOLS``

    :arg bool strip: whether or not to strip disallowed elements

    :arg bool strip_comments: whether or not to strip HTML comments

    :arg list filters: list of html5lib Filter classes to pass streamed content through
        If ``None``, an instance of ``TagTreeFilter`` will be used; otherwise at
        least one element in the list must be ``TagTreeFilter`` or a subclass of it.

        .. seealso:: http://html5lib.readthedocs.io/en/latest/movingparts.html#filters

        .. Warning::

           Using filters changes the output of ``bleach.Cleaner.clean``.
           Make sure the way the filters change the output are secure.

    To adjust the tags to strip, submit subclasses of ``TagTreeFilter`` to ``filters``.

    :returns: cleaned text as unicode

    """
    cleaner = cleaner_factory__strip_content(
        tags=tags, attributes=attributes,
        styles=styles, protocols=protocols, strip=strip,
        strip_comments=strip_comments, filters=filters,
    )
    return cleaner.clean(text)


def cleaner_factory__strip_content(
    tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES,
    styles=ALLOWED_STYLES, protocols=ALLOWED_PROTOCOLS, strip=False,
    strip_comments=True, filters=None,
):
    """Factory for building a ``bleach.Cleaner`` instance designed to strip content.

    The accepts the same arguments as ``clean_strip_content`` except for the
    initial `text` argument.

    :returns: ``bleach.Cleaner`` instance
    """
    # whitelist the tags we want to strip, so they can be filtered out
    tags = [t.lower() for t in tags]
    # ensure we apply the `TagTreeFilter` defined above
    if filters is None:
        filters = [TagTreeFilter, ]
    # then adjust the tags based on the `tags_strip_content` of subclasses
    _has_approved_filter = False
    for f in filters:
        if isinstance(f, TagTreeFilter) or issubclass(f, TagTreeFilter):
            _has_approved_filter = True
            for t in f.tags_strip_content:
                t = t.lower()  # handle this as lowercase
                if t not in tags:
                    tags.append(t)
    if not _has_approved_filter:
        raise ValueError("You must submit `TagTreeFilter` or a subclass as `filters`.")
    cleaner = Cleaner(
        tags=tags,
        attributes=attributes,
        styles=styles,
        protocols=protocols,
        strip=strip,
        strip_comments=strip_comments,
        filters=filters,
    )
    return cleaner


__all__ = ('TAG_TREE_TAGS',
           'TagTreeFilter',
           'clean_strip_content',
           'cleaner_factory__strip_content',
           )
