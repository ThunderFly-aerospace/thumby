from setuptools import setup


with open('README.md', 'r') as freadme:
    long_description = freadme.read()

setup(
    name='thumby',
    version='0.2.3',
    url='https://github.com/ThunderFly-aerospace/thumby/',
    author='Dusan Jansky',
    description='Simple python library for inserting .png thumbnails into gcode files.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=['thumby'],
    package_dir={'':'src'},
    license='MIT',
    install_requires=['Pillow>=9.0.1'],
    extras_require = {
        'dev': [
            'pytest-runner',
            'pytest',
        ],
    },
)
