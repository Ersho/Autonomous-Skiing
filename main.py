import numpy as np
import cv2
import time

from perception import *
from decision import *
from get_input import *

#vertices = np.array([[100,200],[1100,200],[1100,600],
#                     [100,600],
#                     ], np.int32)

vertices = [200,600,100,1100,]
move = Decision()

frame_num = 0

while True:
    
    start_time = time.time()
    
    frame = get_screen(50,50, 1000, 1000)
    # , , h, w
    
    frame = threshold(frame)
    #frame = edge_detection(frame)
    roi = crop_region_of_intereset(frame, vertices)
    #PressKey(W)
    #time.sleep(0.5)
    #ReleaseKey(W)
    
    wrap = perspect_transform(roi)
    xpix, ypix = get_center_coords(wrap)
    nav_dist, nav_angles = to_polar_coords(xpix, ypix)
    
    drive_angle = np.clip(np.mean(nav_angles * 180 / np.pi), -15, 15)
    
    #print(drive_angle)
    move.next_move(drive_angle)
    
    cv2.imshow('window',roi)
    cv2.imshow('wrap', wrap)
    
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
    
    frame_num +=1
    if frame_num > 1000:
        cv2.destroyAllWindows()
        break
    
    print(drive_angle, "FPS: ", 1.0 / (time.time() - start_time))