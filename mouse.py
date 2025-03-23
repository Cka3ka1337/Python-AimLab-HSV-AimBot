import time
import math

import win32api
import win32con

from settings import settings


class Mouse:
    def __init__(self) -> None:
        self.__last_click = time.perf_counter()
        
    
    def __move(self, x_offset: int, y_offset: int) -> None:
        win32api.mouse_event(
            win32con.MOUSEEVENTF_MOVE,
            x_offset,
            y_offset
        )
    
    
    def __click(self) -> None:
        t = time.perf_counter()
        if t - self.__last_click > 0.05:
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0)
            
            self.__last_click = t
    
    
    def __calc_offsets(self, bbox: list[int, int, int, int]) -> tuple[int, int]:
        x, y = bbox[0] + bbox[2] // 2 - settings.FOV // 2, bbox[1] + bbox[3] // 2 - settings.FOV // 2
        distance = math.sqrt(
            x ** 2 + y ** 2
        ) * settings.scale
        rad = math.atan2(y, x)
        return int(math.cos(rad) * distance), int(math.sin(rad) * distance)
    
    
    def __handle_trigger_bot(self, bbox: list[int, int, int, int]) -> tuple[int, int]:
        ox, oy = bbox[0] + bbox[2] // 2 - settings.FOV // 2, bbox[1] + bbox[3] // 2 - settings.FOV // 2
        distance = math.sqrt(
            ox ** 2 + oy ** 2
        )
        
        min_ = (min(bbox[2:]) / 2) * 0.5
        return distance < min_
        
    
    
    def __call__(self, bbox) -> None:
        if win32api.GetAsyncKeyState(settings.overide_sleep_bind) or not bbox:
            return

        if settings.aimbot_always_work:
            self.__move(*self.__calc_offsets(bbox))
        
        elif win32api.GetAsyncKeyState(settings.aimbot_bind) and settings.work_aimbot:
            self.__move(*self.__calc_offsets(bbox))
        
        if settings.work_triggerbot:
            if self.__handle_trigger_bot(bbox):
                self.__click()