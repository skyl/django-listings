from setuptools import setup, find_packages

version = '0.1'

LONG_DESCRIPTION = """
=====================================
django-listings
=====================================

Simple reusable app for Django (http://djangoproject.com )
that allows for the creation of classifieds like a job board.

"""

setup(
    name='django-listings',
    version=version,
    description="django-listings",
    long_description=LONG_DESCRIPTION,
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: Django",
        "Environment :: Web Environment",
    ],
    keywords='django,pinax,classfieds',
    author='Skylar Saveland',
    author_email='skylar.saveland@gmail.com',
    url='http://github.com/skyl/django-listings',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    setup_requires=['setuptools_git'],
)


