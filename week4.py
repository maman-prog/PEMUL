
import point


class Point():
    x=0
    y=0
pl=Point()
pl.x=30
pl.y=-8
pl.nama="Lokasi UMY"
print(pl.nama)

pl2=point(7,9)
print(pl)
print(pl.distance_from_origin())

pl2=Point(7,9)
print("jarak 2 titik: "+ str(pl2.distance_from_origin(pl2)))

from point import *
class point3D(point):
    def __init__(self,x,y,z):
        point.__init__(self,x,y)
        self.z=z
    def translare(self, dx, dy, dz):
        self.z += dz
    def __str__(self):
        return "Point3D("+str(self.x)+","+str(self.y)+","+str(self.z)+")"
        ", "+str(self.y) + \
        ", "+str(self.z)+")"
