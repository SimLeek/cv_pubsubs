import warnings

import cv2
import pubsub
import numpy as np

from .winctrl import WinCtrl
from ..listen_default import listen_default
from ..webcam_pub.camctrl import CamCtrl

if False:
    from typing import List, Union, Callable, Any
    import numpy as np


class SubscriberWindows(object):
    frame_dict = {}

    esc_key_codes = [27]  # ESC key on most keyboards

    def __init__(self,
                 window_names=('cvpubsubs',),  # type: List[str]
                 video_sources=(0,),  # type: List[Union[str,int]]
                 callbacks=(None,),  # type: List[Callable[[List[np.ndarray]], Any]]
                 ):
        self.window_names = window_names
        self.source_names = []
        for name in video_sources:
            if len(str(name))<=1000:
                self.source_names.append(str(name))
                self.input_vid_global_names = [str(name) + "frame" for name in video_sources]
            elif isinstance(name, np.ndarray):
                self.source_names.append(str(hash(str(name))))
                self.input_vid_global_names = [str(hash(str(name))) + "frame" for name in video_sources]
            else:
                raise ValueError("Input window name too long.")

        self.callbacks = callbacks
        self.input_cams = video_sources


    @staticmethod
    def set_global_frame_dict(name, *args):
        if len(str(name)) <= 1000:
            SubscriberWindows.frame_dict[str(name) + "frame"] = [*args]
        elif isinstance(name, np.ndarray):
            SubscriberWindows.frame_dict[str(hash(str(name))) + "frame"] = [*args]
        else:
            raise ValueError("Input window name too long.")


    def __stop_all_cams(self):
        for c in self.source_names:
            CamCtrl.stop_cam(c)

    def handle_keys(self,
                    key_input,  # type: int
                    ):
        if key_input in self.esc_key_codes:
            for name in self.window_names:
                cv2.destroyWindow(name + " (press ESC to quit)")
            WinCtrl.quit()
            self.__stop_all_cams()
            return 'quit'
        elif key_input not in [-1, 0]:
            try:
                WinCtrl.key_stroke(chr(key_input))
            except ValueError:
                warnings.warn(
                    RuntimeWarning("Unknown key code: [{}]. Please report to cv_pubsubs issue page.".format(key_input))
                )

    def update_window_frames(self):
        win_num = 0
        for i in range(len(self.input_vid_global_names)):
            if self.input_vid_global_names[i] in self.frame_dict and self.frame_dict[
                self.input_vid_global_names[i]] is not None:
                if len(self.callbacks)>0 and self.callbacks[i % len(self.callbacks)] is not None:
                    frames = self.callbacks[i % len(self.callbacks)](self.frame_dict[self.input_vid_global_names[i]])
                else:
                    frames = self.frame_dict[self.input_vid_global_names[i]]
                for f in range(len(frames)):
                    cv2.imshow(self.window_names[win_num % len(self.window_names)] + " (press ESC to quit)", frames[f])
                    win_num += 1

    # todo: figure out how to get the red x button to work. Try: https://stackoverflow.com/a/37881722/782170
    def loop(self):
        sub_cmd = pubsub.subscribe("CVWinCmd")
        msg_cmd = ''
        while msg_cmd != 'quit':
            self.update_window_frames()
            msg_cmd = self.handle_keys(cv2.waitKey(1))
            if not msg_cmd:
                msg_cmd = listen_default(sub_cmd, block=False, empty='')
        WinCtrl.quit()
        self.__stop_all_cams()
