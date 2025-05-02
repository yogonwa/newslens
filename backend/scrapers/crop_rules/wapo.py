from PIL import Image
from . import BaseCropper, CropDimensions, CropMetadata

class WaPostCropper(BaseCropper):
    """
    Washington Post-specific cropping implementation
    
    Layout:
    - Header/navigation/ads end at 810px
    - Main content area extends 1900px below header
    - Uses standard 3000px width for modern layout
    """
    
    def __init__(self):
        super().__init__(source_key="washingtonpost.com")
        self.crop_top = 810       # Skip header, nav, and ads
        self.crop_height = 1900   # Height of main content area
        
    def get_crop_dimensions(self, image: Image.Image) -> CropDimensions:
        """
        Get WaPo-specific crop dimensions.
        
        Args:
            image: PIL Image to be cropped
            
        Returns:
            CropDimensions configured for WaPo layout
        """
        return CropDimensions(
            top=self.crop_top,
            height=self.crop_height,
            target_width=self.target_width
        )
        
    def validate_crop(self, cropped: Image.Image, metadata: CropMetadata) -> bool:
        """
        Validate WaPo-specific crop requirements.
        
        Args:
            cropped: The cropped PIL Image
            metadata: Metadata about the crop operation
            
        Returns:
            bool indicating if crop meets WaPo requirements
        """
        # First check base requirements
        if not self._validate_base_requirements(cropped, metadata):
            return False
            
        # Verify total height makes sense
        if metadata.total_height < self.minimum_height:
            logger.warning(f"WaPo: Total height {metadata.total_height}px below minimum {self.minimum_height}px")
            return False
            
        return True 