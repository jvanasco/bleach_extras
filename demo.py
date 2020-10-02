from future import __print_function__

import bleach
import bleach_extras

dangerous = """foo.<div>1<script>alert("ur komputer hs VIRUS! Giv me ur BITCOIN in 24 hours! Wallet is: abdefg!");</script>2</div>.bar"""

print(
    bleach.clean(
        dangerous,
        tags=[
            "div",
        ],
        strip=False,
    )
)
# foo.<div>1&lt;script&gt;alert("ur komputer hs VIRUS! Giv me ur BITCOIN in 24 hours! Wallet is: abdefg!");&lt;/script&gt;2</div>.bar

print(
    bleach.clean(
        dangerous,
        tags=[
            "div",
        ],
        strip=True,
    )
)
# foo.<div>1alert("ur komputer hs VIRUS! Giv me ur BITCOIN in 24 hours! Wallet is: abdefg!");2</div>.bar

print(
    bleach_extras.clean_strip_content(
        dangerous,
        tags=["div"],
    )
)
# foo.<div>12</div>.bar

cleaner = bleach_extras.cleaner_factory__strip_content(
    tags=["div"],
)
print(cleaner.clean(dangerous))
# foo.<div>12</div>.bar

print(
    bleach_extras.clean_strip_content(
        dangerous,
        tags=[
            "div",
        ],
        strip=True,
    )
)
# foo.<div>12</div>.bar


dangerous = dangerous + "<iframe>IFRAME</iframe>"


class FilterTagTreeFilter_script_style(bleach_extras.TagTreeFilter):
    tags_strip_content = [
        "script",
        "style",
    ]


class FilterTagTreeFilter_SCRIPT(bleach_extras.TagTreeFilter):
    tags_strip_content = [
        "SCRIPT",
    ]


class FilterTagTreeFilter_SCRIPT_iframe(bleach_extras.TagTreeFilter):
    tags_strip_content = [
        "SCRIPT",
        "iframe",
    ]


class IFrameFilter(bleach_extras.TagTreeFilter):
    tags_strip_content = ("script", "style", "iframe")


print(
    bleach_extras.clean_strip_content(
        dangerous,
        tags=[
            "div",
        ],
        filters=[
            FilterTagTreeFilter_script_style,
        ],
        strip=True,
    )
)
print(
    bleach_extras.clean_strip_content(
        dangerous,
        tags=[
            "div",
        ],
        filters=[
            FilterTagTreeFilter_SCRIPT,
        ],
        strip=True,
    )
)
print(
    bleach_extras.clean_strip_content(
        dangerous,
        tags=[
            "div",
        ],
        filters=[
            FilterTagTreeFilter_SCRIPT,
        ],
        strip=False,
    )
)
print(
    bleach_extras.clean_strip_content(
        dangerous,
        tags=[
            "div",
        ],
        filters=[
            FilterTagTreeFilter_SCRIPT_iframe,
        ],
        strip=False,
    )
)
print(
    bleach_extras.clean_strip_content(
        dangerous,
        tags=[
            "div",
        ],
        filters=[
            IFrameFilter,
        ],
        strip=False,
    )
)
print(
    bleach_extras.clean_strip_content(
        dangerous,
        tags=[
            "div",
        ],
        filters=[
            IFrameFilter,
        ],
        strip=True,
    )
)

dangerous2 = """foo.<div>1<script>alert("ur komputer hs VIRUS! Giv me ur BITCOIN in 24 hours! Wallet is: abdefg!");<iframe>iiffrraammee</iframe></script>2</div>.bar"""


class IFrameFilter2(bleach_extras.TagTreeFilter):
    tags_strip_content = ("script", "style", "iframe")
    tag_replace_string = "&lt;unsafe/&gt;"


print(
    bleach_extras.clean_strip_content(
        dangerous2,
        tags=[
            "div",
        ],
        filters=[
            IFrameFilter2,
        ],
    )
)
print(
    bleach_extras.clean_strip_content(
        dangerous2,
        tags=[
            "div",
        ],
        filters=[
            IFrameFilter2,
        ],
        strip=True,
    )
)
