from pkg_resources import parse_version

# ==============================================================================


# yyyymmdd
__releasedate__ = '20190424'
# x.y.z or x.y.z.dev0 -- semver
__version__ = '0.0.3'
VERSION = parse_version(__version__)


# ==============================================================================


from .tag_tree_filter import *
