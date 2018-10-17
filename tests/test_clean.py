from bleach_extras import clean_strip_content
from bleach_extras import TagTreeFilter
from bleach_extras import cleaner_factory__strip_content
from bleach_extras import TAG_TREE_TAGS
from bleach.sanitizer import Cleaner


# ==============================================================================


class FilterTagTreeFilter_SCRIPT(TagTreeFilter):
    tags_strip_content = ['SCRIPT', ]

class FilterTagTreeFilter_StYLe(TagTreeFilter):
    tags_strip_content = ['StYLe', ]

class FilterTagTreeFilter_PlusiFrame(TagTreeFilter):
    tags_strip_content = list(TagTreeFilter.tags_strip_content) + ['iframe', ]

class FilterTagTreeFilter_iFrame(TagTreeFilter):
    tags_strip_content = ['iframe', ]

class FilterTagTreeFilter_Unsafe(TagTreeFilter):
    tag_replace_string = "&lt;unsafe/&gt;"


# ==============================================================================


def test_factory():
    factory = cleaner_factory__strip_content()
    assert isinstance(factory, Cleaner)
    for tag in TAG_TREE_TAGS:
        assert tag in factory.tags
    assert TagTreeFilter in factory.filters
    assert len(factory.filters) == 1


def test_interface_options():

    _input = 'foo.<div>bar.<script type="text/javascript">alert(1);<div>alpha.<style><div>beta.</style></div></script>bang.</div>biz'

    _input_iframe = 'foo.<div>bar.<script type="text/javascript">alert(1);<div>alpha.<style><div>beta.</style></div></script>bang.<iframe>IFRAME</iframe></div>biz'

    assert (clean_strip_content(_input, tags=['div', ], ) ==
            'foo.<div>bar.bang.</div>biz'
            )
    assert (clean_strip_content(_input, tags=['div', 'script', 'style'], ) ==
            'foo.<div>bar.bang.</div>biz'
            )
    assert (clean_strip_content(_input, tags=['div', 'script', 'style'], filters=[TagTreeFilter, ]) ==
            'foo.<div>bar.bang.</div>biz'
            )

    # what about nonstandard tags?
    assert (clean_strip_content(_input_iframe, tags=['div', 'script', 'style'], filters=[TagTreeFilter, ]) ==
            'foo.<div>bar.bang.&lt;iframe&gt;IFRAME&lt;/iframe&gt;</div>biz'
            )
    assert (clean_strip_content(_input_iframe, tags=['div', 'script', 'style'], filters=[FilterTagTreeFilter_PlusiFrame, ]) ==
            'foo.<div>bar.bang.</div>biz'
            )
    assert (clean_strip_content(_input_iframe, tags=['div', 'script', 'style'], filters=[FilterTagTreeFilter_iFrame, ]) ==
            'foo.<div>bar.<script>alert(1);<div>alpha.<style><div>beta.</style></div></script>bang.</div>biz'
            )
    assert (clean_strip_content(_input_iframe, tags=['div', ], filters=[FilterTagTreeFilter_iFrame, ]) ==
            'foo.<div>bar.&lt;script type="text/javascript"&gt;alert(1);<div>alpha.&lt;style&gt;<div>beta.&lt;/style&gt;</div>&lt;/script&gt;bang.</div>biz</div>'
            )
    assert (clean_strip_content(_input_iframe, tags=['div', 'script', 'style'], filters=[TagTreeFilter, FilterTagTreeFilter_iFrame, ]) ==
            'foo.<div>bar.bang.</div>biz'
            )

    assert (clean_strip_content(_input, tags=['div', ], filters=[FilterTagTreeFilter_PlusiFrame, ]) ==
            'foo.<div>bar.bang.</div>biz'
            )
    assert (clean_strip_content(_input, tags=['div', ], filters=[FilterTagTreeFilter_iFrame, ]) ==
            'foo.<div>bar.&lt;script type="text/javascript"&gt;alert(1);<div>alpha.&lt;style&gt;<div>beta.&lt;/style&gt;</div>&lt;/script&gt;bang.</div>biz</div>'
            )


def test_strip_tags():

    # this is flat
    _input_1 = 'foo.<div>bar.<script type="text/javascript">alert(1);</script>bar2.<script>alert(2);</script>bar3.<style>.body{}</style>bar4.<style tyle="text/css">.body{}</style>bar5.</div>biz'

    assert (clean_strip_content(_input_1, tags=['div', ]) ==
            'foo.<div>bar.bar2.bar3.bar4.bar5.</div>biz'
            )
    assert (clean_strip_content(_input_1, tags=['div', ], filters=[TagTreeFilter, ]) ==
            'foo.<div>bar.bar2.bar3.bar4.bar5.</div>biz'
            )

    assert (clean_strip_content(_input_1, tags=['div', ], strip=True) ==
            'foo.<div>bar.bar2.bar3.bar4.bar5.</div>biz'
            )
    assert (clean_strip_content(_input_1, tags=['div', ], filters=[TagTreeFilter, ], strip=True) ==
            'foo.<div>bar.bar2.bar3.bar4.bar5.</div>biz'
            )

    # `style` is escaped, because it is not stripped or allowed
    assert (clean_strip_content(_input_1, tags=['div', ], filters=[FilterTagTreeFilter_SCRIPT, ], ) ==
            'foo.<div>bar.bar2.bar3.&lt;style&gt;.body{}&lt;/style&gt;bar4.&lt;style tyle="text/css"&gt;.body{}&lt;/style&gt;bar5.</div>biz'
            )
            
    # the `stle` content becomes plaintext
    assert (clean_strip_content(_input_1, tags=['div', ], filters=[FilterTagTreeFilter_SCRIPT, ], strip=True) ==
            'foo.<div>bar.bar2.bar3..body{}bar4..body{}bar5.</div>biz'
            )

    assert (clean_strip_content(_input_1, tags=['div', ], filters=[FilterTagTreeFilter_StYLe, ]) ==
            'foo.<div>bar.&lt;script type="text/javascript"&gt;alert(1);&lt;/script&gt;bar2.&lt;script&gt;alert(2);&lt;/script&gt;bar3.bar4.bar5.</div>biz'
            )

    # the `script` content becomes plaintext
    assert (clean_strip_content(_input_1, tags=['div', ], filters=[FilterTagTreeFilter_StYLe, ], strip=True) ==
            'foo.<div>bar.alert(1);bar2.alert(2);bar3.bar4.bar5.</div>biz'
            )

    # nested, nested+malformed
    _input_2 = 'foo.<div>bar.<script type="text/javascript">alert(1);<div>alpha.<style><div>beta.</style></div></script>bang.</div>biz'
    _input_2_b = 'foo.<div>bar.<script type="text/javascript">alert(1);<div>alpha.<style><div>beta.</style></div>bang.</div>biz'

    assert (clean_strip_content(_input_2, tags=['div', ], filters=[FilterTagTreeFilter_SCRIPT, ], ) ==
            'foo.<div>bar.bang.</div>biz'
            )
    assert (clean_strip_content(_input_2_b, tags=['div', ], filters=[FilterTagTreeFilter_SCRIPT, ], ) ==
            'foo.<div>bar.</div>'
            )

    assert (clean_strip_content(_input_2, tags=['div', ], filters=[FilterTagTreeFilter_SCRIPT, ], strip=True) ==
            'foo.<div>bar.bang.</div>biz'
            )
    assert (clean_strip_content(_input_2_b, tags=['div', ], filters=[FilterTagTreeFilter_SCRIPT, ], strip=True) ==
            'foo.<div>bar.</div>'
            )
