# pypi
from bleach.sanitizer import Cleaner

# local
from bleach_extras import clean_strip_content
from bleach_extras import cleaner_factory__strip_content
from bleach_extras import TAG_TREE_TAGS
from bleach_extras import TagTreeFilter

# ==============================================================================


class FilterTagTreeFilter_SCRIPT(TagTreeFilter):
    tags_strip_content = [
        "SCRIPT",
    ]


class FilterTagTreeFilter_StYLe(TagTreeFilter):
    tags_strip_content = [
        "StYLe",
    ]


class FilterTagTreeFilter_PlusiFrame(TagTreeFilter):
    tags_strip_content = list(TagTreeFilter.tags_strip_content) + [
        "iframe",
    ]


class FilterTagTreeFilter_iFrame(TagTreeFilter):
    tags_strip_content = [
        "iframe",
    ]


class FilterTagTreeFilter_Unsafe(TagTreeFilter):
    tag_replace_string = "&lt;unsafe garbage/&gt;"


# ------------------------------------------------------------------------------


def test_factory():
    cleaner = cleaner_factory__strip_content()
    assert isinstance(cleaner, Cleaner)
    for tag in TAG_TREE_TAGS:
        assert tag in cleaner.tags
    assert TagTreeFilter in cleaner.filters
    assert len(cleaner.filters) == 1
    # run it twice
    assert cleaner.clean("<div>foo</div>") == "&lt;div&gt;foo&lt;/div&gt;"
    assert cleaner.clean("<div>foo</div>") == "&lt;div&gt;foo&lt;/div&gt;"


def test_interface_options():

    _input = 'foo.<div>bar.<script type="text/javascript">alert(1);<div>alpha.<style><div>beta.</style></div></script>bang.</div>biz'

    _input_iframe = 'foo.<div>bar.<script type="text/javascript">alert(1);<div>alpha.<style><div>beta.</style></div></script>bang.<iframe>IFRAME</iframe></div>biz'

    assert (
        clean_strip_content(
            _input,
            tags=[
                "div",
            ],
        )
        == cleaner_factory__strip_content(
            tags=[
                "div",
            ],
        ).clean(_input)
        == "foo.<div>bar.bang.</div>biz"
    )
    assert (
        clean_strip_content(
            _input,
            tags=["div", "script", "style"],
        )
        == cleaner_factory__strip_content(
            tags=[
                "div",
                "script",
                "style",
            ],
        ).clean(_input)
        == "foo.<div>bar.bang.</div>biz"
    )
    assert (
        clean_strip_content(
            _input,
            tags=["div", "script", "style"],
            filters=[
                TagTreeFilter,
            ],
        )
        == cleaner_factory__strip_content(
            tags=[
                "div",
                "script",
                "style",
            ],
            filters=[
                TagTreeFilter,
            ],
        ).clean(_input)
        == "foo.<div>bar.bang.</div>biz"
    )
    assert (
        clean_strip_content(
            _input,
            tags=[
                "div",
            ],
            filters=[
                FilterTagTreeFilter_PlusiFrame,
            ],
        )
        == cleaner_factory__strip_content(
            tags=[
                "div",
            ],
            filters=[
                FilterTagTreeFilter_PlusiFrame,
            ],
        ).clean(_input)
        == "foo.<div>bar.bang.</div>biz"
    )
    assert (
        clean_strip_content(
            _input,
            tags=[
                "div",
            ],
            filters=[
                FilterTagTreeFilter_iFrame,
            ],
        )
        == cleaner_factory__strip_content(
            tags=[
                "div",
            ],
            filters=[
                FilterTagTreeFilter_iFrame,
            ],
        ).clean(_input)
        == 'foo.<div>bar.&lt;script type="text/javascript"&gt;alert(1);<div>alpha.&lt;style&gt;<div>beta.&lt;/style&gt;</div>&lt;/script&gt;bang.</div>biz</div>'
    )

    # what about nonstandard tags?
    assert (
        clean_strip_content(
            _input_iframe,
            tags=["div", "script", "style"],
            filters=[
                TagTreeFilter,
            ],
        )
        == cleaner_factory__strip_content(
            tags=[
                "div",
                "script",
                "style",
            ],
            filters=[
                TagTreeFilter,
            ],
        ).clean(_input_iframe)
        == "foo.<div>bar.bang.&lt;iframe&gt;IFRAME&lt;/iframe&gt;</div>biz"
    )
    assert (
        clean_strip_content(
            _input_iframe,
            tags=["div", "script", "style"],
            filters=[
                FilterTagTreeFilter_PlusiFrame,
            ],
        )
        == cleaner_factory__strip_content(
            tags=[
                "div",
                "script",
                "style",
            ],
            filters=[
                FilterTagTreeFilter_PlusiFrame,
            ],
        ).clean(_input_iframe)
        == "foo.<div>bar.bang.</div>biz"
    )

    # Starting in bleach 3.1.1, html entities within <script> tags are escaped>
    # - "foo.<div>bar.<script>alert(1);<div>alpha.<style><div>beta.</style></div></script>bang.</div>biz"
    # + "foo.<div>bar.<script>alert(1);&lt;div&gt;alpha.&lt;style&gt;&lt;div&gt;beta.&lt;/style&gt;&lt;/div&gt;</script>bang.</div>biz"
    assert (
        clean_strip_content(
            _input_iframe,
            tags=["div", "script", "style"],
            filters=[
                FilterTagTreeFilter_iFrame,
            ],
        )
        == cleaner_factory__strip_content(
            tags=[
                "div",
                "script",
                "style",
            ],
            filters=[
                FilterTagTreeFilter_iFrame,
            ],
        ).clean(_input_iframe)
        == "foo.<div>bar.<script>alert(1);&lt;div&gt;alpha.&lt;style&gt;&lt;div&gt;beta.&lt;/style&gt;&lt;/div&gt;</script>bang.</div>biz"
    )
    assert (
        clean_strip_content(
            _input_iframe,
            tags=[
                "div",
            ],
            filters=[
                FilterTagTreeFilter_iFrame,
            ],
        )
        == cleaner_factory__strip_content(
            tags=[
                "div",
            ],
            filters=[
                FilterTagTreeFilter_iFrame,
            ],
        ).clean(_input_iframe)
        == 'foo.<div>bar.&lt;script type="text/javascript"&gt;alert(1);<div>alpha.&lt;style&gt;<div>beta.&lt;/style&gt;</div>&lt;/script&gt;bang.</div>biz</div>'
    )
    assert (
        clean_strip_content(
            _input_iframe,
            tags=["div", "script", "style"],
            filters=[
                TagTreeFilter,
                FilterTagTreeFilter_iFrame,
            ],
        )
        == cleaner_factory__strip_content(
            tags=[
                "div",
                "script",
                "style",
            ],
            filters=[
                TagTreeFilter,
                FilterTagTreeFilter_iFrame,
            ],
        ).clean(_input_iframe)
        == "foo.<div>bar.bang.</div>biz"
    )


