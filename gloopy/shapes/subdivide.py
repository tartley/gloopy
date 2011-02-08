from __future__ import division

from .shape import Shape, add_vertex


def subdivided(original):
    r"""
    Given a shape consisting entirely of triangular faces, returns a new Shape
    instance, copied from the given original but with each face subdivided into
    four triangles:  v0
                     /\                 v0-v2 correspond to indices face[0:2]
                    /  \
             mid[0]/----\mid[2]
                  / \  / \
                 /___\/___\
               v1  mid[1]  v2
    """
    vertices = original.vertices[:]
    faces = []
    colors = []

    # Edges gets populated with one entry per edge of the original shape.
    # Keys are (start, end) vertex indices (sorted by numerical value)
    # Value is the index of the new vertex inserted at that edge's midpoint
    edges = {}
    
    for face in original.faces:

        # verts at the midpoint of each edge
        midpoints = []

        for i in xrange(len(face)):
            next_i = (i + 1) % len(face)
            start = face[i]
            end = face[next_i]
            edge = tuple(sorted((start, end)))
            if edge not in edges:
                midpoint = (vertices[start] + vertices[end]) / 2
                edges[edge] = add_vertex(vertices, midpoint)
            midpoints.append( edges[edge] )

        for i in xrange(len(face)):
            prev_i = (i - 1) % len(face)
            faces.append([face[i], midpoints[i], midpoints[prev_i]])
            colors.append(face.color)
        faces.append([midpoints[i] for i in xrange(len(face))])
        colors.append(face.color.inverted())

    return Shape(vertices, faces, colors)

