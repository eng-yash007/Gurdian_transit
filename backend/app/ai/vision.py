import os
import cv2
import numpy as np
from deepface import DeepFace
from typing import List

# Disable tf logging for cleaner console
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

class VisionEngine:
    MODEL_NAME = "ArcFace" # Produces 512-d embeddings compatible with our DB
    
    @staticmethod
    def extract_embedding(image_bytes: bytes) -> List[float]:
        """
        Takes raw image bytes (e.g. from a FastAPI UploadFile), detects the face, 
        and extracts the 512-d embedding vector.
        """
        # Convert bytes to numpy array then to cv2 image
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            raise ValueError("Could not decode image.")
            
        try:
            # represent() returns a list of dictionaries (one for each face detected)
            # enforce_detection=True will throw ValueError if no face is found
            results = DeepFace.represent(img_path=img, model_name=VisionEngine.MODEL_NAME, enforce_detection=True)
            
            if not results:
                raise ValueError("No face detected.")
                
            # Assume the most prominent face is the first one
            embedding = results[0]["embedding"]
            return embedding
            
        except Exception as e:
            raise ValueError(f"Face extraction failed: {str(e)}")
