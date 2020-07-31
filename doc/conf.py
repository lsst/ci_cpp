"""Sphinx configuration file for an LSST stack package.

This configuration only affects single-package Sphinx documentation builds.
"""

from documenteer.sphinxconfig.stackconf import build_package_configs
import lsst.ci.cpp


_g = globals()
_g.update(build_package_configs(
    project_name='ci.cpp',
    version=lsst.ci.cpp.version.__version__))
