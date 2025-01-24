from PIL import Image

LUMIX_FONT_HEAD = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400..900&display=swap" rel="stylesheet">
"""

NIKON_FONT_HEAD = """
<script type="text/javascript">
    MathJax = {
    tex: {
    inlineMath: [['$', '$'], ['\\(', '\\)']],
    displayMath: [['$$', '$$'], ['\\[', '\\]']]
    },
    svg: {
    fontCache: 'global'
    }
    };
    </script>
  <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
"""

CANON_FONT_HEAD = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Crimson+Pro:ital,wght@0,200..900;1,200..900&family=Exo+2:ital,wght@0,100..900;1,100..900&display=swap" rel="stylesheet">
"""

SONY_FONT_HEAD = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Exo+2:ital,wght@0,100..900;1,100..900&family=Spectral:ital,wght@0,200;0,300;0,400;0,500;0,600;0,700;0,800;1,200;1,300;1,400;1,500;1,600;1,700;1,800&display=swap" rel="stylesheet">
"""

OEM_LOGOS = {
    "Panasonic": "lumix.png",
    "Nikon": "nikon.svg",
    "Canon": "canon.svg",
    "SONY": "sony.png",
}

OEM_FONTS = {  # Make logo, Model logo
    "Panasonic": ["Arial Black", "Orbitron"],
    "Nikon": ["Arial Black", "Cambria"],  # Arial italic + Jax
    "Canon": ["Crimson Pro", "Exo 2"],
    "SONY": ["Spectral", "Exo 2"],  # Spectral squashed
}

OEM_FONT_HEADS = {
    "Panasonic": LUMIX_FONT_HEAD,
    "Nikon": NIKON_FONT_HEAD,
    "Canon": CANON_FONT_HEAD,
    "SONY": SONY_FONT_HEAD,
}


class TemplateGenerator:
    def __init__(self, metadata, img_path):
        if metadata["Make"] not in OEM_LOGOS:
            raise Exception(f"OEM {metadata['Make']} not supported")
        self.metadata = metadata
        self.img_path = img_path
        self.width, self.height = Image.open(img_path).size
        self.make = metadata["Make"]
        self.model = metadata["Model"]

    def _gen_head(self):
        return f"""
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={self.width + 200}, initial-scale=1.0" />
    <title>Document</title>
    {OEM_FONT_HEADS[self.metadata["Make"]]}
  </head>
"""

    def _gen_img(self, img_path):
        return f"""
<body style="background-color: white">
    <div
      class="container"
      style="
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        position: absolute;
        top: 0;
        width: {self.width}px;
        padding: 100px;
      "
    >
      <img
        src="{img_path}"
        style="object-fit: cover; margin-bottom: 50px"
      />
"""

    def _gen_camera(self):
        return f"""
<div
        class="info"
        style="
          font-size: 50px;
          display: flex;
          flex-direction: row;
          justify-content: space-between;
          width: inherit;
          margin-bottom: 10px;
        "
      >
        <div
          class="left"
          style="display: flex; flex-direction: row; align-items: center; justify-content: center"
        >
          <img
            src="sprites/outputs/{OEM_LOGOS[self.make]}"
            style="height: {"80px" if self.make != "Nikon" else "100px"}; object-fit: contain"
          />
          <span style="margin-left: 25px; display: flex; flex-direction: column; align-items: baseline; justify-content: center">
            <span
              style="
                font-family: '{OEM_FONTS[self.make][0]}', sans-serif;
                {'font-style: italic;' if self.make == 'Nikon' else ''}
                {'transform: scaleY(0.85); ' if self.make == 'SONY' else ''}
                font-size: 40px;
                font-weight: bold;
              "
              >{self.make}
            </span>
            <span style="font-family: '{OEM_FONTS[self.make][1]}', sans-serif; margin-left: 25px;"
              >{self.model if self.make != 'Nikon' else f'${chr(92)}mathbb{{{self.model[0]}}}${self.model[1:]}'}</span
            >
          </span>
        </div>
"""

    def _gen_lens(self):
        if "LensModel" in self.metadata:
            lens_info = f"""
<div class="lens" style="font-family: '{OEM_FONTS[self.make][1]}', sans-serif">{self.metadata['LensModel']}</div>
"""
        else:
            lens_info = ""
        if "ExposureTime" in self.metadata:
            exposure_time = self.metadata['ExposureTime'] if self.metadata['ExposureTime'] > 1 else f'1&frasl;{round(1 / self.metadata["ExposureTime"])}'
        else:
            exposure_time = "--"
        return f"""
        <div
          class="right"
          style="
            display: flex;
            flex-direction: column;
            align-items: flex-end;
            justify-content: center;
            font-family: Cambria, Cochin, Georgia, Times, 'Times New Roman',
              serif;
          "
        >
          {lens_info}
          <div class="params" style="font-size: 40px;">
            <span>{int(self.metadata["FocalLength"]) if "FocalLength" in self.metadata else "--"}mm</span>
            <span style="margin-left: 25px;">F{self.metadata['FNumber'] if "FNumber" in self.metadata else "--"}</span>
            <span style="margin-left: 25px;">ISO{self.metadata['ISOSpeedRatings'] if "ISOSpeedRatings" in self.metadata else "--"}</span>
            <span style="margin-left: 25px;">{exposure_time}\"</span> 
          </div>
        </div>
      </div>
      <div class="datetime" style="font-size: 30px; color: gray; align-self: center;">
        <span>{self.metadata["DateTimeOriginal"]}</span>
      </div>
    </div>
  </body>
</html>
"""

    def generate(self):
        head = self._gen_head()
        img = self._gen_img(self.img_path)
        camera = self._gen_camera()
        lens = self._gen_lens()
        return head + img + camera + lens
