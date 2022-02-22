from setuptools import find_packages, setup

setup(
    name='thumb-py',
    packages=find_packages(include=['thumb-py']),
    version='0.1.0',
    description='Simple python library for inserting .png thumbnails into gcode files.',
    author='Dusan Jansky',
    license='MIT',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)

# TODO customise requirments