from setuptools import setup, find_packages
import os
from os.path import abspath, dirname, join

"""Remember that your package name should not be the same name as your project, otherwise python will run into namespace collision issues."""

root_path = abspath(dirname(__file__))

source_directory = None


package_name = None
package_version = None
maintainer = None
description = None
python_requirements = []
"""
Here are some example values for the above:
source_directory = 'caffe'
package_name = 'caffe_python'
package_version = 0.1.4-gpu'
maintainer = "James Sutton"
description = 'Wrapper package for caffe bindings'
python_requirements = ['cython>=0.19.2',
'numpy>=1.7.1',
'scipy>=0.13.2',
'scikit-image>=0.9.3',
'matplotlib>=1.3.1',
'ipython>=3.0.0',
'h5py>=2.2.0',
'leveldb>=0.191',
'networkx>=1.8.1',
'nose>=1.3.0',
'pandas>=0.12.0',
'python-dateutil>=1.4<2',
'protobuf==3.0.0b2.post1',
'python-gflags>=2.0',
'pyyaml>=3.10',
'Pillow>=2.3.0']
"""

package_data = {}

"""Initialize the package with a __init__ and a real folder, this can be handled by your builder script."""
try:
    os.mkdir(join(root_path, package_name))
    with open(join(join(root_path, package_name), '__init__.py'), 'w+') as f:
        f.write(" ")
except:
    pass


"""Let's bundle up all of the shared objects that your cmake/make operation creates, if they create them in a separate directory please adjust accordingly."""
if os.name == 'posix':
    package_data[package_name] = ['{}/*.so'.format(source_directory)]
else:
    package_data[package_name] = ['{}/*.pyd'.format(source_directory), '{}/*.dll'.format(source_directory)]

"""
If you have any python specific files or folders you would like to include in the python wheel, do so here:

package_data[package_name] += ['{}/algorithm_a.py'.format(source_directory), '{}/data_processing.py'.format(source_directory)]
"""

"""
If necessary, place your license(s) into your package here

package_data[package_name] += ['{}/LICENSE.txt'.format(source_directory), '{}/LICENSE-3RD-PARTY.txt'.format(source_directory)]
"""

package_data[''] = ['{}/*.xml'.format(source_directory)]

# This creates a list which is empty but returns a length of 1.
# Should make the wheel a binary distribution and platlib compliant.

class EmptyListWithLength(list):
    def __len__(self):
        return 1


setup(name=package_name,
      version=package_version,
      description=description,
      packages=find_packages(),
      package_data=package_data,
      include_package_data=True,
      ext_modules=EmptyListWithLength(),
      install_requires=python_requirements,
      zip_safe=False
      )

