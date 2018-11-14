class Game:
    def is_collision(self, x1, y1, x2, y2, bsize):
        if x1 >= x2 and x1 <= x2 + bsize:
            if y1 >= y2 and y1 <= y2 + bsize:
                return True
        return False

    def is_wall_collision(self, x_lower, x_upper, y_lower, y_upper, x2, y2):
        if x2 < x_lower or x2 > x_upper or y2 < y_lower or y2 > y_upper:
            return True
        return False
