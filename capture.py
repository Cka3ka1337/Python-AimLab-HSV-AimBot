import threading

import cv2
import mss
import numpy

import overlay

from settings import settings


class Capture:
    def __init__(self):
        self.frame = None
        
        self.start_w = 0
        self.end_w = 100
        self.start_h = 0
        self.end_h = 100

    
    def init(self, cap_thr_name=None) -> None:
        if cap_thr_name:
            threading.Thread(target=cap_thr_name, daemon=False).start()
            while self.frame is None: pass
        
        
        _, _, w, h = overlay.overlay.get_window_info()
        frame = self.frame
        
        h, w, _ = frame.shape
        
        self.start_w = w // 2 - settings.FOV // 2
        self.end_w = w // 2 + settings.FOV // 2
        self.start_h = h // 2 - settings.FOV // 2
        self.end_h = h // 2 + settings.FOV // 2

    
    def show_frame(self, frame) -> None:
        cv2.imshow('Capture', frame)
        if cv2.waitKey(1) == ord('q'):
            cv2.destroyAllWindows()
            settings.show_capture_frames = False
    
    
    def get_frame(self) -> None:
        return self.frame    


class OBS(Capture):
    def __init__(self, cam_id: int, backend: str='CAP_DSHOW') -> None:
        '''
        VALID BACKENDS:
            CAP_ANY                       # 82 FPS
            CAP_DSHOW                   # 120+ FPS
            CAP_INTELPERC_DEPTH_MAP       # 80 FPS
            CAP_MSMF                      # 89 FPS
            CAP_OBSENSOR_DEPTH_MAP        # 85 FPS
            CAP_OPENNI_DEPTH_MAP          # 78 FPS
            CAP_OPENNI_VGA_30HZ           # 90 FPS
            CAP_PROP_POS_MSEC             # 80 FPS
            CAP_PVAPI_FSTRIGMODE_FREERUN  # 83 FPS
        '''
        
        super().__init__()
        
        self.cap = cv2.VideoCapture(cam_id, getattr(cv2, backend))
        self.cap.set(cv2.CAP_PROP_FPS, 0)
        
        _, _, w, h = overlay.overlay.get_window_info()
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, w)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)
        self.init(self.__thr)
        
        
    
    def get_valid_backends(self, cam_idx) -> None:
        self.cap.release()
        
        attrs = [x for x in cv2.__dict__ if 'CAP_' in x]
        valid = []
        for i in attrs:
            self.cap = cv2.VideoCapture(cam_idx, getattr(cv2, i))
            try:
                self.get_frame()
                valid.append(i)
                print(f'Valid: {i}')
            except:
                print(f'Invalid: {i}')
            self.cap.release()
        
        print(*valid, sep='\n')
        
        settings.is_running = False
    
    
    def __thr(self) -> None:
        while True:
            _, self.frame = self.cap.read()
    
    
    def get_frame(self) -> numpy.array:
        frame = self.frame.copy()[self.start_h:self.end_h, self.start_w:self.end_w]
        
        if settings.show_capture_frames:
            self.show_frame(frame)
            
        return frame


class MSS(Capture):
    def __init__(self) -> None:
        super().__init__()
        settings.visuals_on = False
        
        self.init(self.__thr)
  
    
    def __thr(self) -> None:
        with mss.mss() as sct:
            while True:
                x, y, w, h = overlay.overlay.get_window_info()
                self.frame = numpy.array(sct.grab((x, y, x + w, y + h)))
    
    
    def get_frame(self) -> numpy.array:
        frame = self.frame.copy()[self.start_h:self.end_h, self.start_w:self.end_w]
        
        if settings.show_capture_frames:
            self.show_frame(frame)
            
        return frame