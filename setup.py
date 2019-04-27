import setuptools

geom_classifiers = [
    'Development Status :: 1 - Planning',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: Python :: 3 :: Only',
    'Topic :: Utilities']

geom_long_description = None
with open('README.rst', 'r') as fp:
    geom_long_description = fp.read()
assert(geom_long_description is not None)

setuptools.setup(
    name='geom',
    version='0.1',
    license='MIT',
    description='Useful functions and classes for geometry',
    author='Josie Thompson',
    author_email='josiahst@gmail.com',
    long_description=geom_long_description,
    long_description_content_type="text/x-rst",
    url='https://github.com/josiest/geom',
    py_modules=['geom'],
    classifiers=geom_classifiers)
