from setuptools import setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(name='simpleimdb',
    version='0.0.1',
    url='https://github.com/zoreu/simpleimdb',
    license='GPL',
    author='Joel Silva',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='joel_webmaster@live.com',
    keywords='simpleimdb',
    description=u'scrape imdb',
    packages=['simpleimdb'],
    install_requires=['beautifulsoup4==4.9.3','requests'],)