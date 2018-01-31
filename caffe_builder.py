#!/usr/bin/python2

"""This is an example of how to compile a C++/python based project so that create_wheel.py
 can access the relevant files for easy wheel creation."""

import os
import sys
from os.path import join, exists, abspath, dirname
import subprocess
from distutils import ccompiler
import pip.download
from pip.req import parse_requirements

source_directory_name = 'source'

project_directory_name = 'caffe'
ROOT_DIR = abspath(dirname(__file__))
SOURCE_DIR = join(ROOT_DIR, source_directory_name)
DUMP_DIR = join(ROOT_DIR, project_directory_name)
BUILD_DIR = join(SOURCE_DIR, 'build')
PROTO_DIR = join(SOURCE_DIR, 'src/caffe/proto')
SRC_DIR = join(SOURCE_DIR, 'src')
LIB_DIR = join(SOURCE_DIR,'build/lib')

## These are caffe specific directories, replace with your own as necessary.
PY_DIR = join(SOURCE_DIR, 'python/caffe')
MOD_DIR = join(PY_DIR, 'proto')
SRC_GEN = [join(SRC_DIR, 'caffe/proto/caffe.pb.h'),
           join(SRC_DIR, 'caffe/proto/caffe.pb.cc')]



## Only necessary for systems that don't automatically have everything necessary for compilation,
# can be ignored in our case.

LIBDIRS = ['/usr/lib', '/usr/lib/x86_64-linux-gnu/']
LIBRARIES = ['cblas', 'blas', 'boost_thread', 'glog', 'gflags', 'protobuf',
             'boost_python', 'boost_system', 'boost_filesystem', 'm', 'hdf5_hl',
             'hdf5']


compiler = ccompiler.new_compiler()
for lib in LIBRARIES:
    if not compiler.find_library_file(LIBDIRS, lib):
        print('Could not find required library {}'.format(lib))
        print("Required libraries: {}".format(LIBRARIES))
        print("Required Ubuntu 14.04 packages: ")
        print("sudo apt-get install libprotobuf-dev libleveldb-dev python-dev "
              "libgflags-dev libgoogle-glog-dev liblmdb-dev libsnappy-dev "
              "libopencv-dev libhdf5-serial-dev protobuf-compiler "
              "libatlas-base-dev")
        print("sudo apt-get install --no-install-recommends libboost-all-dev")
        sys.exit(-1)


## Only necessary for caffe projects, or projects with protocol buffers, can be ignored.

# Create the proto module in python/caffe, from the caffe proto buffer

try:
    os.makedirs(MOD_DIR)
except OSError:
    pass


if not exists(join(MOD_DIR, 'caffe_pb2.py')):
    # Converts the caffe.proto protocol buffer into a python format
    subprocess.call(['protoc',
                     join(PROTO_DIR, 'caffe.proto'),
                     '--proto_path', PROTO_DIR,
                     '--python_out', MOD_DIR])

# Generates cc files from proto buffer
if (not exists(join(PROTO_DIR, 'caffe.pb.cc')) or
        not exists(join(PROTO_DIR, 'caffe.pb.h'))):
    # Converts the caffe.proto protocol buffer into a python format
    subprocess.call(['protoc',
                     join(PROTO_DIR, 'caffe.proto'),
                     '--proto_path', PROTO_DIR,
                     '--cpp_out', PROTO_DIR])

## if there are any other build or make operations that need to be performed for your modification, please move
## the required build products into the DUMP_DIR after being created.
p = subprocess.Popen(['mkdir', 'build'], cwd=SOURCE_DIR)
p.wait()
p = subprocess.Popen(['cmake', '-DBUILD_SHARED_LIBS=OFF', '..'], cwd=BUILD_DIR)
p.wait()
p = subprocess.Popen(['make', '-j'], cwd=BUILD_DIR)
p.wait()
p = subprocess.Popen(['make', 'pycaffe'], cwd=BUILD_DIR)
p.wait()
p = subprocess.Popen(['cp','-R', '.', DUMP_DIR], cwd=PY_DIR)
p.wait()
p = subprocess.Popen(['rm', '_caffe.so'], cwd=DUMP_DIR)
p.wait()
p = subprocess.Popen(['cp', '-R', '.', DUMP_DIR], cwd=LIB_DIR)
p.wait()
print('build complete.')