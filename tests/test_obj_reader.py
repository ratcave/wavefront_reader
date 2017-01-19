#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_wavefront_reader
----------------------------------

Tests for `wavefront_reader` module.
"""
from os import path
import pytest
from wavefront_reader import read_objfile

filepath = path.join(path.split(__file__)[0], '..', 'examples')

filenames = ['untitled.obj',
             'untitled_with_normals.obj',
             'untitled_with_normals_and_texcoords.obj',
             'two_complete_meshes.obj'
             ]

fnames = [path.join(filepath, name) for name in filenames]

@pytest.mark.parametrize("objfile", fnames)
def test_files_exist(objfile):
        assert path.exists(objfile)


@pytest.mark.parametrize("objfile,expected", list(zip(fnames, [True, True, True, True])))
def test_has_vertices(objfile, expected):
    geoms = read_objfile(objfile)
    cube = geoms['Cube']
    assert (len(cube['v']) > 0) == expected


@pytest.mark.parametrize("objfile,expected", list(zip(fnames, [False, True, True, True])))
def test_has_normals(objfile, expected):
    geoms = read_objfile(objfile)
    cube = geoms['Cube']
    assert (len(cube['vn']) > 0) == expected


@pytest.mark.parametrize("objfile,expected", list(zip(fnames, [False, False, True, True])))
def test_has_texcoords(objfile, expected):
    geoms = read_objfile(objfile)
    cube = geoms['Cube']
    assert (len(cube['vt']) > 0) == expected


@pytest.mark.parametrize("objfile", fnames)
def test_has_texcoords(objfile):
    geoms = read_objfile(objfile)
    for geom in geoms.values():
        vertrows = len(geom['v'])
        for coord in ['vn', 'vt']:
            if len(geom[coord]):
                assert len(geom[coord]) == vertrows


@pytest.mark.parametrize("objfile, count", list(zip(fnames, [1, 1, 1, 2])))
def test_has_correct_number_of_meshes(objfile, count):
    geoms = read_objfile(objfile)
    assert len(geoms) == count


