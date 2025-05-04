import pytest
from PIL import Image
from backend.scrapers.crop_rules.cnn import CNNCropper
from backend.scrapers.crop_rules.nyt import NYTimesCropper
from backend.scrapers.crop_rules.fox import FoxNewsCropper
from backend.scrapers.crop_rules.usatoday import USATodayCropper
from backend.scrapers.crop_rules.wapo import WaPostCropper
from backend.scrapers.crop_rules import CropMetadata
import os

TEST_IMAGE_DIR = os.path.join(os.path.dirname(__file__), "images")

@pytest.mark.parametrize("cropper_cls, image_file", [
    (CNNCropper, "cnn.png"),
    (NYTimesCropper, "nytimes.png"),
    (FoxNewsCropper, "fox.png"),
    (USATodayCropper, "usatoday.png"),
    (WaPostCropper, "wapo.png"),
])
def test_crop_and_validate(cropper_cls, image_file):
    image_path = os.path.join(TEST_IMAGE_DIR, image_file)
    image = Image.open(image_path)
    cropper = cropper_cls()
    cropped, metadata = cropper.crop(image)
    assert cropped.width == cropper.target_width
    assert cropped.height > 0
    assert isinstance(metadata, CropMetadata)
    assert cropper.validate_crop(cropped, metadata)

    # Save output for visual inspection
    output_dir = os.path.join(os.path.dirname(__file__), "crop_outputs")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{cropper_cls.__name__}_{image_file}")
    cropped.save(output_path)


def test_crop_error_handling():
    cropper = CNNCropper()
    # Create a tiny image that will fail validation
    image = Image.new("RGB", (100, 100), color="white")
    with pytest.raises(Exception):
        cropper.crop(image) 