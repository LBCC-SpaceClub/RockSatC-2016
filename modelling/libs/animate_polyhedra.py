#!/usr/bin/python2
# from __future__ import division
import numpy
# from pylab import *

# ------------------------------------------------------------------------------
# Define functions
# ------------------------------------------------------------------------------
# returns the distance from the point p to the plane defined by 3 points
def dist_to_plane(point, plane):
  p = point-plane[2]
  e1 = plane[0]-plane[2]
  e2 = plane[1]-plane[2]
  n = cross(e1, e2)
  nhat = n/norm(n)
  return dot(nhat, p)

# takes a 2d array and treats it as a list of vertices
# returns a 2d array, that is a list of indices of vertices per face.
# It will pad each list of vertices so that they are a minimum of length pad
# which is useful for mixtures

# new method, look at all possible triplets of vertices, then reject those that have
# other vertices on both sides of the plane that they span
def get_faces(verts, pad = 0, acc = 0.1):
  # find the distance between neighbors. Assumes all neighbors are equidistant
  faces = []
  for i in xrange(len(verts)):
    u = verts[i]
    for j in xrange(i+1, len(verts)):
      v = verts[j]
      for k in xrange(j+1, len(verts)):
        w = verts[k]
        # now make sure we don't have a duplicate
        keep = True
        for face in faces:
          if (i in face) and (j in face) and (k in face):
            keep = False
            break
        if keep:
          plane = vstack((u, v, w))
          has_neg = False
          has_pos = False
          for l in xrange(len(verts)):
            if l != i and l != j and l != k:
              dist = dist_to_plane(verts[l], plane)
              if (dist > acc): has_pos = True
              elif (dist < -acc): has_neg = True
          if (not has_neg) or (not has_pos):
            # this plane is good!
            face = empty(0)
            for l in xrange(len(verts)):
              if abs(dist_to_plane(verts[l], plane)) < acc:
                face = append(face, l)
            faces.append(face)
  # okay we have our faces, but we need to sort them so they'll connect properly
  sfaces = []
  for face in faces:
    sface = array([face[0]])
    for i in xrange(len(face)-1):
      last = sface[-1]
      dmin = 10000
      for j in face:
        if not j in sface:
          dist = norm(verts[last] - verts[j])
          if dist < dmin:
            dmin = dist
            next_neighbor = j
      sface = append(sface, next_neighbor)
    sfaces.append(sface)
  faces = sfaces
  #print("we have %i vertices, %i faces, and the first face has %i vertices." %(len(verts), len(faces), len(faces[0])))
  # enforce that all faces have the same number of points so it can be a
  # 2d array:
  n = max([len(face) for face in faces])
  n = max(n, pad)
  for i in xrange(len(faces)):
    if len(face) < n:
      faces[i] = hstack((faces[i], ones(n-len(faces[i]))*faces[i][-1]))
  return array(faces)