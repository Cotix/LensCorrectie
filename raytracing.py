from models.vector import Vec
from models.screen3d import Screen3D
from models.ray import Ray
from models.doublescreen import DoubleScreen
from models.lens import Sphere
import math
import time
import pygame

class RayTracing:

    def __init__(self, lens, lens_width, lens_height, screen_distance, eye_dist, input, output):
        self.lens = lens
        self.lens_width = lens_width
        self.lens_height = lens_height
        self.screen_distance = screen_distance
        self.eye_dist = eye_dist
        self.input = input
        self.output = output
        self.eyemaxx = 4
        self.eyemaxy = 4


    def trace_bitmap(self):

        # self.direction = Vec(1.0, 0.0, 0.0)
        # self.normal_x = self.direction.cross(Vec(0.0, 1.0, 0.0))
        # self.normal_y = self.direction.cross(self.normal_x)
        # self.position = Vec(0.0, 0.0, 0.0)

        # print(f'Normal x {self.normal_x} ,Normal y {self.normal_y}')

        # center = self.cast_lens_ray(self.screen_width / 2, self.screen_height / 2)
        # center.dir = center.dir.normalize(self.cast_ray(0, 0, ))

        print(self.eye_dist)
        screens = DoubleScreen(self.gen_source_screen(), self.gen_dest_screen(), self.input, self.output)
        
        time.sleep(2)
        for source_x in range(0, self.input.get_width()):
            print(source_x)
            pygame.display.flip()
            for source_y in range(0, self.input.get_height()):
                for lens_x in range(0, self.eyemaxx):
                    for lens_y in range(0, self.eyemaxy):
                        ray = self.cast_lens_ray(source_x, source_y, lens_x, lens_y)
                        screens.trace(ray)

        screens.draw()

    def calc_screen_dimension(self, ray, center):
        angle = ray.dir.angle(center.dir)
        length = math.cos(angle) * 10

        return ray.pos + ray.dir * length

    def search_source_dist(self, goal):
        result = 1
        fail_dist = 999999999
        for t in range(4000000, 40000000, 1):
            self.eye_dist = t / 4000000

            dist = self.calc_source_dist()
            if abs(dist - goal) < fail_dist:
                print(self.eye_dist, dist)
                result = self.eye_dist
                fail_dist = abs(dist - goal)
        self.eye_dist = result
        return result


    def calc_source_dist(self):
        ray0 = self.cast_lens_ray(0, 0, 0, 0)
        ray1 = self.cast_lens_ray(0, 0, self.eyemaxx, self.eyemaxy)
        return ray0.intersect(ray1).x

    def gen_source_screen(self):
        distance = self.calc_source_dist()
        print("Source distance", distance)

        print("START GENERATING SOURCE DIMENSION RAYS")
        min_ray = self.cast_lens_ray(self.input.get_width(), self.input.get_height(), 0, 0)
        max_ray = self.cast_lens_ray(0, 0, self.eyemaxx, self.eyemaxy)

        print("rays, ", min_ray, max_ray)

        min_ray.dir = min_ray.dir.normalize()
        max_ray.dir = max_ray.dir.normalize()

        t0 = (distance - min_ray.pos.x) / min_ray.dir.x
        minpos1 = min_ray.pos + (min_ray.dir * t0)

        t1 = (distance - max_ray.pos.x) / max_ray.dir.x
        maxpos1 = max_ray.pos + (max_ray.dir * t1)


        # Checking other minima and maxima
        min_ray = self.cast_lens_ray(self.input.get_width(), self.input.get_height(), self.eyemaxx, self.eyemaxy)
        max_ray = self.cast_lens_ray(0, 0, 0, 0)

        print("rays, ", min_ray, max_ray)

        min_ray.dir = min_ray.dir.normalize()
        max_ray.dir = max_ray.dir.normalize()

        t0 = (distance - min_ray.pos.x) / min_ray.dir.x
        minpos2 = min_ray.pos + (min_ray.dir * t0)

        t1 = (distance - max_ray.pos.x) / max_ray.dir.x
        maxpos2 = max_ray.pos + (max_ray.dir * t1)

        minpos = Vec(min(minpos1.x, minpos2.x), min(minpos1.y, minpos2.y), min(minpos1.z, minpos2.z))
        maxpos = Vec(max(maxpos1.x, maxpos2.x), max(maxpos1.y, maxpos2.y), max(maxpos1.z, maxpos2.z))

        return Screen3D(minpos, maxpos)

    def gen_dest_screen(self):
        distance = self.screen_distance

        print("Screen distance", distance)
        min_ray = self.cast_lens_ray(self.input.get_width(), self.input.get_height(), self.eyemaxx, self.eyemaxy)
        max_ray = self.cast_lens_ray(0, 0, 0, 0)

        min_ray.dir = min_ray.dir.normalize()
        max_ray.dir = max_ray.dir.normalize()

        t0 = (distance - min_ray.pos.x) / min_ray.dir.x
        minpos = min_ray.pos + (min_ray.dir * t0)

        t1 = (distance - max_ray.pos.x) / max_ray.dir.x
        maxpos = max_ray.pos + (max_ray.dir * t1)

        return Screen3D(minpos, maxpos)

    def cast_lens_ray_old(self, x, y, eye_x, eye_y):
        ox = -self.eye_dist
        oy = (y / self.input.get_height()) - 0.5
        oz = (x / self.input.get_width()) - 0.5

        origin = Vec(ox, oy, oz)
        
        ex = 0
        ey = (eye_y / self.eyemaxx - 0.5) * self.lens_height
        ez = (eye_x / self.eyemaxy - 0.5) * self.lens_width

        # print(ex, ey, ez)

        direction = Vec(ex, ey, ez) - origin
        return self.lens.refract_ray(Ray(origin, direction.normalize()))

    def cast_lens_ray(self, x, y, eye_x, eye_y):
        # start = Vec(0, 0, 0)
        sphere = Sphere(Vec(0, 0, 0), 1.15)

        # x_angle_factor = x / self.input.get_width() - 0.5
        # y_angle_factor = y / self.input.get_height() - 0.5

        # ray_dir = Vec(-1, 0, 0)
        # ray_dir = ray_dir.rotate(Vec(0, 0, 1), y_angle_factor * math.pi / 2)
        # ray_dir = ray_dir.rotate(Vec(0, 1, 0), -x_angle_factor * math.pi / 2)
        
        start = Vec(0, 0, 0)

        ray_dir = Vec(-1, y / self.input.get_height() - 0.5, x / self.input.get_width() - 0.5)


        # oy = (y / self.input.get_height()) - 0.5
        # oz = (x / self.input.get_width()) - 0.5


        ray = Ray(start, ray_dir)

        # print("ray to sphere", ray)

        intersect_point = sphere.ray_intersection(ray, False)

        ex = 0
        ey = (eye_y / self.eyemaxx - 0.5) * self.lens_height
        ez = (eye_x / self.eyemaxy - 0.5) * self.lens_width

        ray_end = Vec(ex, ey, ez)

        direction = (ray_end - intersect_point).normalize()

        # print("Generated ray from", intersect_point, direction)
        return self.lens.refract_ray(Ray(intersect_point, direction))


