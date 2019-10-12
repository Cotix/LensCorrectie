import math

class Vec:
    x = 0.0
    y = 0.0
    z = 0.0

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self._length = math.sqrt(self.x*self.x + self.y*self.y + self.z*self.z)
    
    def dot(self, other):
        return self.x*other.x + self.y*other.y + self.z*other.z
    
    def __mul__(self, scalar):
        return Vec(self.x*scalar, self.y*scalar, self.z*scalar)

    def __rmul__(self, scalar):
        return Vec(self.x*scalar, self.y*scalar, self.z*scalar)

    def __sub__(self, other):
        return Vec(self.x-other.x, self.y-other.y, self.z-other.z)

    def __add__(self, other):
        return Vec(self.x+other.x, self.y+other.y, self.z+other.z)

    def cross(self, other):
        return Vec(self.y*other.z - self.z*other.y,
                    self.z*other.x - self.x*other.z,
                    self.x*other.y - self.y*other.x)
    
    def length(self):
        return self._length

    def normalize(self):
        return Vec(self.x/self._length, self.y/self._length, self.z/self._length)

    def rotate(self, other, angle):
        a = self
        b = other
        a_dir_b = (a.dot(b) / b.dot(b)) * b
        a_ort_b = a - a_dir_b

        w = b.cross(a_ort_b)

        x1 = math.cos(angle) / a_ort_b.length()
        x2 = math.sin(angle) / w.length()

        a_ort_b_phi = a_ort_b.length() * ((x1 * a_ort_b) + (x2 * w))
        a_rot_b_phi = a_ort_b_phi + a_dir_b
        return a_rot_b_phi
    
    def __str__(self):
        return f'Vector({self.x}, {self.y}, {self.z})'
    
    def __repr__(self):
        return str(self)
    
    def angle(self, other):
        return math.acos(self.dot(other)/(self.length()*other.length()))