import os
from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, "README.md")).read()
README = README.split('\n\n', 1)[0] + "\n"

tests_require = [
    'pytest>=3.0.0',
]

install_requires = [
    'bleach',
]

setup(
    name='bleach_extras',
    author='Jonathan Vanasco',
    author_email='jonathan@findmeon.com',
    version='0.0.1',
    url='http://github.com/jvanasco/bleach_extras',
    license='MIT License',
    description='some extensions for bleach',
    long_description=README,
    zip_safe=False,
    keywords="",
    test_suite='tests',
    packages=find_packages(),
    include_package_data=True,
    package_data={'': ['README.md']},
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    install_requires=install_requires,
    tests_require=tests_require,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        "Intended Audience :: Developers",
    ]
)
