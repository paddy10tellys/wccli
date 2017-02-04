from setuptools import setup


setup(
    name="basic wordcounter",
    version='1.0',
    py_modules=['wordcounter'],
    include_package_data=True,
    install_requires=[
            'Click',
    ],
    entry_points='''
        [console_scripts]
        wordcounter=wordcounter:cli
    ''',
)
