from models.vector import Vec

class Screen3D:

    def __init__(self, minpos, maxpos):
        self.P0 = minpos
        self.S1 = Vec(0, 0, maxpos.z - minpos.z)
        self.S2 = Vec(0, maxpos.y - minpos.y, 0)
        self.N = self.S1.cross(self.S2)
        self.height = self.S2.y
        self.width = self.S1.z

        print("Created 3d screen from ", minpos, "to", maxpos)

    def trace(self, ray):
        R0 = ray.pos
        D = ray.dir.normalize()

        assert D.dot(self.N) < 0
        a = ((self.P0 - R0).dot(self.N)) / D.dot(self.N)

        relative_hit = (R0 + a * D - self.P0)

        x = relative_hit.z / self.S1.z
        y = relative_hit.y / self.S2.y


        return x, y





