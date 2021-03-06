#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/globocom/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com timehome@corp.globo.com

from setuptools import setup, Extension
from thumbor import __version__

import glob
import os


def filter_extension_module(name, lib_objs, lib_headers):
    return Extension(
        'thumbor.ext.filters.%s' % name,
        ['thumbor/ext/filters/%s.c' % name] + lib_objs,
        libraries=['m'],
        include_dirs=['thumbor/ext/filters/lib'],
        depends=['setup.py'] + lib_objs + lib_headers,
        extra_compile_args=['-Wall', '-Wextra', '-Werror', '-Wno-unused-parameter'])


def gather_filter_extensions():
    files = glob.glob('thumbor/ext/filters/_*.c')
    lib_objs = glob.glob('thumbor/ext/filters/lib/*.c')
    lib_headers = glob.glob('thumbor/ext/filters/lib/*.h')

    return [filter_extension_module(f[0:-2].split('/')[-1], lib_objs, lib_headers) for f in files]


def run_setup(extension_modules=[]):
    if not 'CFLAGS' in os.environ:
        os.environ['CFLAGS'] = ''
    setup(
        name='thumbor',
        version=__version__,
        description="thumbor is an open-source photo thumbnail service by globo.com",
        long_description="""
Thumbor is a smart imaging service. It enables on-demand crop, resizing and flipping of images.

It also features a VERY smart detection of important points in the image for better cropping and
resizing, using state-of-the-art face and feature detection algorithms (more on that in Detection Algorithms).

Using thumbor is very easy (after it is running). All you have to do is access it using an url for an image, like this:

http://<thumbor-server>/300x200/smart/s.glbimg.com/et/bb/f/original/2011/03/24/VN0JiwzmOw0b0lg.jpg
""",
        keywords='imaging face detection feature thumbnail imagemagick pil opencv',
        author='globo.com',
        author_email='timehome@corp.globo.com',
        url='https://github.com/globocom/thumbor/wiki',
        license='MIT',
        classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Natural Language :: English',
            'Operating System :: MacOS',
            'Operating System :: POSIX :: Linux',
            'Programming Language :: Python :: 2.6',
            'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
            'Topic :: Multimedia :: Graphics :: Presentation'
        ],
        packages=['thumbor'],
        package_dir={"thumbor": "thumbor"},
        include_package_data=True,
        package_data={
            '': ['*.xml'],
        },

        install_requires=[
            "tornado>=2.1.1,<2.2.0",
            "pyCrypto>=2.1.0",
            "pycurl>=7.19.0,<7.20.0",
            "Pillow>=1.7.5,<=2.0.0",
            "derpconf>=0.2.0",
            "python-magic>=0.4.3"
        ],

        entry_points={
            'console_scripts': [
                'thumbor=thumbor.server:main',
                'thumbor-url=thumbor.url_composer:main',
                'thumbor-config=thumbor.config:generate_config'
            ],
        },

        ext_modules=extension_modules
    )

try:
    run_setup(gather_filter_extensions())
except SystemExit as exit:
    print "\n\n*******************************************************************"
    print "Couldn't build one or more native extensions, skipping compilation.\n\n"
    run_setup()
