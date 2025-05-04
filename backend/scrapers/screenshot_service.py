from datetime import datetime
import logging
import asyncio
import psutil
import os
from typing import Optional, Dict
from io import BytesIO
from playwright.async_api import async_playwright, Browser, Page

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ScreenshotService:
    """Service for capturing screenshots using Playwright"""
    
    def __init__(self):
        self.browser: Optional[Browser] = None
        self.viewport = {
            "width": 1920,
            "height": 2000,
            "device_scale_factor": 2.0
        }
        self.browser_args = [
            '--disable-gpu',
            '--disable-dev-shm-usage',
            '--disable-setuid-sandbox',
            '--no-sandbox'
        ]
        
    def _get_memory_usage(self) -> Dict[str, float]:
        """Get current memory usage"""
        process = psutil.Process(os.getpid())
        memory_info = process.memory_info()
        return {
            "rss_mb": memory_info.rss / 1024 / 1024,
            "vms_mb": memory_info.vms / 1024 / 1024
        }
        
    async def _init_browser(self) -> None:
        """Initialize browser if not already initialized"""
        if not self.browser:
            playwright = await async_playwright().start()
            self.browser = await playwright.chromium.launch(
                headless=True,
                args=self.browser_args
            )
            mem_usage = self._get_memory_usage()
            logger.info("Browser initialized", extra={
                "memory_usage": mem_usage,
                "timestamp": datetime.utcnow().isoformat()
            })
            
    async def capture(self, url: str) -> Optional[BytesIO]:
        """
        Capture a full-page screenshot of the given URL
        
        Args:
            url (str): URL to capture
            
        Returns:
            Optional[BytesIO]: Screenshot as bytes if successful, None otherwise
        """
        start_time = datetime.utcnow()
        log_ctx = {
            "url": url,
            "start_time": start_time.isoformat(),
            "operation": "capture"
        }
        
        context = None
        try:
            await self._init_browser()
            context = await self.browser.new_context(viewport=self.viewport)
            page = await context.new_page()
            
            # Configure timeouts
            page.set_default_navigation_timeout(120000)  # 2 minutes
            page.set_default_timeout(120000)
            
            # Navigate and wait for basic content
            await page.goto(url, wait_until='domcontentloaded')
            await page.wait_for_selector('body')
            
            # Capture screenshot
            screenshot_bytes = await page.screenshot(full_page=True, type='png')
            
            # Log success with metrics
            end_time = datetime.utcnow()
            duration = (end_time - start_time).total_seconds()
            mem_usage = self._get_memory_usage()
            
            log_ctx.update({
                "status": "success",
                "duration_seconds": duration,
                "memory_usage": mem_usage,
                "screenshot_size_bytes": len(screenshot_bytes)
            })
            logger.info("Screenshot captured successfully", extra=log_ctx)
            
            return BytesIO(screenshot_bytes)
            
        except Exception as e:
            log_ctx.update({
                "status": "error",
                "error_type": type(e).__name__,
                "error_message": str(e)
            })
            logger.error("Screenshot capture failed", extra=log_ctx)
            return None
            
        finally:
            # Clean up context
            if context is not None:
                try:
                    await context.close()
                except Exception:
                    pass
                
    async def cleanup(self):
        """Clean up browser resources"""
        if self.browser:
            try:
                await self.browser.close()
                self.browser = None
                logger.info("Browser resources cleaned up")
            except Exception as e:
                logger.error(f"Error cleaning up browser: {e}") 