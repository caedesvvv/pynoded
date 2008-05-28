try:
    from setuptools import setup, find_packages
except ImportError:
    import ez_setup
    ez_setup.use_setuptools()
    from setuptools import setup, find_packages

import os

#coz setuptools on linux can't figure it out
bi = "pygraph"
wdirs = []

for root, dirs, files in os.walk(bi):
    wd = root.split('/')
    wd = '.'.join(wd)
    wdirs.append(wd)
    if '.svn' in dirs:
            dirs.remove('.svn')

setup(
    name = "pygraph",
    version = "0.1",
    packages = ['pygraph'] + wdirs,
    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.xml','hellow.py'],
        'examples':['*.*'],
        },
    zip_safe = True,
    include_package_data = True,
    # metadata for upload to PyPI
    author = "Curro and Caedes",
    author_email = "caedes@sindominio.net",
    description = """Cairo based graph drawing library.""",
    long_description = """Cairo based graph drawing library.""",
    classifiers = filter(None,"""
Development Status :: 3 - Alpha
Environment :: Other Environment
Environment :: Win32 (MS Windows)
Environment :: X11 Applications :: GTK
Intended Audience :: End Users/Desktop
License :: OSI Approved :: Mozilla Public License 1.0 (MPL)
Operating System :: Microsoft :: Windows
Operating System :: OS Independent
Operating System :: POSIX :: Linux
Programming Language :: Python
Topic :: Desktop Environment
Topic :: Multimedia :: Graphics
Topic :: Software Development :: User Interfaces
""".split("\n")),
    platforms = ["any"],
    requires = ["cairo",'pycairo','pango'],
    license = "GPL",
    keywords = "GUI Graph cairo",
    url = "http://delcorp.org",   # project home page, if any
    download_url = "http://delcorp.org",
)
