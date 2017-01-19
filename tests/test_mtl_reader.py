from os import path
import pytest
from wavefront_reader import read_mtlfile

filepath = path.join(path.split(__file__)[0], '..', 'examples')

filenames = ['untitled.mtl',
             'untitled_with_normals.mtl',
             'untitled_with_normals_and_texcoords.mtl',
             'two_complete_meshes.mtl'
             ]

fnames = [path.join(filepath, name) for name in filenames]


@pytest.mark.parametrize("fn", fnames)
def test_files_exist(fn):
        assert path.exists(fn)

@pytest.mark.parametrize("fn, count", zip(fnames, [1, 1, 1, 2]))
def test_all_materials_extracted(fn, count):
    materials = read_mtlfile(fn)
    assert len(materials) == count


@pytest.mark.parametrize("fn, count", zip(fnames, [1, 1, 1, 2]))
def test_all_materials_extracted(fn, count):
    materials = read_mtlfile(fn)
    assert len(materials) == count

@pytest.mark.parametrize("fn, diffuse", zip(fnames, [(0.64, 0.64, 0.64),
                                                     (0.64, 0.6, 0.64),
                                                     (0.64, 0.64, 0.64),
                                                     (0.64, 0.64, 0.24)]))
def test_diffuse_values_correct(fn, diffuse):
    materials = read_mtlfile(fn)
    assert materials['Material']['Kd'] == diffuse


@pytest.mark.parametrize("fn, illum", zip(fnames, [2, 2, 2, 3]))
def test_illum(fn, illum):
    materials = read_mtlfile(fn)
    assert materials['Material']['illum'] == illum
    assert isinstance(materials['Material']['illum'], int)
