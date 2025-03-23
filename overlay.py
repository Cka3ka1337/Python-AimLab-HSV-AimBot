import ctypes

import win32gui

from ctypes import wintypes

from pyray import *

from settings import settings


class WINDOWINFO(ctypes.Structure):
    _fields_ = [
        ('cbSize', wintypes.DWORD),
        ('rcWindow', wintypes.RECT),
        ('rcClient', wintypes.RECT),
        ('dwStyle', wintypes.DWORD),
        ('dwExStyle', wintypes.DWORD),
        ('dwWindowStatus', wintypes.DWORD),
        ('cxWindowBorders', wintypes.UINT),
        ('cyWindowBorders', wintypes.UINT),
        ('atomWindowType', wintypes.ATOM),
        ('wCreatorVersion', wintypes.WORD),
    ]


class Overlay:
    def __init__(self, target_window_name: str) -> None:
        set_target_fps(settings.frame_rate_limit)
        
        set_config_flags(ConfigFlags.FLAG_WINDOW_UNDECORATED)
        set_config_flags(ConfigFlags.FLAG_WINDOW_MOUSE_PASSTHROUGH)
        set_config_flags(ConfigFlags.FLAG_WINDOW_TRANSPARENT)
        set_config_flags(ConfigFlags.FLAG_WINDOW_TOPMOST)
        
        self.target_window_hwnd = win32gui.FindWindow(
            None, target_window_name)

        init_window(
            settings.FOV,
            settings.FOV,
            'Overlay'
        )
        self.__set_target_window_pos()
        
        self.cx = get_screen_width() // 2
        self.cy = get_screen_height() // 2

    
    def __set_target_window_pos(self) -> None:
        x, y, w, h = self.get_window_info()
        set_window_position(
            x + w // 2 - settings.FOV // 2,
            y + h // 2 - settings.FOV // 2,
        )
        # print(x, y, w, h)
    
    
    def get_window_info(self):
        win_info = WINDOWINFO()
        rect = wintypes.RECT()
        ctypes.windll.user32.GetWindowInfo(self.target_window_hwnd, ctypes.byref(win_info))
        ctypes.windll.user32.GetClientRect(self.target_window_hwnd, ctypes.byref(rect))
        return (win_info.rcClient.left, win_info.rcClient.top, rect.right, rect.bottom)

    
    def close(self) -> None:
        close_window()
    
    
    @property
    def is_alive(self) -> bool:
        return not window_should_close()
    
    
    def render(self, rects: list) -> None:
        self.__set_target_window_pos()
        
        begin_drawing()
        clear_background((0, 0, 0, 0))
        
        if settings.visuals_on:
        
            for idx, bbox in enumerate(rects):
                x, y, w, h = bbox
                h -= 1
                x += 1
                w -= 1
                
                draw_rectangle(
                    x,
                    y,
                    w,
                    h,
                    (20, 20, 20, 220)
                )
                box = BoundingBox(Vector3(x, y, 0), Vector3(x + w, y + h, 0))
                draw_bounding_box(box, (255, 255, 255, 255))
                
                draw_line(
                    self.cx,
                    self.cy,
                    x + w // 2,
                    y + h // 2,
                    (230, 230, 230, 220)
                )
                
                draw_text(
                    f'Idx: {idx}',
                    x,
                    y - 16,
                    16,
                    (255, 255, 255, 255)
                )
        
            # draw_rectangle_lines(
            #     1, 1, settings.FOV - 1, settings.FOV - 2,
            #     (255, 255, 255, 255)
            # )
            
            draw_circle_lines(
                self.cx,
                self.cy,
                settings.FOV // 2,
                (255, 255, 255, 255)
            )

            draw_fps(3, 3)
        
        end_drawing()


overlay = Overlay('aimlab_tb')