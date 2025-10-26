"""
Quick test script for basic robot driver functionality
Run this to verify the installation is working correctly
"""
import asyncio
from robot_driver import search_product_price


async def test_basic_functionality():
    """Test basic robot driver"""
    print("\n" + "="*60)
    print("Testing Basic Robot Driver")
    print("="*60)

    try:
        print("\n1. Testing product search...")
        result = await search_product_price("wireless mouse")

        if result["success"]:
            print(f"\n✓ TEST PASSED")
            print(f"   Product: {result['product']}")
            print(f"   Price: {result['price']}")
            print(f"   Message: {result['message']}")
            return True
        else:
            print(f"\n✗ TEST FAILED")
            print(f"   Error: {result['message']}")
            return False

    except Exception as e:
        print(f"\n✗ TEST FAILED WITH EXCEPTION")
        print(f"   Error: {str(e)}")
        return False


async def main():
    """Main test runner"""
    success = await test_basic_functionality()

    print("\n" + "="*60)
    if success:
        print("All tests passed! ✓")
        print("\nYour installation is working correctly.")
        print("\nNext steps:")
        print("  - Edit robot_driver.py to customize the task")
        print("  - Try ai_robot_driver.py for AI-powered automation")
        print("  - Run api.py to start the web service")
    else:
        print("Tests failed ✗")
        print("\nTroubleshooting:")
        print("  - Check your internet connection")
        print("  - Ensure Playwright browsers are installed:")
        print("    playwright install chromium")
        print("  - Check if Amazon is accessible from your location")
    print("="*60 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
