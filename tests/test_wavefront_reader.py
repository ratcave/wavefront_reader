#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_wavefront_reader
----------------------------------

Tests for `wavefront_reader` module.
"""
from os import path
import unittest
from wavefront_reader import read_objfile, parse_mixed_delim_str

filepath = path.join(path.split(__file__)[0], '..', 'examples')

class TestReadObj(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        filename = path.join(filepath, 'untitled.obj')
        cls.objfile = open(filename, 'r')
        cls.geoms = read_objfile(cls.objfile)

    @classmethod
    def tearDownClass(cls):
        cls.objfile.close()

    def test_file_opens(self):
        self.assertFalse(self.objfile.closed)

    def test_file_returns_Geom(self):
        self.assertTrue('Cube' in self.geoms)

    def test_has_vertices(self):
        cube = self.geoms['Cube']
        self.assertTrue(cube['v'].size > 0)

    def test_has_no_normals(self):
        cube = self.geoms['Cube']
        self.assertFalse(cube['vn'])

    def test_has_no_texcoords(self):
        cube = self.geoms['Cube']
        self.assertFalse(cube['vt'])


class TestReadObjWithNormals(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        filename = path.join(filepath, 'untitled_with_normals.obj')
        cls.objfile = open(filename, 'r')
        cls.geoms = read_objfile(cls.objfile)

    @classmethod
    def tearDownClass(cls):
        cls.objfile.close()

    def test_file_opens(self):
        self.assertFalse(self.objfile.closed)

    def test_file_returns_obj(self):
        self.assertTrue('Cube' in self.geoms)

    def test_has_vertices(self):
        cube = self.geoms['Cube']
        self.assertTrue(cube['v'].size > 0)

    def test_has_normals(self):
        cube = self.geoms['Cube']
        self.assertTrue(cube['vn'].size > 0)

    def test_has_no_texcoords(self):
        cube = self.geoms['Cube']
        self.assertFalse(cube['vt'])

    def test_all_vert_lengths_match(self):
        cube = self.geoms['Cube']
        self.assertEquals(cube['vn'].shape[0], cube['v'].shape[0])


class TestStringParser(unittest.TestCase):

    def test_verts_only(self):
        line = '1 2 3'
        out = parse_mixed_delim_str(line)
        self.assertEqual(out, [(1, 2, 3), tuple(), tuple()])

    def test_verts_and_texcoords(self):
        line = '1/5 2/6 3/7'
        out = parse_mixed_delim_str(line)
        self.assertEqual(out, [(1, 2, 3), (5, 6, 7), tuple()])

    def test_verts_and_norms(self):
        line = '1//5 2//6 3//7'
        out = parse_mixed_delim_str(line)
        self.assertEqual(out, [(1, 2, 3), tuple(), (5, 6, 7)])

    def test_all_coords_present(self):
        line = '1/3/5 2/4/6 3/5/7'
        out = parse_mixed_delim_str(line)
        self.assertEqual(out, [(1, 2, 3), (3, 4, 5), (5, 6, 7)])
