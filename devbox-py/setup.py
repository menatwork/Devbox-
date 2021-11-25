from distutils.core import setup
setup(
    name='devbox',
    version='0.1',
    description='Python Devbox tooling',
    author='Tobias Umbach',
    author_email='umbach@men-at-work.de',
    packages=['devbox.autoconf'],
    install_requires=[
        'cerberus>=1.3',
        'inotify>=0.2',
        'jinja2>=2.10',
        'toml>=0.10',
        'Flask>=2.0',
    ],
    entry_points={
        'console_scripts': [
            'devbox-autoconf=devbox.autoconf.__main__:main',
        ]
    }
)