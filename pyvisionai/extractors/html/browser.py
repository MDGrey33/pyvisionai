"""Browser management for HTML processing."""

import asyncio
from typing import Optional
from playwright.async_api import async_playwright, Browser, Page

from pyvisionai.config.html_config import DEFAULT_CONFIG, AD_SELECTORS, WAIT_SELECTORS


async def setup_browser(config: Optional[dict] = None) -> Browser:
    """Set up and return a browser instance."""
    config = config or DEFAULT_CONFIG
    browser_config = config["browser"]

    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=browser_config["headless"])
    return browser


async def setup_page(browser: Browser, config: Optional[dict] = None) -> Page:
    """Set up and return a page with configured viewport and settings."""
    config = config or DEFAULT_CONFIG
    viewport = config["viewport"]

    page = await browser.new_page()
    await page.set_viewport_size(
        {"width": viewport["width"], "height": viewport["height"]}
    )
    await page.set_extra_http_headers({"User-Agent": config["browser"]["user_agent"]})
    return page


async def process_page(url: str, config: Optional[dict] = None) -> bytes:
    """Process a webpage and return its screenshot."""
    config = config or DEFAULT_CONFIG
    timeout = config["timeout"]
    content = config["content"]

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=config["browser"]["headless"])
        page = await setup_page(browser, config)

        try:
            # Navigate to the page
            await page.goto(url, wait_until="networkidle", timeout=timeout["page_load"])

            # Wait for key elements
            if content["wait_for_images"]:
                for selector in WAIT_SELECTORS:
                    try:
                        await page.wait_for_selector(
                            selector, state="visible", timeout=timeout["wait_for_idle"]
                        )
                    except:
                        continue

            # Remove ads if configured
            if content["remove_ads"]:
                for selector in AD_SELECTORS:
                    try:
                        await page.evaluate(
                            f"""
                            document.querySelectorAll('{selector}')
                            .forEach(el => el.remove())
                        """
                        )
                    except:
                        continue

            # Add small delay for final renders
            await page.wait_for_timeout(timeout["render_delay"])

            # Take screenshot
            screenshot = await page.screenshot(
                full_page=config["screenshot"]["full_page"],
                type=config["screenshot"]["format"],
                quality=config["screenshot"]["quality"],
            )

            return screenshot

        finally:
            await browser.close()


def capture_webpage(url: str, config: Optional[dict] = None) -> bytes:
    """Synchronous wrapper for processing webpage."""
    return asyncio.run(process_page(url, config))
