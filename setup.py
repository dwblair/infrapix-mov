#!/usr/bin/python
"""   
Setup script for 'infrapix' Python package and commandline tools.
Install with "python setup.py install".
"""
import platform, os, shutil

PACKAGE_METADATA = {
    'name'         : 'infrapix',
    'version'      : 'dev',
    'author'       : "Pioneer Valley Open Science",
    'author_email' : "https://github.com/Pioneer-Valley-Open-Science/infrapix/issues",
}
    
PACKAGE_SOURCE_DIR = 'src'
MAIN_PACKAGE_DIR   = 'infrapix'
MAIN_PACKAGE_PATH  = os.path.abspath(os.sep.join((PACKAGE_SOURCE_DIR,MAIN_PACKAGE_DIR)))
 
#dependencies
INSTALL_REQUIRES = [
                    'numpy >= 1.1.0',
                    'matplotlib >= 0.98',
                    ]

#scripts and plugins
ENTRY_POINTS = { 'gui_scripts': [],
                 'console_scripts': [
                                      'infrapix_render = infrapix.commands.render:main','infrapix_single = infrapix.commands.single:main',
                                    ],
                } 
 
if __name__ == "__main__":
    from setuptools import setup, find_packages    
    setup(package_dir      = {'':PACKAGE_SOURCE_DIR},
          packages         = find_packages(PACKAGE_SOURCE_DIR),
          install_requires = INSTALL_REQUIRES,
          entry_points     = ENTRY_POINTS,
          #non-code files
          package_data     =   {'': ['*.jpg']},
          **PACKAGE_METADATA
         )

