from ultralytics import YOLO
import utillitary as ut

class pose_detector:

    def __init__(self):

        self.model = YOLO('synth.pt')

    def process_frame(self, frame):

        results = self.model(frame, stream=True, verbose=False)

        for r in results:

            annotated_frame = r.plot()

            if r.keypoints is not None and len(r.keypoints.xy) > 0:

                if len(r.keypoints.xy[0].tolist()) == 3:

                    base_vector = ut.calc_vector(r.keypoints.xy[0].tolist()[1], r.keypoints.xy[0].tolist()[2])
                    needle_vector = ut.calc_vector(r.keypoints.xy[0].tolist()[1], r.keypoints.xy[0].tolist()[0])
                    valor = round(ut.interpolate(ut.calc_angle(base_vector, needle_vector)))
                    #In order to read the manometer, we use two vectors based on three pose points: the base, the center and the tip of the manometer

                    return annotated_frame, valor

                else: return frame, -1
                
            else: return frame, -1