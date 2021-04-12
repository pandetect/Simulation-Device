import argparse 
import socket
import time
import threading
import cv2
import numpy as np
import io
from PIL import Image
while True:
    cv2.imshow('Frame', np.random.normal(0 , 100 , (28 , 28 , 3)))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()