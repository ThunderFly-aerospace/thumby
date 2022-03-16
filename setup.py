from setuptools import find_packages, setup

setup(
    name='thumb-py',
    packages=find_packages(include=['thumby']),
    version='0.1.0',
    description='Simple python library for inserting .png thumbnails into gcode files.',
    author='Dusan Jansky',
    license='MIT',
    install_requires=['Pillow>=9.0.1'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
)

# TODO customise requirments