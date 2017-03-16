from os import path
import pytest
import unittest
import os
from uuid import uuid4
from wavefront_reader import WavefrontWriter, read_objfile
import numpy as np


class TestWriter(unittest.TestCase):

    def setUp(self):
        self.verts = [[0., 0., 0.], [0., 1., 1.], [1., 0., 0.]]
        self.norms = [[0., 1., 0.]]
        self.objname = 'Triangle'
        self.writer = WavefrontWriter.from_arrays(self.objname, self.verts, self.norms)

    def test_writer_completes(self):
        result = self.writer.dumps()
        self.assertTrue(len(result) > 1 and type(result) == str)

    def test_writer_writes_to_file(self):
        fname = '/tmp/testobj{}.obj'.format(uuid4())
        with open(fname, 'w') as f:
            self.writer.dump(f)
        self.assertTrue(os.path.exists(fname))

    def test_writer_writes_to_filename(self):
        fname = '/tmp/testobj{}.obj'.format(uuid4())
        self.writer.dump(fname)
        self.assertTrue(os.path.exists(fname))

    def test_writer_can_be_read_by_reader(self):
        fname = '/tmp/testobj{}.obj'.format(uuid4())
        self.writer.dump(fname)
        geoms = read_objfile(fname)
        self.assertTrue(self.objname in geoms)
        obj = geoms[self.objname]
        self.assertTrue(np.isclose(np.array(self.verts), np.array(obj['v'])).all())
        self.assertTrue(np.isclose(np.array(self.norms), np.array(obj['vn'])).all())
