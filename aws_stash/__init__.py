from pkg_resources import get_distribution, DistributionNotFound
try:
    __project_name__ = get_distribution(__name__).project_name
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    __project_name__ = __name__
    __version__ = 'unknown'
