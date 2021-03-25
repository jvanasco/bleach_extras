from pkg_resources import parse_version

# ==============================================================================


# yyyymmdd
__releasedate__ = "20210325"
# x.y.z or x.y.z.dev0 -- semver
__version__ = "0.1.2"
VERSION = parse_version(__version__)


# ==============================================================================


from .tag_tree_filter import *
