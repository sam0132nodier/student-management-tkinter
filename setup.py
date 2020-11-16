"""Setup file for student-management-tkinter"""

import os.path
from setuptools import setup

# The directory containing this file
THIS = os.path.abspath(os.path.dirname(__file__))

# Read the text of the README file

with open(os.path.join(THIS, "README.md")) as fid:
	README = fid.read()

setup(
    name="student-management-tkinter",
    version="1.0",
    description="Store student information in the database",
    long_description="README",
    long_description_content_type="text/markdown",
    url="https://github.com/sam0132nodier/student-management-tkinter",
    author="Sam Nodier",
    author_email="sam0132nodier@gmail.com",
    license="MIT",
    classifiers=[
    	"Licence :: OSI Approved :: MIT License",
    	"Programming Language :: Python",
    	"Programming Language :: Python :: 3",
    ],
    packages=["student_management"]
    include_packages_data=True,
    install_requires=[
    	"tkinter", "sqlite3", "json", "datetime", "re", "uuid", "view_students_dialog", "add_students_dialog", "about_dialog", "webbrowser", "os", "sys",
    ],
    entry_points={"console_scripts": ["studentmanagement=student_management.__main__:main"]},
)