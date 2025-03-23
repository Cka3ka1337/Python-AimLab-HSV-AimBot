import win32api
import win32gui
import win32con

from numpy import array

from settings import settings
from capture import OBS, MSS
from overlay import overlay
from cv_detect import CV
from mouse import Mouse


def main():
    # 2 метода захвата на выбор:
    # cap = OBS(0, 'CAP_DSHOW') # Предварительно необходимо настроить OBS камеру.
    cap = MSS()
    
    cv = CV(array([0,199,50]), array([100,255,255]), settings.min_size)
    mouse = Mouse()
    
    while overlay.is_alive and settings.is_running and not win32api.GetAsyncKeyState(win32con.VK_PAUSE):
        frame = cap.get_frame()
        bboxes = cv.find_objects(frame=frame)
        overlay.render(bboxes)

        if bboxes and win32gui.GetWindowText(win32gui.GetForegroundWindow()) == 'aimlab_tb':
            mouse(bboxes[0])

    settings.is_running = False
    
    try:
        overlay.close()
    except:
        pass


if __name__ == '__main__':
    main()