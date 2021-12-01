# pypi
from pkg_resources import parse_version

# local
from .tag_tree_filter import clean_strip_content  # noqa: F401
from .tag_tree_filter import cleaner_factory__strip_content  # noqa: F401
from .tag_tree_filter import TAG_TREE_TAGS  # noqa: F401
from .tag_tree_filter import TagTreeFilter  # noqa: F401

# ==============================================================================


# yyyymmdd
__releasedate__ = "20211201"
# x.y.z or x.y.z.dev0 -- semver
__version__ = "0.1.3"
VERSION = parse_version(__version__)
