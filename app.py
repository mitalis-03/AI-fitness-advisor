import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import cv2
import numpy as np
from detector import PoseDetector
from voice import speak
import mediapipe as mp

st.set_page_config(layout="wide")
st.title("🏋️ AI Fitness Advisor")
pose_type = st.selectbox("Select Activity", ["Squats", "Push-Ups", "Lunges", "Tadasana", "TreePose", "Meditation"])

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

class VideoProcessor(VideoTransformerBase):
    def __init__(self):
        self.detector = PoseDetector(pose_type)

    def transform(self, frame):
        image = frame.to_ndarray(format="bgr24")
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.detector.pose.process(image_rgb)

        if results.pose_landmarks:
            landmarks = [(lm.x, lm.y) for lm in results.pose_landmarks.landmark]
            feedback = self.detector.detect_pose(image, landmarks)
            cv2.putText(image, feedback, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            if "✅" in feedback:
                speak("Correct Pose")

        return image

webrtc_streamer(key="ai-fitness", video_transformer_factory=VideoProcessor)
