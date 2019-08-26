from setuptools import setup

setup(name="region_plot",
      version="0.1",
      author="Ahmet Cetinkaya",
      description="A function for plotting two-dimensional regions of points that satisfy a given predicate.",
      py_modules=["region_plot"],
      install_requires=["numpy", "matplotlib"])
