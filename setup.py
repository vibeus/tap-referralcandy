#!/usr/bin/env python
from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(
    name="tap-referralcandy",
    version="0.0.1",
    description="Singer.io tap for extracting ReferralCandy data",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Vibe Inc",
    url="http://github.com/vibeus/tap-referralcandy",
    classifiers=["Programming Language :: Python :: 3 :: Only"],
    py_modules=["tap_referralcandy"],
    install_requires=[
        "referral_candy",
        "requests",
        "singer-python",
    ],
    entry_points="""
    [console_scripts]
    tap-referralcandy=tap_referralcandy:main
    """,
    packages=["tap_referralcandy", "tap_referralcandy.streams"],
    package_data = {"schemas": ["tap_referralcandy/schemas/*.json"]},
    include_package_data=True,
)
