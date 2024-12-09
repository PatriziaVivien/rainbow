from setuptools import setup, find_packages
 
VERSION = '0.0.1'
DESCRIPTION = 'Python package with pre defined colors and custom color maps'
LONG_DESCRIPTION = 'Python package to create custom semi linar colormaps. Pre defined colormaps and colors are available.'
 
setup(
        name="chiliscustomcolors", # has to be the same as the folder name!
        version=VERSION,
        author="Patrizia Schoch",
        author_email="<patrizia.vivien@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['matplotlib', 'numpy', 'colorspacious'], # add all 
# packages that you use in your module (here, I added as 
# an example numpy and xarray - you should adapt this)
 
        keywords=['python'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent",
        ]
)
