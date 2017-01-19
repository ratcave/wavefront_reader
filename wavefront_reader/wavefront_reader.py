# -*- coding: utf-8 -*-
import numpy as np
from collections import namedtuple, defaultdict
from six import iteritems
from os import path

def parse_mixed_delim_str(line):
    """Turns .obj face index string line into [verts, texcoords, normals] numeric tuples."""
    arrs = [[], [], []]
    for group in line.split(' '):
        for col, coord in enumerate(group.split('/')):
            if coord:
                arrs[col].append(int(coord))

    return [tuple(arr) for arr in arrs]


def read_objfile(f):
    """Takes .obj file and returns dict of object properties for each object in file."""
    verts = defaultdict(list)
    obj_props = []
    for line in f:
        prefix, value = line.split(' ', 1)
        if prefix == 'o':
            obj_props.append({})
            obj = obj_props[-1]
            obj['f'] = []
            obj[prefix] = value.strip()
        if obj_props:
            if prefix[0] == 'v':
                verts[prefix].append([float(val) for val in value.split(' ')])
            elif prefix == 'f':
                obj[prefix].append(parse_mixed_delim_str(value))
            else:
                obj[prefix] = value.strip()


    # Reindex vertices to be in face index order, then remove face indices.
    verts = {key: tuple(value) for key, value in iteritems(verts)}
    for obj in obj_props:
        obj['f'] = tuple(np.array(verts) if verts[0] else tuple() for verts in zip(*obj['f']))
        for idx, vertname in enumerate(['v' ,'vt', 'vn']):
            if vertname in verts:
                obj[vertname] = verts[vertname][obj['f'][idx].flatten() - 1, :]
            else:
                obj[vertname] = tuple()
        del obj['f']

    geoms = {obj['o']:obj for obj in obj_props}

    return geoms


def read_objfile(fname):
    """Takes .obj filename and returns dict of object properties for each object in file."""
    verts = defaultdict(list)
    obj_props = []
    with open(fname) as f:
        lines = f.read().splitlines()

    if 'OBJ' not in lines[0]:
        raise ValueError("File not .obj-formatted.")

    for line in lines:
        if line:
            prefix, value = line.split(' ', 1)
            if prefix == 'o':
                obj_props.append({})
                obj = obj_props[-1]
                obj['f'] = []
                obj[prefix] = value
            if obj_props:
                if prefix[0] == 'v':
                    verts[prefix].append([float(val) for val in value.split(' ')])
                elif prefix == 'f':
                    obj[prefix].append(parse_mixed_delim_str(value))
                else:
                    obj[prefix] = value


    # Reindex vertices to be in face index order, then remove face indices.
    verts = {key: np.array(value) for key, value in iteritems(verts)}
    for obj in obj_props:
        obj['f'] = tuple(np.array(verts) if verts[0] else tuple() for verts in zip(*obj['f']))
        for idx, vertname in enumerate(['v' ,'vt', 'vn']):
            if vertname in verts:
                obj[vertname] = verts[vertname][obj['f'][idx].flatten() - 1, :]
            else:
                obj[vertname] = tuple()
        del obj['f']

    geoms = {obj['o']:obj for obj in obj_props}

    return geoms


def read_mtlfile(fname):
    materials = {}
    with open(fname) as f:
        lines = f.read().splitlines()

    for line in lines:
        if line:
            prefix, data = line.split(' ', 1)
            if 'newmtl' in prefix:
                material = {}
                materials[data] = material
            elif materials:
                if len(data.split(' ')) > 1:
                    material[prefix] = tuple(float(d) for d in data.split(' '))
                else:
                    try:
                        material[prefix] = int(data)
                    except ValueError:
                        material[prefix] = float(data)

    return materials


def read_wavefront(fname_obj):
    """Returns mesh dictionary along with their material dictionary from a wavefront (.obj and/or .mtl) file."""
    geoms = read_objfile(fname_obj)
    for line in open(fname_obj):
        if line.strip():
            prefix, data = line.strip().split(' ', 1)
            if 'mtllib' in prefix:
                fname_mtl = data
                break


    materials = read_mtlfile(path.join(path.dirname(fname_obj), fname_mtl))

    for geom in geoms.values():
        geom['material'] = materials[geom['usemtl']]

    return geoms


