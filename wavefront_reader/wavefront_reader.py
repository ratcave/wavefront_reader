# -*- coding: utf-8 -*-
import numpy as np
import unittest
from collections import namedtuple, defaultdict
from six import iteritems

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
