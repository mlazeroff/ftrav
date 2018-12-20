import setuptools

setuptools.setup(
    name='ftrav',
    license='GPL-3',
    version='0.1dev',
    author='Matthew Lazeroff',
    author_email='mdlazeroff@gmail.com',
    description='Utility for traversing and indexing directory contents',
    url='https://github.com/mlazeroff/ftrav',
    packages=['ftrav'],
    entry_points={'console_scripts': 'ftrav = ftrav.ftrav:main'},
    classifiers={'Programming Language :: Python :: 3',
                 'License :: OSI Approved :: GPL-3',
                 'Operating System :: Linux, OS-X, Windows'},
)