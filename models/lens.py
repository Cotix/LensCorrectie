import math
from models.vector import Vec
from models.ray import Ray

class Circle:
    # Circle on the X axis in the same direction as de other two axises
    def __init__(self, origin, radius):
        assert origin.y == origin.z == 0
        self.origin = origin
        self.radius = radius

class Sphere:

    def __init__(self, origin, radius):
        self.origin = origin
        self.radius = radius

    def ray_intersection(self, ray, isRight=True):
        oc = ray.pos - self.origin
        a = ray.dir.dot(ray.dir)
        b = 2 * ray.dir.dot(oc)
        c = oc.dot(oc) - (self.radius*self.radius)
        discriminant = b*b - 4*a*c

        if discriminant >= 0:
            t0 = (-b - math.sqrt(discriminant))/(2*a)
            t1 = (-b + math.sqrt(discriminant))/(2*a)

            dir0 = ray.dir * t0
            dir1 = ray.dir * t1

            p1 = ray.pos + dir0
            p2 = ray.pos + dir1

            # print(f'Possible intersections: {p1}, {p2}')

            if isRight:
                return p1 if p1.x >= self.origin.x else p2
            else:
                return p1 if p1.x < self.origin.x else p2
        return None
    
    def sphere_intersection(self, sphere):
        # Only works on spheres along the X axis
        assert self.origin.y == self.origin.z == sphere.origin.y == sphere.origin.z == 0
        d = self.origin.x - sphere.origin.x
        distance_difference = (d*d-sphere.radius*sphere.radius + self.radius*self.radius)
        radius = abs(1/(2*d) * math.sqrt(4*d*d*self.radius*self.radius - distance_difference*distance_difference))
        x = distance_difference/(2*d)
        return Circle(Vec(self.origin.x - x, 0, 0), radius)
    
    def __str__(self):
        return f'Sphere({self.origin}, {self.radius})'
    
    def __repr__(self):
        return str(self)
    

class ConvexLens:

    def __init__(self, x1, x2, radius1, radius2, glass_refraction=1.38, air_refraction=1.0002):
        self.sphere_left = Sphere(Vec(x1, 0, 0), radius1)
        self.sphere_right = Sphere(Vec(x2, 0, 0), radius2)
        self.glass_refraction = glass_refraction
        self.air_refraction = air_refraction

    def _intersect_sphere(self, sphere, ray, isRight):
        intersection = sphere.ray_intersection(ray, isRight)
        assert intersection is not None
        origin_direction = sphere.origin - intersection
        normal = ray.dir.cross(origin_direction)
        if normal.length() == 0:
            return intersection, 0, normal
        return intersection, ray.dir.angle(origin_direction), normal

    def refract_ray(self, ray):
        # print(f'Intersecting {ray}')
        # First we intersect with the right sphere
        intersection, angle, normal = self._intersect_sphere(self.sphere_right, ray, False)
        # print(f'First intersection: {intersection}')

        # Going from air to glass
        new_angle = math.asin(self.air_refraction/self.glass_refraction * math.sin(angle))
        if new_angle != 0:
            ray = Ray(intersection, ray.dir.rotate(normal, new_angle))
        # print(f'New ray: {ray}')
        # Intersect left sphere
        intersection, angle, normal = self._intersect_sphere(self.sphere_left, ray, True)
        # print(f'Second intersection: {intersection}')
        
        # Going from glass to air
        # print(f'Angle: {angle}')
        new_angle = math.asin(self.glass_refraction/self.air_refraction * math.sin(angle))
        if new_angle != 0:
            return Ray(intersection, ray.dir.rotate(normal, new_angle))
        return Ray(intersection, ray.dir)
