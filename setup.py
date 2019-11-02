from setuptools import setup, find_packages

setup(
    name='pykasso',
    version='0.0.1 dev',
    description='Werkzeuge für die Kasse',
    author='Jan-Peer Grunwald',
    author_email='pekh@eufrutki.net',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'pykasso=pykasso.cli:cli'
        ]
    }
)
