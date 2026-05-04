from pathlib import Path
from urllib.request import urlretrieve
from django.core.management.base import BaseCommand

MODEL_URL = 'https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_full/float16/latest/pose_landmarker_full.task'

class Command(BaseCommand):
    help = 'Downloads the MediaPipe Pose Landmarker model into trainova/pose_models.'
    def handle(self, *args, **kwargs):
        target = Path(__file__).resolve().parents[2] / 'pose_models' / 'pose_landmarker.task'
        target.parent.mkdir(parents=True, exist_ok=True)
        self.stdout.write(f'Downloading model to {target} ...')
        urlretrieve(MODEL_URL, target)
        self.stdout.write(self.style.SUCCESS('MediaPipe pose model downloaded.'))
