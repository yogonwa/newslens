from PIL import Image
from . import MultiRegionCropper, CropRegion, CropMetadata
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class USATodayRegion:
    """Defines a region to crop in USA Today layout"""
    top: int
    height: int
    description: str

class USATodayCropper(MultiRegionCropper):
    """
    USA Today-specific cropping implementation
    
    Layout:
    - Navigation: 130-287px (157px height)
    - Advertisement section: 575px (skipped)
    - Main content: Starts at 862px, extends 1800px
    - Regions are stitched together with white background
    """
    
    def __init__(self):
        super().__init__(source_key="usatoday.com")
        
        # Original measurements
        self.top_skip = 130
        self.nav_height = 157
        self.ad_height = 575
        self.body_start = self.top_skip + self.nav_height + self.ad_height
        self.content_height = 1800
        
    def get_regions(self) -> List[CropRegion]:
        """
        Get USA Today-specific crop regions.
        
        Returns:
            List of regions to crop:
            - Navigation region (130-287px)
            - Main content region (862px+)
        """
        return [
            CropRegion(
                top=self.top_skip,
                height=self.nav_height,
                description="navigation"
            ),
            CropRegion(
                top=self.body_start,
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
        Validate USA Today-specific crop requirements.
        
        Args:
            cropped: The cropped PIL Image
            metadata: Metadata about the crop operation
            
        Returns:
            bool indicating if crop meets USA Today requirements
        """
        # First check base requirements
        if not self._validate_base_requirements(cropped, metadata):
            return False
            
        # Verify we got both required regions
        required_regions = {"navigation", "main_content"}
        if not all(region in metadata.regions_cropped for region in required_regions):
            logger.warning(f"USA Today: Missing required regions. Found: {metadata.regions_cropped}")
            return False
            
        return True 