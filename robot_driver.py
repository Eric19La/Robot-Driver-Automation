"""
Robot Driver - Core automation module
Performs a fixed task: Search for a product on Amazon and report its price
"""
import asyncio
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError


async def search_product_price(product_name: str = "wireless mouse") -> dict:
    """
    Search for a product on Amazon and return its price.

    Args:
        product_name: Name of the product to search for

    Returns:
        Dictionary with status and result/error message
    """
    result = {
        "success": False,
        "message": "",
        "product": product_name,
        "price": None
    }

    browser = None

    try:
        async with async_playwright() as p:
            # Launch browser (set headless=False to see what's happening)
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            # Set timeout for operations
            page.set_default_timeout(30000)  # 30 seconds

            # Navigate to Amazon
            print(f"Navigating to Amazon...")
            await page.goto("https://www.amazon.com", wait_until="domcontentloaded")
            await asyncio.sleep(2)  # Give page time to fully load

            # Wait for search box to be available (try multiple selectors)
            print(f"Searching for '{product_name}'...")
            search_box_selectors = [
                'input[id="twotabsearchtextbox"]',
                'input[name="field-keywords"]',
                'input[type="text"]'
            ]

            search_box = None
            for selector in search_box_selectors:
                try:
                    search_box = await page.wait_for_selector(selector, timeout=5000)
                    if search_box:
                        break
                except:
                    continue

            if not search_box:
                result["message"] = "Could not find search box on Amazon"
                print(f"\n Error: {result['message']}")
                return result

            # Type product name and search
            await search_box.fill(product_name)
            await search_box.press("Enter")

            # Wait for results to load
            await page.wait_for_selector(
                '[data-component-type="s-search-result"]',
                timeout=15000
            )

            # Get first product result
            first_result = await page.query_selector(
                '[data-component-type="s-search-result"]'
            )

            if not first_result:
                result["message"] = "No search results found"
                return result

            # Extract product title (try multiple selectors)
            title_selectors = [
                'h2 a span',
                'h2 span',
                'h2',
                '.a-size-medium',
                '.a-size-base-plus'
            ]

            product_title = "Unknown"
            for selector in title_selectors:
                title_element = await first_result.query_selector(selector)
                if title_element:
                    text = await title_element.inner_text()
                    if text and text.strip():
                        product_title = text.strip()
                        break

            # Extract price (try multiple selectors as Amazon's layout varies)
            price_selectors = [
                '.a-price .a-offscreen',
                '.a-price-whole',
                'span.a-price span[aria-hidden="true"]'
            ]

            price_text = None
            for selector in price_selectors:
                price_element = await first_result.query_selector(selector)
                if price_element:
                    price_text = await price_element.inner_text()
                    if price_text:
                        break

            if price_text:
                result["success"] = True
                result["message"] = f"Success! Product '{product_title[:50]}...' found"
                result["price"] = price_text.strip()
                print(f"\n Success! Product: {product_title[:50]}...")
                print(f" Price: {price_text}")
            else:
                result["message"] = "Product found but price not available"
                print(f"\n Warning: Product found but price not displayed")

            await browser.close()

    except PlaywrightTimeoutError as e:
        result["message"] = f"Timeout error: Page took too long to load or element not found"
        print(f"\n Error: {result['message']}")
        if page:
            try:
                await page.screenshot(path="error_screenshot.png")
                print(f"   Screenshot saved to: error_screenshot.png")
            except:
                pass

    except Exception as e:
        result["message"] = f"Error occurred: {str(e)}"
        print(f"\n Error: {result['message']}")

    finally:
        if browser:
            try:
                await browser.close()
            except:
                pass

    return result


async def main():
    """Main entry point for the robot driver"""
    print("=" * 60)
    print("Robot Driver - Automated Product Search")
    print("=" * 60)

    # Perform the fixed task
    result = await search_product_price("wireless mouse")

    print("\n" + "=" * 60)
    if result["success"]:
        print(f"RESULT: {result['message']}")
        print(f"PRICE: {result['price']}")
    else:
        print(f"FAILED: {result['message']}")
    print("=" * 60)

    return result


if __name__ == "__main__":
    asyncio.run(main())