def test_strip_tags():

    # this is flat
    _input_1 = 'foo.<div>bar.<script type="text/javascript">alert(1);</script>bar2.<script>alert(2);</script>bar3.<style>.body{}</style>bar4.<style tyle="text/css">.body{}</style>bar5.</div>biz'

    assert (
        clean_strip_content(
            _input_1,
            tags=[
                "div",
            ],
        )
        == cleaner_factory__strip_content(
            tags=[
                "div",
            ],
        ).clean(_input_1)
        == "foo.<div>bar.bar2.bar3.bar4.bar5.</div>biz"
    )
    assert (
        clean_strip_content(
            _input_1,
            tags=[
                "div",
            ],
            filters=[
                TagTreeFilter,
            ],
        )
        == cleaner_factory__strip_content(
            tags=[
                "div",
            ],
            filters=[
                TagTreeFilter,
            ],
        ).clean(_input_1)
        == "foo.<div>bar.bar2.bar3.bar4.bar5.</div>biz"
    )

    assert (
        clean_strip_content(
            _input_1,
            tags=[
                "div",
            ],
            strip=True,
        )
        == cleaner_factory__strip_content(
            tags=[
                "div",
            ],
            strip=True,
        ).clean(_input_1)
        == "foo.<div>bar.bar2.bar3.bar4.bar5.</div>biz"
    )
    assert (
        clean_strip_content(
            _input_1,
            tags=[
                "div",
            ],
            filters=[
                TagTreeFilter,
            ],
            strip=True,
        )
        == cleaner_factory__strip_content(
            tags=[
                "div",
            ],
            filters=[
                TagTreeFilter,
            ],
            strip=True,
        ).clean(_input_1)
        == "foo.<div>bar.bar2.bar3.bar4.bar5.</div>biz"
    )

    # `style` is escaped, because it is not stripped or allowed
    assert (
        clean_strip_content(
            _input_1,
            tags=[
                "div",
            ],
            filters=[
                FilterTagTreeFilter_SCRIPT,
            ],
        )
        == cleaner_factory__strip_content(
            tags=[
                "div",
            ],
            filters=[
                FilterTagTreeFilter_SCRIPT,
            ],
        ).clean(_input_1)
        == 'foo.<div>bar.bar2.bar3.&lt;style&gt;.body{}&lt;/style&gt;bar4.&lt;style tyle="text/css"&gt;.body{}&lt;/style&gt;bar5.</div>biz'
    )

    # the `stle` content becomes plaintext
    assert (
        clean_strip_content(
            _input_1,
            tags=[
                "div",
            ],
            filters=[
                FilterTagTreeFilter_SCRIPT,
            ],
            strip=True,
        )
        == cleaner_factory__strip_content(
            tags=[
                "div",
            ],
            filters=[
                FilterTagTreeFilter_SCRIPT,
            ],
            strip=True,
        ).clean(_input_1)
        == "foo.<div>bar.bar2.bar3..body{}bar4..body{}bar5.</div>biz"
    )

    assert (
        clean_strip_content(
            _input_1,
            tags=[
                "div",
            ],
            filters=[
                FilterTagTreeFilter_StYLe,
            ],
        )
        == cleaner_factory__strip_content(
            tags=[
                "div",
            ],
            filters=[
                FilterTagTreeFilter_StYLe,
            ],
        ).clean(_input_1)
        == 'foo.<div>bar.&lt;script type="text/javascript"&gt;alert(1);&lt;/script&gt;bar2.&lt;script&gt;alert(2);&lt;/script&gt;bar3.bar4.bar5.</div>biz'
    )

    # the `script` content becomes plaintext
    assert (
        clean_strip_content(
            _input_1,
            tags=[
                "div",
            ],
            filters=[
                FilterTagTreeFilter_StYLe,
            ],
            strip=True,
        )
        == cleaner_factory__strip_content(
            tags=[
                "div",
            ],
            filters=[
                FilterTagTreeFilter_StYLe,
            ],
            strip=True,
        ).clean(_input_1)
        == "foo.<div>bar.alert(1);bar2.alert(2);bar3.bar4.bar5.</div>biz"
    )

    # nested, nested+malformed
    _input_2 = 'foo.<div>bar.<script type="text/javascript">alert(1);<div>alpha.<style><div>beta.</style></div></script>bang.</div>biz'
    _input_2_b = 'foo.<div>bar.<script type="text/javascript">alert(1);<div>alpha.<style><div>beta.</style></div>bang.</div>biz'

    assert (
        clean_strip_content(
            _input_2,
            tags=[
                "div",
            ],
            filters=[
                FilterTagTreeFilter_SCRIPT,
            ],
        )
        == cleaner_factory__strip_content(
            tags=[
                "div",
            ],
            filters=[
                FilterTagTreeFilter_SCRIPT,
            ],
        ).clean(_input_2)
        == "foo.<div>bar.bang.</div>biz"
    )
    assert (
        clean_strip_content(
            _input_2_b,
            tags=[
                "div",
            ],
            filters=[
                FilterTagTreeFilter_SCRIPT,
            ],
        )
        == cleaner_factory__strip_content(
            tags=[
                "div",
            ],
            filters=[
                FilterTagTreeFilter_SCRIPT,
            ],
        ).clean(_input_2_b)
        == "foo.<div>bar.</div>"
    )

    assert (
        clean_strip_content(
            _input_2,
            tags=[
                "div",
            ],
            filters=[
                FilterTagTreeFilter_SCRIPT,
            ],
            strip=True,
        )
        == cleaner_factory__strip_content(
            tags=[
                "div",
            ],
            filters=[
                FilterTagTreeFilter_SCRIPT,
            ],
            strip=True,
        ).clean(_input_2)
        == "foo.<div>bar.bang.</div>biz"
    )
    assert (
        clean_strip_content(
            _input_2_b,
            tags=[
                "div",
            ],
            filters=[
                FilterTagTreeFilter_SCRIPT,
            ],
            strip=True,
        )
        == cleaner_factory__strip_content(
            tags=[
                "div",
            ],
            filters=[
                FilterTagTreeFilter_SCRIPT,
            ],
            strip=True,
        ).clean(_input_2_b)
        == "foo.<div>bar.</div>"
    )


