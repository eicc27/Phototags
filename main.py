from templates.temp_gen import TemplateGenerator
from reader import Reader

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os


def add_metadata(src_folder_path, dst_folder_path):
    # init chrome driver
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument(
        "--hide-scrollbars"
    )  # Prevent scrollbars from appearing in the screenshot
    options.add_argument("--force-device-scale-factor=1")  # Ensure consistent scaling
    service = Service()
    driver = webdriver.Chrome(service=service, options=options)
    try:
        for file in os.listdir(src_folder_path):
            image_path = os.path.join(src_folder_path, file)
            reader = Reader(image_path)
            gen = TemplateGenerator(reader.exif_data, image_path)
            with open("index.html", "w") as f:
                f.write(gen.generate())
            driver.get(f"file://{os.path.abspath('index.html')}")
            width = driver.execute_script("return document.querySelector('.container').clientWidth;")
            height = driver.execute_script("return document.querySelector('.container').clientHeight;")
            print(width, height)
            driver.execute_cdp_cmd(
                "Emulation.setDeviceMetricsOverride",
                {
                    "width": width,
                    "height": height,  # Add padding to ensure no cropping
                    "deviceScaleFactor": 1,
                    "mobile": False,
                },
            )
            driver.save_screenshot(f"{dst_folder_path}/{file}_m.png")
    finally:
        driver.quit()


if __name__ == "__main__":
    add_metadata("./inputs", "./outputs")
