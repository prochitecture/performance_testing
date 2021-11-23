import os, sys
def _checkPath():
    path = os.path.dirname(__file__)
    if path in sys.path:
        sys.path.remove(path)
    # make <path> the first one to search for a module
    sys.path.insert(0, path)
_checkPath()


from data_karl_marx_allee import polysWithHoles
from timeit import timeit
import bmesh


class Testing:
    
    def __init__(self, polygons):
        self.polygons = polygons
        #self.bm = bmesh.new()
    
    def test1(self):
        for entryIndex, polygonEntry in enumerate(self.polygons):
            # new bmesh instance for each <polygonEntry>
            bm = bmesh.new()
            numContours = len(polygonEntry)-1
            
            # create a list of <BMEdge>s for the contours that form the outer polygon border and polygon holes
            edges = []
            for contourIndex in range(numContours):
                self.createEdges(polygonEntry[contourIndex], edges, bm)
            
            bmesh.ops.triangle_fill(bm, use_beauty=False, use_dissolve=False, edges=edges)
    
    def test2(self):
        for entryIndex, polygonEntry in enumerate(self.polygons):
            # new bmesh instance for each <polygonEntry>
            bm = bmesh.new()
            numContours = len(polygonEntry)-1
            
            # create a list of <BMEdge>s for the polygon with bridges, it's the last one in <polygonEntry>
            edges = []
            self.createEdges(polygonEntry[-1], edges, bm)
    
    def createEdges(self, coords, edges, bm):
        numCoords = len(coords)
        verts = [bm.verts.new(coord+(0.,)) for coord in coords]
        edges.extend(
            bm.edges.new( (verts[i1], verts[i2]) ) \
                for i1,i2 in zip( range(-1, numCoords-1), range(0, numCoords) )
        )


testing = Testing(polysWithHoles)
print( timeit("testing.test1()", number=100, globals=globals()) )
print( timeit("testing.test2()", number=100, globals=globals()) )