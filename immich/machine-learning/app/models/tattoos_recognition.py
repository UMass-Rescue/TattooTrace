from io import BytesIO
from pathlib import Path
from typing import Any

import cv2
import numpy as np
import torch
from numpy.typing import NDArray
from typing import Any, Literal

from app.config import clean_name, log
from app.schemas import Face, ModelType, is_ndarray

from .base import InferenceModel
import base64
from app.schemas import ModelType, RecognizedTattoos

from .base import InferenceModel

from PIL import Image
from ultralytics import YOLO
from pathlib import Path
import os

class TattoosRecognition(InferenceModel):
    _model_type = ModelType.TATTOOS_RECOGNITION

    def __init__(
        self,
        model_name: str,
        cache_dir: Path | str | None = None,
        mode: Literal["image", "video"] | None = None,
        **model_kwargs: Any,
    ) -> None:
        self.mode = mode
        super().__init__(model_name, cache_dir, **model_kwargs)

    def _load(self) -> None:
        if self.mode == "image" or self.mode is None:
            log.debug(f"Loading model '{self.model_name}'")
            self.image_model = None
            log.debug(f"Loaded model '{self.model_name}'")

        if self.mode == "video" or self.mode is None:
            log.debug(f"Loading model '{self.model_name}'")
            self.video_model = None
            log.debug(f"Loaded model '{self.model_name}'")

    def _predict(self, image: NDArray[np.uint8] | str) -> NDArray[np.float32]:
        if isinstance(image, bytes):
            decoded_image = cv2.imdecode(np.frombuffer(image, np.uint8), cv2.IMREAD_COLOR)
        else:
            decoded_image = image

        # Encode image to base64 string
        _, buffer = cv2.imencode('.jpg', decoded_image)
        encoded_string = base64.b64encode(buffer).decode('utf-8')

        outputs = []
        tattoo: RecognizedTattoos = {
                "image": "data:image/jpeg;base64," + encoded_string,  # Prefix with data URI"
                "score": 0.3
            }
        outputs.append(tattoo)

        return outputs

    def configure(self, **model_kwargs: Any) -> None:
        self.det_model.det_thresh = model_kwargs.pop("minScore", self.det_model.det_thresh)


class TattooDetector:
    def __init__(self):
        model_path = './app/models/best.pt'
        #model_path = './yolov5m.pt'
        self.initialize_model(model_path)


    def run_prediction_image(self, image):
        prediction_result = self.model(image)
        return prediction_result 
    

    def run_image_prediction_byte_stream(self, image, asset_id, save_directory, confidence):
        file_path = save_directory / f"{asset_id}.jpg"
        recognition_made = False

        if file_path.exists():
            tattoo_recognition_res = {
                "filePath": str(file_path)
            }
        else:
            if isinstance(image, bytes):
                image = cv2.imdecode(np.frombuffer(image, np.uint8), cv2.IMREAD_COLOR)
                recognition_result = self.run_prediction_image(image)
                print(recognition_result)
                recognition_result.render()  # Update images with bounding boxes and labels
                recognition_made = bool(len(recognition_result.xyxy[0]))  # Check if any detections were made

                # Convert the last image to base64 format
                buffered = BytesIO()
                im_rgb = cv2.cvtColor(recognition_result.ims[-1], cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
                im_base64 = Image.fromarray(im_rgb)
                im_base64.save(buffered, format="JPEG")
                recognized_image_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

                # Decode the base64 image back into a numpy array
                recognized_image = cv2.imdecode(np.fromstring(base64.b64decode(recognized_image_base64), dtype=np.uint8), cv2.IMREAD_COLOR)
            else:
                recognized_image = image

            if asset_id and recognition_made:
                cv2.imwrite(str(file_path), recognized_image)

                tattoo_recognition_res = {
                    "filePath": str(file_path)
                }
            else:
                tattoo_recognition_res = {
                    "filePath": ""
                }

        return tattoo_recognition_res


    def run_prediction_video(self, video_path, save_directory, confidence=0.2):
        video_save_file_path = save_directory / f"detected_{video_path.name}"
        recognition_made = False 

        if not video_save_file_path.exists():
            recognition_made = self.predict_video(str(video_path), str(video_save_file_path), confidence)

        if recognition_made:
            tattoo_recognition_res = {
                "filePath": str(video_save_file_path)
            }
        else:
             tattoo_recognition_res = {
                "filePath": ""
            }
       
        return tattoo_recognition_res
        
        
    def predict_video(self, video_path, output_path, confidence):
        video_cap = cv2.VideoCapture(str(video_path))
        fps = video_cap.get(cv2.CAP_PROP_FPS)
        frame_size = (int(video_cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        recognition_made = False

        out = cv2.VideoWriter(output_path, fourcc, fps, frame_size)

        ret = True 
        while ret:
            ret, frame = video_cap.read()

            if ret:
                results = self.model.predict(frame)
                # Process the results to get bounding boxes, labels, and confidence scores
                # Draw the bounding boxes and labels on the frame
                out.write(frame)

                if recognition_made is False:
                    recognition_made = bool(len(results))

        video_cap.release()
        out.release()

        # if no tattoos are detected, delete the processed video
        if recognition_made is False:
            os.remove(output_path)

        return recognition_made


    def run_prediction_bitstream_deprecated(self, byte_image, save_path=None):
        reconstructed_image = Image.open(byte_image)
        prediction_result = self.run_prediction_image(reconstructed_image)[0]

        if save_path:
            recognition_image = self.create_recognized_image(prediction_result, save_path)
            print (f"Recognition saved at {save_path}")

        return prediction_result, recognition_image


    def create_recognized_image(self, recognized_result, save_path):
        """ Saves the thumbnails of detection
        """
        return recognized_result.plot(save=True, filename=save_path)
         

    def initialize_model(self, model_path):
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path, force_reload=True)

