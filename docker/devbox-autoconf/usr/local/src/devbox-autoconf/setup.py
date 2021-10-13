from distutils.core import setup
setup(
    name='devbox-autoconf',
    version='0.1',
    description='Devbox web server configuration daemon',
    author='Tobias Umbach',
    author_email='umbach@men-at-work.de',
    packages=['devbox.autoconf'],
    install_requires=[
        'cerberus>=1.3',
        'inotify>=0.2',
        'pyyaml>=5.3',
    ],
    entry_points={
        'console_scripts': ['devbox-autoconf=devbox.autoconf.__main__:main']
    }
)