def test_tag_replace():

    # this is flat
    _input_1 = 'foo.<div>bar.<script type="text/javascript">alert(1);</script>bar2.<script>alert(2);</script>bar3.<style>.body{}</style>bar4.<style tyle="text/css">.body{}</style>bar5.</div>biz'

    assert (
        clean_strip_content(
            _input_1,
            tags=[
                "div",
            ],
        )
        == cleaner_factory__strip_content(
            tags=[
                "div",
            ],
        ).clean(_input_1)
        == "foo.<div>bar.bar2.bar3.bar4.bar5.</div>biz"
    )

    assert (
        clean_strip_content(
            _input_1,
            tags=[
                "div",
            ],
            filters=[FilterTagTreeFilter_Unsafe],
        )
        == cleaner_factory__strip_content(
            tags=[
                "div",
            ],
            filters=[
                FilterTagTreeFilter_Unsafe,
            ],
        ).clean(_input_1)
        == "foo.<div>bar.&amp;lt;unsafe garbage/&amp;gt;bar2.&amp;lt;unsafe garbage/&amp;gt;bar3.&amp;lt;unsafe garbage/&amp;gt;bar4.&amp;lt;unsafe garbage/&amp;gt;bar5.</div>biz"
    )

    assert (
        clean_strip_content(
            _input_1,
            tags=[
                "div",
            ],
            filters=[FilterTagTreeFilter_Unsafe],
            strip=True,
        )
        == cleaner_factory__strip_content(
            tags=[
                "div",
            ],
            filters=[
                FilterTagTreeFilter_Unsafe,
            ],
            strip=True,
        ).clean(_input_1)
        == "foo.<div>bar.&amp;lt;unsafe garbage/&amp;gt;bar2.&amp;lt;unsafe garbage/&amp;gt;bar3.&amp;lt;unsafe garbage/&amp;gt;bar4.&amp;lt;unsafe garbage/&amp;gt;bar5.</div>biz"
    )

    # this is nested
    _input_2 = 'foo.<div>bar.<script type="text/javascript">alert(1);<div>alpha.<style><div>beta.</style></div></script>bang.</div>biz'

    assert (
        clean_strip_content(
            _input_2,
            tags=[
                "div",
            ],
        )
        == cleaner_factory__strip_content(
            tags=[
                "div",
            ],
        ).clean(_input_2)
        == "foo.<div>bar.bang.</div>biz"
    )

    assert (
        clean_strip_content(
            _input_2,
            tags=[
                "div",
            ],
            filters=[FilterTagTreeFilter_Unsafe],
        )
        == cleaner_factory__strip_content(
            tags=[
                "div",
            ],
            filters=[
                FilterTagTreeFilter_Unsafe,
            ],
        ).clean(_input_2)
        == "foo.<div>bar.&amp;lt;unsafe garbage/&amp;gt;bang.</div>biz"
    )

    assert (
        clean_strip_content(
            _input_2,
            tags=[
                "div",
            ],
            filters=[FilterTagTreeFilter_Unsafe],
            strip=True,
        )
        == cleaner_factory__strip_content(
            tags=[
                "div",
            ],
            filters=[
                FilterTagTreeFilter_Unsafe,
            ],
            strip=True,
        ).clean(_input_2)
        == "foo.<div>bar.&amp;lt;unsafe garbage/&amp;gt;bang.</div>biz"
    )


def test_invalid():
    try:
        cleaner = cleaner_factory__strip_content(filters=[])
        raise RuntimeError("The command above should raise a ValueError")
    except ValueError as exc:  # noqa: F841
        # expects ValueError: You must submit `TagTreeFilter` or a subclass as `filters`.
        pass

    try:
        cleaner = cleaner_factory__strip_content(
            filters=[
                str,
            ]
        )
        raise RuntimeError("The command above raise a ValueError")
    except ValueError as exc:  # noqa: F841
        # expects ValueError: You must submit `TagTreeFilter` or a subclass as `filters`.
        pass
