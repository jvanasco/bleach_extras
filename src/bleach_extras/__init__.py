# pypi
from packaging.version import parse as parse_version

# local
from .tag_tree_filter import clean_strip_content  # noqa: F401
from .tag_tree_filter import cleaner_factory__strip_content  # noqa: F401
from .tag_tree_filter import TAG_TREE_TAGS  # noqa: F401
from .tag_tree_filter import TagTreeFilter  # noqa: F401

# ==============================================================================


# yyyymmdd
__releasedate__ = "20261027"
# x.y.z or x.y.z.dev0 -- semver
__version__ = "1.0.0"
VERSION = parse_version(__version__)
