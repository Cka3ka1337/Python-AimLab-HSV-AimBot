import sys


class Settings:
    def __init__(self) -> None:
        self.is_running = True
        self.frame_rate_limit = 128
        self.show_capture_frames = False
        self.overide_sleep_bind = 0x14
        self.min_size = 20
        
        self.FOV = 416
        self.scale = 0.2
        self.work_triggerbot = True
        
        self.aimbot_bind = 0x12
        self.work_aimbot = True
        self.aimbot_always_work = True
        
        self.reflex_on = False
        self.visuals_on = True
        
        
        args = sys.argv[1:]
        print(args)
        for i in range(len(args) // 2):
            attr = args[::2][i].replace('-', '')
            
            value = args[1::2][i]
            
            if value.lower() == 'true':
                value = True
            elif value.lower() == 'false':
                value = False
            elif '.' in value:
                value = float(value)
            else:
                value = int(value)
            
            setattr(self, attr, value)


settings = Settings()
