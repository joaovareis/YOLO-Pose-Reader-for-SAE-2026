import yaml
import cv2
import numpy as np
import statistics as stats
from yolo_stream import pose_detector

#---- Constants

YAML_PATH = r"camera_info.yaml"

with open(YAML_PATH, 'r') as file:
    YAML_DATA = yaml.safe_load(file)

CAM_DIM = (YAML_DATA['image_width'], YAML_DATA['image_height'])

K = np.array(YAML_DATA['camera_matrix']['data']).reshape((3,3))
D = np.array(YAML_DATA['distortion_coefficients']['data']).reshape((1,5))

CAM_MAT, _ = cv2.getOptimalNewCameraMatrix(cameraMatrix=K,
                                                 distCoeffs= D,
                                                 imageSize=CAM_DIM,
                                                 alpha=1,
                                                 newImgSize=CAM_DIM,
                                                 centerPrincipalPoint=False)

MAP_X, MAP_Y = cv2.initUndistortRectifyMap(cameraMatrix=K,
                                           distCoeffs=D,
                                           R = None,
                                           newCameraMatrix = CAM_MAT,
                                           size=CAM_DIM,
                                           m1type=cv2.CV_16SC2)

#---- Helper methods

#---- Main 

def main():

    engine = pose_detector()
    reading_buffer = []
    median = str(0)

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAM_DIM[0])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,  CAM_DIM[1])

    while cap.isOpened():

        ret, frame = cap.read()

        if not ret: break

        undistorted_frame = cv2.remap(frame, MAP_X, MAP_Y, cv2.INTER_LINEAR)
        #Use mapping instead of CV2 undistort for faster processing

        annotated, reading = engine.process_frame(undistorted_frame)
        #Do the YOLO inference in another archive in order to keep main clean

        if reading != -1: reading_buffer.append(reading)
        #Discards unvalid readings

        if len(reading_buffer) == 5:
            #Calculates the median of the last 5 readings in order to minimize the pose fluctuation
            median = str(stats.median(reading_buffer))

            reading_buffer = []

        cv2.putText(
                annotated,
                median, 
                (50, 50),                   # XY position
                cv2.FONT_HERSHEY_SIMPLEX,   # Font
                1.0,                        # Font size
                (0, 255, 0),                # Color (BGR)
                2,                          # Line thickness
                cv2.LINE_AA                 # Anti-aliasing 
            )

        cv2.imshow("YOLO Pose + Reading", annotated)

        if cv2.waitKey(1) & 0xFF == 27: break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()



    

