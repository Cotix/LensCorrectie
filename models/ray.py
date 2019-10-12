

class Ray:
    
    def __init__(self, position, direction):
        self.pos = position
        self.dir = direction

    def __str__(self):
        return f'Ray({self.pos}, {self.dir})'
    
    def __repr__(self):
        return str(self)

    def intersect(self, other):
        P1 = self.pos
        P2 = other.pos
        V1 = self.dir
        V2 = other.dir

        # a (V1.cross(V2)) = (P2 - P1).cross(V2)

        left = V1.cross(V2)
        right = (P2 - P1).cross(V2)

        a = 0
        if right.x != 0 and left.x != 0:
            a = right.x / left.x
        elif right.y != 0 and left.y != 0:
            a = right.y / left.y
        else:
            a = right.z / left.z

        return self.pos + (self.dir * a)

