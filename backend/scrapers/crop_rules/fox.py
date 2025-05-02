from PIL import Image
from . import MultiRegionCropper, CropRegion, CropMetadata
from typing import List

class FoxNewsCropper(MultiRegionCropper):
    """
    Fox News-specific cropping implementation
    
    Layout:
    - Header/navigation: 195-395px (200px height)
    - Advertisement section: Skipped
    - Main content: Starts at 1080px, extends 2000px
    - Regions are stitched together with white background
    """
    
    def __init__(self):
        super().__init__(source_key="foxnews.com")
        
        # Original measurements
        self.header_top = 195
        self.header_height = 200  # 195 to 395
        self.content_top = 1080
        self.content_height = 2000
        
    def get_regions(self) -> List[CropRegion]:
        """
        Get Fox News-specific crop regions.
        
        Returns:
            List of regions to crop:
            - Header region (195-395px)
            - Main content region (1080px+)
        """
        return [
            CropRegion(
                top=self.header_top,
                height=self.header_height,
                description="header"
            ),
            CropRegion(
                top=self.content_top,
                height=self.content_height,
                description="main_content"
            )
        ]
        
    def stitch_regions(self, regions: List[Image.Image]) -> Image.Image:
        """
        Stitch regions together with white background.
        
        Args:
            regions: List of cropped image regions
            
        Returns:
            Stitched image with white background between regions
        """
        if not regions:
            raise ValueError("No regions to stitch")
            
        # Calculate total height
        total_height = sum(region.height for region in regions)
        
        # Create new image with white background
        stitched = Image.new("RGB", (self.target_width, total_height), (255, 255, 255))
        
        # Stitch regions together
        current_y = 0
        for region in regions:
            stitched.paste(region, (0, current_y))
            current_y += region.height
            
        return stitched
        
    def validate_crop(self, cropped: Image.Image, metadata: CropMetadata) -> bool:
        """
        Validate Fox News-specific crop requirements.
        
        Args:
            cropped: The cropped PIL Image
            metadata: Metadata about the crop operation
            
        Returns:
            bool indicating if crop meets Fox News requirements
        """
        # First check base requirements
        if not self._validate_base_requirements(cropped, metadata):
            return False
            
        # Verify we got both required regions
        required_regions = {"header", "main_content"}
        if not all(region in metadata.regions_cropped for region in required_regions):
            logger.warning(f"Fox News: Missing required regions. Found: {metadata.regions_cropped}")
            return False
            
        return True 