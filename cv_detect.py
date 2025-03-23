import math

import cv2
import numpy


from settings import settings
from reflex import Reflex


class CV:
    def __init__(self, min_: numpy.array, max_: numpy.array, min_size: int=40) -> None:
        self.min = min_
        self.max = max_
        self.min_size = min_size
        
        self.reflex = Reflex()

    
    def find_objects(self, frame) -> list:
        mask = cv2.inRange(cv2.cvtColor(frame, cv2.COLOR_BGR2HSV), self.min, self.max)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if settings.reflex_on:
            return self.sort(
                [[int(x - self.reflex.rel_x), int(y - self.reflex.rel_y), w, h] for x, y, w, h in map(cv2.boundingRect, contours) if math.sqrt(w ** 2 + h ** 2) > self.min_size]
            )
        else:
            return self.sort(
                [x for x in map(cv2.boundingRect, contours) if math.sqrt(x[2] ** 2 + x[3] ** 2) > self.min_size]
            )
    
    
    def sort(self, bboxes: list[int, int, int, int]) -> list[int, int, int, int]:
        distances = [
            math.sqrt(
                (bbox[0] + bbox[2] // 2 - settings.FOV // 2) ** 2 + (bbox[1] + bbox[3] // 2 - settings.FOV // 2) ** 2
            )
        for bbox in bboxes]
        return [bboxes[i] for i in [distances.index(x) for x in sorted(distances)]]