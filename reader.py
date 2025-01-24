from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime

EXIF_TAGS = ["Make", "Model", "DateTimeOriginal", "FNumber", "ExposureTime", "ISOSpeedRatings", "FocalLength", "LensModel"]

class Reader:
    def __init__(self, path):
        self.path = path
        self.image = Image.open(path)
        self.exif_data = self._read_exif()
        print(self.exif_data)
        
    
    def _read_exif(self):
        self.exif_data = self.image._getexif()
        if not self.exif_data:
            raise ValueError("No EXIF data found in the image")
        exif_data = {}
        for k, v in self.exif_data.items():
            tag = TAGS.get(k, k)
            if isinstance(v, bytes):
                continue
            # print(tag, v)
            if tag in EXIF_TAGS:
                exif_data[tag] = v.strip() if isinstance(v, str) else v
        # Align make and model
        if exif_data["Make"] == "NIKON CORPORATION":
            exif_data["Make"] = "Nikon"
            exif_data["Model"] = exif_data["Model"].split(" ", maxsplit=1)[1]
        # Align date and time
        parsed = datetime.strptime(exif_data["DateTimeOriginal"], "%Y:%m:%d %H:%M:%S")
        exif_data["DateTimeOriginal"] = parsed.strftime("%d %b %Y, %H:%M")
        return exif_data


if __name__ == "__main__":
    reader = Reader("./P1000030.JPG")
   