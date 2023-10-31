import cv2
from google.protobuf.json_format import MessageToDict
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.camera import Camera
import mediapipe as mp



class CameraOpenCv(Camera):
    """Componente que carga la camara usando opencv"""
    def __init__(self, hasFacialRecognition = False, hasHandsRecognition = False, **kwargs):
        super(CameraOpenCv, self).__init__(play = False,**kwargs)
        self.frame = None
        self.hasFacialRecognition = hasFacialRecognition
        self.hasHandsRecognition = hasHandsRecognition
        self._mp_hands_detection = mp.solutions.hands
        self._mp_face_detection = mp.solutions.face_detection
        self._capture = cv2.VideoCapture(0)
        self._schedule = None

    def on_enter(self):
        print("Video abierto")
        self.start_video()

    def on_leave(self):
        print("video parado")
        self.stop_video()

    def start_video(self, *args):
        self._schedule = Clock.schedule_interval(self.load_video, 1 / 60)

    def stop_video(self, *args):

        if not self._schedule:
            return
        self._schedule.cancel()


    def load_video(self, *args):
        ret, frame = self._capture.read()
        if not ret:
            return
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        if self.hasHandsRecognition:
            with self._mp_hands_detection.Hands() as hands_detection:
                results = hands_detection.process(frame_rgb)
                height, width, _ = frame.shape
                if results.multi_hand_landmarks is not None:
                    # Dibujando los puntos y las conexiones mediante mp_drawing
                    for (hand_landmarks, handedness) in zip(results.multi_hand_landmarks, results.multi_handedness):
                        y_1 = int(hand_landmarks.landmark[self._mp_hands_detection.HandLandmark.WRIST].y * height)
                        y_2 = int(hand_landmarks.landmark[self._mp_hands_detection.HandLandmark.MIDDLE_FINGER_TIP].y * height)
                        x_1 = int(hand_landmarks.landmark[self._mp_hands_detection.HandLandmark.THUMB_TIP].x * width)
                        x_2 = int(hand_landmarks.landmark[self._mp_hands_detection.HandLandmark.PINKY_DIP].x * width)
                        cv2.rectangle(frame, (x_1, y_1), (x_2, y_2), (0, 255, 0), 1)

                        x_text = min([x_1, x_2])
                        y_text = max([y_1, y_2]) + 5
                        font = cv2.FONT_HERSHEY_SIMPLEX
                        tipo_mano = MessageToDict(handedness)["classification"][0]["label"]

                        if tipo_mano == "Right":
                            cv2.putText(frame, 'Derecha', (x_text, y_text), font, 1, (0, 255, 255), 2, cv2.LINE_AA)
                        else:
                            cv2.putText(frame, 'Izquierda', (x_text, y_text), font, 1, (0, 255, 255), 2, cv2.LINE_AA)
        if self.hasFacialRecognition:
            with self._mp_face_detection.FaceDetection() as face_detection:
                results = face_detection.process(frame_rgb)
                height, width, _ = frame.shape
                if results.detections:
                    for detection in results.detections:
                        xmin = int(detection.location_data.relative_bounding_box.xmin * width)
                        ymin = int(detection.location_data.relative_bounding_box.ymin * height)
                        xmax = xmin + int(detection.location_data.relative_bounding_box.width * width)
                        ymax = ymin + int(detection.location_data.relative_bounding_box.height * height)
                        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 1)
                        font = cv2.FONT_HERSHEY_SIMPLEX
                        cv2.putText(frame, 'Cara', (xmin, ymax), font, 1, (0, 255, 255), 2, cv2.LINE_AA)
        frame = cv2.flip(frame, 0)
        buffer = frame.tobytes()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt="bgr")
        texture.blit_buffer(buffer, colorfmt="bgr", bufferfmt="ubyte")
        self.texture = texture
        frame = cv2.flip(frame, 0)
        self.frame = frame
