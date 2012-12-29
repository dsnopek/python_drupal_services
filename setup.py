
import ez_setup
ez_setup.use_setuptools()

from setuptools import setup

setup(
    name = "drupal_services",
    author = "David Snopek",
    author_email = "dsnopek@gmail.com",
    description = "Some simple Python classes for interacting with the Drupal 'services' module.",
    license = "MIT",
    version = "0.1.0",
    packages = ['drupal_services'],
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
)

