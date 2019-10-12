from models.screen3d import Screen3D

class DoubleScreen:

    def __init__(self, source, destination, input_file, output):
        self.source = source
        self.destination = destination
        print(f'Source size: {source.width}, {source.height}')
        print(f'Destination size: {destination.width}, {destination.height}')
        self.rays = 0
        self.screen_height = output.get_height()
        self.screen_width = output.get_width()
        print(self.screen_width, self.screen_height)
        self.screen = [[0, 0, 0, 0] for _ in range(0, self.screen_height*self.screen_width)]
        self.image_file = input_file
        self.output = output

    def trace(self, ray):
        source_x, source_y = self.source.trace(ray)
        dest_x, dest_y = self.destination.trace(ray)
        if (dest_x > 1 or dest_y > 1):
            return
        x = round(dest_x*(self.screen_width-1))
        y = round(dest_y*(self.screen_height-1))

        pixel = self._get_pixel(source_x, source_y)
        
        sp = self.screen[y*self.screen_width + x]

        sp[0], sp[1], sp[2], sp[3] = sp[0]+pixel[0], sp[1]+pixel[1], sp[2]+pixel[2], sp[3]+1
        self.rays += 1
        # self.output.set_at((x, y), self.get_pixel_value(x, y))
    
    def _get_pixel(self, x, y):
        x = round(x*(self.image_file.get_width()-1))
        y = round(y*(self.image_file.get_height()-1))
        
        if (x < 0 or y < 0):
            return (0,0,0)
        if (x >= self.image_file.get_width() or y >= self.image_file.get_height()):
            return (0,0,0)
        
        return self.image_file.get_at((x, y))
    
    def get_pixel_value(self, x, y):
        rays_per_pixel = self.rays / (self.screen_width*self.screen_height)
        pixel = self.screen[y*self.screen_width + x]

        if pixel[3] == 0:
            return (0,0,0,255)
        return (round(pixel[0] / pixel[3]),
                round(pixel[1] / pixel[3]),
                round(pixel[2] / pixel[3]),
                255)
    
    def draw(self):
        for x in range(0, self.screen_width):
            for y in range(0, self.screen_height):
                self.output.set_at((x, y), self.get_pixel_value(x, y))