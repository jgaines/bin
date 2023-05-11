"""Inject qalib.pth file into the current python environment.

This should be run from within a virtual env to add the qalib.pth file into its
site-packages.
"""

import pathlib
import site

site_packages = site.getsitepackages()[0]

qalib_pth = pathlib.Path(site_packages) / 'qalib.pth'

if qalib_pth.exists():
    answer = input(f"{qalib_pth}\nalready exists, overwrite? ")
else:
    answer = input(f'Inject QA lib into {site_packages}? ')

if answer and answer[0] in 'yY':
    with qalib_pth.open('w') as pth:
        pth.write("/home/jgaines/git/eng-tools/qa/pylib")
