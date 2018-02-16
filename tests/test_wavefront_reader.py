from os import path
import pytest
from wavefront_reader import read_wavefront



filepath = path.join(path.split(__file__)[0], '..', 'examples')

filenames = ['untitled.obj',
             'untitled_with_normals.obj',
             'untitled_with_normals_and_texcoords.obj',
             'two_complete_meshes.obj',
             'bad_file.obj'
             ]

fnames = [path.join(filepath, name) for name in filenames]


@pytest.mark.parametrize("fn, count", zip(fnames, [1, 1, 1, 2, 1]))
def test_all_materials_extracted(fn, count):
    geoms = read_wavefront(fn)
    assert len(geoms) == count

# Ignore 'bad_file.obj', it purposefully has no material
@pytest.mark.parametrize("fn", fnames[0:-1])
def test_geoms_have_material_dict(fn):
    geoms = read_wavefront(fn)
    for geom in geoms.values():
        assert 'material' in geom
        assert isinstance(geom['material'], dict)
        assert 'Kd' in geom['material']


