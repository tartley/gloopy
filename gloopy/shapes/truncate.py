from __future__ import division

from .shape import Shape, add_vertex
from ..color import Color


def edges(shape, index, face=None):
    '''
    Returns a dict with one entry for each edge that connects to the given
    index. Keys are the connected index, values are the vector of the edge,
    from the location of the given index to the location of the connected
    index.
    Presumably this should be a method on Shape
    '''
    joined_indices= set()
    for face in shape.faces:
        for i in xrange(len(face)):
            if face[i] == index:
                joined_indices.add(face[i-1])
                joined_indices.add(face[i+1])
    d = {
        i: shape.vertices[i] - shape.vertices[index]
        for i in joined_indices
    }
    return d


def filter_edges(edges, face):
    return {
        k: v for k, v in edges.iteritems()
        if k in face.indices
    }


def truncate(original, amount=0.5):
    '''
    Returns a new Shape instance, copied from the original but with every
    vertex truncated, exposing new faces which occupy volume within the
    original shape. The amount of truncation must lie between 0 and 1:
        0: do nothing, although some redundant new vertices and zero-sized
           faces will be created.
        intermediate: truncation of vertices forms new faces on the shape.
        1: new faces grow until they meet - original faces entirely dissapear.
    Truncating by an amount of 1 results in the original's geometric dual.
    '''
    vertices = []
    faces = []
    colors = []

    print '\n'.join(str(v) for v in original.vertices)

    # shrink the original faces
    # HAS A BUG: we don't know what order to add the indices which pass
    # the 'if in face.indices' test.
    for face in original.faces:
        print 'face', face.indices
        shrunk_face = []
        for index in face:
            print '  index', index
            orig_position = original.vertices[index]
            for joined_index, edge in edges(original, index).iteritems():
                if joined_index in face.indices:
                    print '    related edge', edge
                    new_position = orig_position + (edge * amount)
                    shrunk_face.append(add_vertex( vertices, new_position ))
        faces.append(shrunk_face)
        colors.append(Color.Random())

    print vertices
    print faces
    print colors
    return Shape(vertices, faces, colors)

