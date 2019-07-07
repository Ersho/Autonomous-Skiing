import numpy as np
import cv2

def threshold(frame, smooth = True):
    
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    
    if smooth:
        frame = cv2.GaussianBlur(frame, (3,3), 0.1 )
        
    ret, thrsh = cv2.threshold(frame, 120, 255, cv2.THRESH_BINARY)
    
    return thrsh

def edge_detection(frame,
                   low_threshold = 100, 
                   high_threshold = 200):
    
    frame = cv2.Canny(frame,  threshold1 = 200, threshold2=300)

    return frame

def region_of_intereset(frame, *args):
    
    mask = np.zeros_like(frame)
    cv2.fillPoly(mask, args, 255)
    masked = cv2.bitwise_and(frame, mask)
    
    return masked

def crop_region_of_intereset(frame, args):
    
    frame = frame[args[0]:args[1], args[2]:args[3]]
    
    return frame

def get_center_coords(binary_img):
    # Identify nonzero pixels
    ypos, xpos = binary_img.nonzero()
    # Calculate pixel positions with reference to the rover position being at the 
    # center bottom of the image.  
    x_pixel = -(ypos - binary_img.shape[0]).astype(np.float)
    y_pixel = -(xpos - binary_img.shape[1]/2 ).astype(np.float)
    
    return x_pixel, y_pixel

def perspect_transform(frame):
           
    dst_size = 5 
    bottom_offset = 6
    #src = np.float32([[14, 140], [301 ,140],[200, 96], [118, 96]])
    #src = np.float32([[0,0], [400,0], [400,1000], [0, 1000]])
    src = np.float32([[0,0], [849,0], [0,400], [849, 400]])
    dst = np.float32([[frame.shape[1]/2 - dst_size, frame.shape[0] - bottom_offset],
                      [frame.shape[1]/2 + dst_size, frame.shape[0] - bottom_offset],
                      [frame.shape[1]/2 + dst_size, frame.shape[0] - 2*dst_size - bottom_offset], 
                      [frame.shape[1]/2 - dst_size, frame.shape[0] - 2*dst_size - bottom_offset],
    ])
    
    M = cv2.getPerspectiveTransform(src, dst)
    warped = cv2.warpPerspective(frame, M, (frame.shape[1], frame.shape[0]))# keep same size as input image
    
    return warped

def to_polar_coords(x_pixel, y_pixel):
    # Convert (x_pixel, y_pixel) to (distance, angle) 
    # in polar coordinates in rover space
    # Calculate distance to each pixel
    dist = np.sqrt(x_pixel**2 + y_pixel**2)
    # Calculate angle away from vertical for each pixel
    angles = np.arctan2(y_pixel, x_pixel)
    return dist, angles
