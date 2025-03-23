import time
import threading

import win32api

from settings import settings


class Reflex:
    def __init__(self) -> None:
        self.prev_x, self.prev_y = win32api.GetCursorPos()
        self.rel_x, self.rel_y = 0, 0
        threading.Thread(target=self.__thr, daemon=False).start()
    
    
    def __thr(self) -> None:
        while settings.is_running:
            x, y = win32api.GetCursorPos()
            self.rel_x = (x - self.prev_x) * 2
            self.rel_y = (y - self.prev_y) * 2
            self.prev_x, self.prev_y = win32api.GetCursorPos()
            time.sleep(0.001)