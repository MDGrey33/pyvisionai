"""HTML processing configuration."""

# Default configuration for HTML processing
DEFAULT_CONFIG = {
    # Viewport settings
    "viewport": {
        "width": 1920,  # Standard desktop width
        "height": 1080,  # Full HD height
        "device_scale_factor": 1.0,
    },
    # Timing settings
    "timeout": {
        "page_load": 30000,  # 30s for initial page load
        "wait_for_idle": 5000,  # 5s wait for network idle
        "render_delay": 1000,  # 1s extra for final renders
    },
    # Browser settings
    "browser": {
        "headless": True,
        "javascript_enabled": True,
        "user_agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
    },
    # Screenshot settings
    "screenshot": {
        "full_page": True,  # Capture entire page
        "quality": 90,  # JPEG quality
        "format": "jpeg",  # JPEG for better compression
        "optimize": True,  # Apply image optimization
    },
    # Content settings
    "content": {
        "wait_for_fonts": True,  # Wait for web fonts
        "wait_for_images": True,  # Wait for images to load
        "remove_ads": True,  # Try to remove ad elements
        "max_height": 15000,  # Prevent infinite scrolls (px)
    },
}

# Common ad-related selectors to remove if remove_ads is True
AD_SELECTORS = [
    'div[class*="ad-"]',
    'div[class*="ads-"]',
    'div[id*="google_ads"]',
    'div[class*="banner"]',
    ".advertisement",
    "#advertisement",
]

# Elements to wait for before taking screenshot
WAIT_SELECTORS = [
    "img",  # Images
    "video",  # Video elements
    "canvas",  # Canvas elements
    "svg",  # SVG graphics
    "@font-face",  # Custom fonts
]
