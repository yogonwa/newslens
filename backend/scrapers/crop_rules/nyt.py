from PIL import Image
from . import BaseCropper, CropDimensions, CropMetadata

class NYTimesCropper(BaseCropper):
    """
    New York Times-specific cropping implementation
    
    Layout:
    - Header/navigation ends at 710px
    - Main content area extends 2000px below header
    - Uses standard 3000px width for modern layout
    """
    
    def __init__(self):
        super().__init__(source_key="nytimes.com")
        self.crop_top = 710      # Skip header and navigation
        self.crop_height = 2000  # Capture main content area
        self.target_width = 3000 # Standard width for content view
        
    def get_crop_dimensions(self, image: Image.Image) -> CropDimensions:
        """
        Get NYT-specific crop dimensions.
        
        Args:
            image: PIL Image to be cropped
            
        Returns:
            CropDimensions configured for NYT layout
        """
        return CropDimensions(
            top=self.crop_top,
            height=self.crop_height,
            target_width=self.target_width
        )
        
    def validate_crop(self, cropped: Image.Image, metadata: CropMetadata) -> bool:
        """
        Validate NYT-specific crop requirements.
        
        Args:
            cropped: The cropped PIL Image
            metadata: Metadata about the crop operation
            
        Returns:
            bool indicating if crop meets NYT requirements
        """
        # First check base requirements
        if not self._validate_base_requirements(cropped, metadata):
            return False
            
        # Verify we didn't exceed original image bounds
        orig_height = metadata.original_dimensions[1]
        if metadata.crop_dimensions.top + metadata.crop_dimensions.height > orig_height:
            logger.warning(f"NYT: Crop would exceed image bounds ({orig_height}px)")
            return False
            
        return True 