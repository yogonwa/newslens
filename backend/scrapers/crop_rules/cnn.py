from PIL import Image
from . import BaseCropper, CropDimensions, CropMetadata

class CNNCropper(BaseCropper):
    """
    CNN-specific cropping implementation
    
    Layout:
    - Header/navigation ends at 552px
    - Main content area extends 2000px below header
    - Uses standard 3000px width for modern layout
    """
    
    def __init__(self):
        super().__init__(source_key="cnn.com")
        # Dimensions calibrated for CNN's layout
        self.crop_top = 552      # Skip header and navigation
        self.crop_height = 2000  # Increased from 1080 to capture more content
        
    def get_crop_dimensions(self, image: Image.Image) -> CropDimensions:
        """
        Get CNN-specific crop dimensions.
        
        Args:
            image: PIL Image to be cropped
            
        Returns:
            CropDimensions configured for CNN layout
        """
        return CropDimensions(
            top=self.crop_top,
            height=self.crop_height,
            target_width=self.target_width
        )
        
    def validate_crop(self, cropped: Image.Image, metadata: CropMetadata) -> bool:
        """
        Validate CNN-specific crop requirements.
        
        Args:
            cropped: The cropped PIL Image
            metadata: Metadata about the crop operation
            
        Returns:
            bool indicating if crop meets CNN requirements
        """
        # First check base requirements
        if not self._validate_base_requirements(cropped, metadata):
            return False
            
        # Verify we didn't exceed original image bounds
        orig_height = metadata.original_dimensions[1]
        if metadata.crop_dimensions.top + metadata.crop_dimensions.height > orig_height:
            logger.warning(f"CNN: Crop would exceed image bounds ({orig_height}px)")
            return False
            
        return True 