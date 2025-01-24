import cv2
from PIL import Image
import numpy as np


class Sprite:
    def __init__(self, path):
        self.image = np.array(Image.open(path))
        # print(self.image)
    
    def pad(self, size: int, color: tuple):
        self.image = cv2.copyMakeBorder(self.image, size, size, size, size, cv2.BORDER_CONSTANT, value=[*color, 255])

    def fit(self, size: int):
        longer_side = max(self.image.shape[:2])
        ratio = size / longer_side
        self.image = Image.fromarray(self.image).resize((int(self.image.shape[1] * ratio), int(self.image.shape[0] * ratio)), Image.Resampling.LANCZOS)
        self.image = np.array(self.image)

    def fill(self, color: tuple):
        indexes = np.where(self.image[..., -1] != 0)
        self.image[indexes[0], indexes[1], :3] = color
        print(self.image)
    
    def downsample(self, factor: int):
        self.image = Image.fromarray(self.image).resize((self.image.shape[1] // factor, self.image.shape[0] // factor), Image.Resampling.LANCZOS)
        self.image = np.array(self.image)

    def save(self, path):
        Image.fromarray(self.image).save(path)

if __name__ == "__main__":
    sprite = Sprite(r"outputs/P1000002.JPG_m.png")
    sprite.downsample(2)
    sprite.save("P1000002.JPG_m.png")        