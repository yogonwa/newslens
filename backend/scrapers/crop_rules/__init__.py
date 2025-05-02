from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
from PIL import Image
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class CropDimensions:
    """
    Standard dimensions for cropping
    
    Attributes:
        top: Pixels from top to start crop
        height: Height of crop region in pixels
        target_width: Standard width (3000px) for all sources
    """
    top: int
    height: int
    target_width: int = 3000  # Standard width across all sources

    def __post_init__(self):
        """Validate dimensions"""
        if self.top < 0:
            raise ValueError("Crop top cannot be negative")
        if self.height <= 0:
            raise ValueError("Crop height must be positive")
        if self.target_width <= 0:
            raise ValueError("Target width must be positive")

@dataclass
class CropMetadata:
    """
    Metadata about the crop operation
    
    Attributes:
        original_dimensions: (width, height) of original image
        source_key: Identifier for the news source
        regions_cropped: List of region descriptions that were cropped
        total_height: Height of final stitched image
    """
    original_dimensions: Tuple[int, int]  # width, height
    source_key: str
    regions_cropped: List[str]  # Description of regions cropped
    total_height: int  # Height of final image

@dataclass
class CropRegion:
    """
    Defines a region to be cropped
    
    Attributes:
        top: Pixels from top to start region
        height: Height of region in pixels
        description: Identifier for this region (e.g., "header", "main_content")
    """
    top: int
    height: int
    description: str

class CropperBase(ABC):
    """
    Shared base functionality for all croppers
    
    This class enforces standard width and provides common utilities.
    All news sources use a 3000px target width for consistency.
    """
    
    def __init__(self, source_key: str):
        self.source_key = source_key
        self.target_width = 3000  # Standard width across all sources
        self.minimum_height = 1000  # Minimum acceptable crop height
        
    def _create_metadata(self, image: Image.Image, regions: List[str], result_height: int) -> CropMetadata:
        """Create metadata for crop operation"""
        return CropMetadata(
            original_dimensions=image.size,
            source_key=self.source_key,
            regions_cropped=regions,
            total_height=result_height
        )
        
    def _center_horizontally(self, full_width: int) -> Tuple[int, int]:
        """
        Calculate horizontal cropping bounds to center content
        
        Args:
            full_width: Width of original image
            
        Returns:
            Tuple of (left, right) crop coordinates
        """
        left = max((full_width - self.target_width) // 2, 0)
        return left, left + self.target_width
        
    def _validate_base_requirements(self, cropped: Image.Image, metadata: CropMetadata) -> bool:
        """
        Validate basic requirements all crops must meet
        
        Args:
            cropped: The cropped PIL Image
            metadata: Metadata about the crop operation
            
        Returns:
            bool indicating if basic requirements are met
        """
        # Check minimum height
        if cropped.height < self.minimum_height:
            logger.warning(f"{self.source_key}: Crop height {cropped.height}px below minimum {self.minimum_height}px")
            return False
            
        # Verify width is correct
        if cropped.width != self.target_width:
            logger.warning(f"{self.source_key}: Crop width {cropped.width}px != target {self.target_width}px")
            return False
            
        return True

class BaseCropper(CropperBase):
    """Base class for single-region croppers (NYT, WaPo)"""
    
    @abstractmethod
    def get_crop_dimensions(self, image: Image.Image) -> CropDimensions:
        """Get dimensions for single crop region"""
        pass
        
    def crop(self, image: Image.Image) -> Tuple[Image.Image, CropMetadata]:
        """Standard single-region crop"""
        try:
            dims = self.get_crop_dimensions(image)
            full_width, full_height = image.size
            
            # Calculate horizontal centering
            left, right = self._center_horizontally(full_width)
            
            # Perform crop
            cropped = image.crop((
                left,
                dims.top,
                right,
                min(dims.top + dims.height, full_height)
            ))
            
            # Create metadata
            metadata = self._create_metadata(
                image=image,
                regions=["main_content"],
                result_height=cropped.height
            )
            
            return cropped, metadata
            
        except Exception as e:
            logger.error(
                "Crop failed",
                extra={
                    "source": self.source_key,
                    "error": str(e),
                    "error_type": type(e).__name__
                }
            )
            raise
            
    @abstractmethod
    def validate_crop(self, cropped: Image.Image, metadata: CropMetadata) -> bool:
        """
        Validate crop requirements
        
        All implementations should call _validate_base_requirements first:
        if not self._validate_base_requirements(cropped, metadata):
            return False
        """
        pass

class MultiRegionCropper(CropperBase):
    """Base class for multi-region croppers (Fox, USA Today)"""
    
    @abstractmethod
    def get_regions(self) -> List[CropRegion]:
        """Get all regions to be cropped"""
        pass
        
    def crop(self, image: Image.Image) -> Tuple[Image.Image, CropMetadata]:
        """Multi-region crop and stitch"""
        try:
            full_width, full_height = image.size
            left, right = self._center_horizontally(full_width)
            
            # Crop each region
            cropped_regions = []
            region_descriptions = []
            total_height = 0
            
            for region in self.get_regions():
                # Skip if region exceeds image bounds
                if region.top + region.height > full_height:
                    continue
                    
                # Crop region
                cropped = image.crop((
                    left,
                    region.top,
                    right,
                    region.top + region.height
                ))
                cropped_regions.append(cropped)
                region_descriptions.append(region.description)
                total_height += region.height
            
            # Stitch regions
            stitched = self.stitch_regions(cropped_regions)
            
            # Create metadata
            metadata = self._create_metadata(
                image=image,
                regions=region_descriptions,
                result_height=stitched.height
            )
            
            return stitched, metadata
            
        except Exception as e:
            logger.error(
                "Multi-region crop failed",
                extra={
                    "source": self.source_key,
                    "error": str(e),
                    "error_type": type(e).__name__
                }
            )
            raise
            
    @abstractmethod
    def stitch_regions(self, regions: List[Image.Image]) -> Image.Image:
        """Define how regions should be combined"""
        pass
        
    @abstractmethod
    def validate_crop(self, cropped: Image.Image, metadata: CropMetadata) -> bool:
        """
        Validate crop requirements
        
        All implementations should call _validate_base_requirements first:
        if not self._validate_base_requirements(cropped, metadata):
            return False
        """
        pass 