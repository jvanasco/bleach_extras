# pypi
from pkg_resources import parse_version

# local
from .tag_tree_filter import clean_strip_content
from .tag_tree_filter import cleaner_factory__strip_content
from .tag_tree_filter import TAG_TREE_TAGS
from .tag_tree_filter import TagTreeFilter

# ==============================================================================


# yyyymmdd
__releasedate__ = ""
# x.y.z or x.y.z.dev0 -- semver
__version__ = "0.2.2"
VERSION = parse_version(__version__)
