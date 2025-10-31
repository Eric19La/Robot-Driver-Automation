"""
AI Robot Driver - Advanced automation with MCP and LLM
Uses Playwright and Google Gemini AI to dynamically execute tasks based on plain English goals
"""
import asyncio
import json
import os
from typing import Optional, List, Dict, Any
import google.generativeai as genai
from playwright.async_api import async_playwright, Page, TimeoutError as PlaywrightTimeoutError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class AIRobotDriver:
    """AI-powered web automation driver using Playwright and Gemini AI"""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the AI Robot Driver

        Args:
            api_key: Google Gemini API key (if not provided, loads from GEMINI_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found. Set it in .env file or pass as parameter.")

        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        self.page: Optional[Page] = None
        self.browser = None
        self.playwright = None

    async def get_page_context(self) -> Dict[str, Any]:
        """
        Get current page context information for the AI

        Returns:
            Dictionary with page URL, title, and accessible elements
        """
        if not self.page:
            return {}

        try:
            context = {
                "url": self.page.url,
                "title": await self.page.title(),
                "elements": []
            }

            # Get interactive elements with their roles and labels
            elements = await self.page.query_selector_all(
                'button, a, input, select, textarea, [role="button"], [role="link"]'
            )

            for i, elem in enumerate(elements[:20]):  # Limit to first 20 elements
                try:
                    tag = await elem.evaluate('el => el.tagName')
                    input_type = await elem.get_attribute('type')

                    # Skip submit buttons when reporting to AI
                    if tag == 'INPUT' and input_type == 'submit':
                        continue

                    text = await elem.inner_text() if tag != 'INPUT' else ''
                    role = await elem.get_attribute('role') or tag.lower()
                    aria_label = await elem.get_attribute('aria-label')
                    placeholder = await elem.get_attribute('placeholder')
                    elem_id = await elem.get_attribute('id')
                    name = await elem.get_attribute('name')

                    element_info = {
                        "index": len(context["elements"]),  # Use actual index in filtered list
                        "tag": tag.lower(),
                        "type": input_type,
                        "role": role,
                        "text": text.strip()[:50] if text else "",
                        "aria_label": aria_label,
                        "placeholder": placeholder,
                        "id": elem_id,
                        "name": name
                    }

                    context["elements"].append(element_info)
                except:
                    continue

            return context

        except Exception as e:
            print(f"Warning: Could not extract full page context: {e}")
            return {"url": self.page.url, "elements": []}

    def create_action_prompt(self, goal: str, context: Dict[str, Any]) -> str:
        """
        Create a prompt for the AI to determine next action

        Args:
            goal: The user's goal in plain English
            context: Current page context

        Returns:
            Formatted prompt string
        """
        elements_str = "\n".join([
            f"  - [{e['index']}] {e['tag']}" +
            (f" type={e['type']}" if e.get('type') else "") +
            f" (role: {e['role']}): "
            f"text='{e['text']}', id='{e['id']}', name='{e['name']}', "
            f"aria-label='{e['aria_label']}', placeholder='{e['placeholder']}'"
            for e in context.get("elements", [])
        ])

        prompt = f"""You are controlling a web browser to accomplish this goal: "{goal}"

Current page state:
- URL: {context.get('url', 'unknown')}
- Title: {context.get('title', 'unknown')}

Available interactive elements:
{elements_str if elements_str else '(No elements found)'}

Based on this information, what is the NEXT SINGLE ACTION to take toward the goal?

Respond ONLY with a JSON object in this exact format:
{{
    "action": "navigate" | "click" | "type" | "wait" | "done",
    "target": "selector or URL or element index",
    "value": "text to type (only for 'type' action)",
    "reasoning": "brief explanation"
}}

Actions:
- navigate: Go to a URL (target = full URL)
- click: Click an element (target = selector or element index from list)
- type: Type text into input (target = selector or element index, value = text)
- wait: Wait for element (target = selector)
- done: Goal completed successfully

Examples:
{{"action": "navigate", "target": "https://amazon.com", "reasoning": "Need to go to Amazon first"}}
{{"action": "click", "target": "0", "reasoning": "Click the search button"}}
{{"action": "type", "target": "input[name='q']", "value": "wireless mouse", "reasoning": "Enter search query"}}
{{"action": "done", "target": "", "reasoning": "Product price found and displayed"}}
"""
        return prompt

    async def execute_action(self, action: Dict[str, Any]) -> bool:
        """
        Execute a single action on the page

        Args:
            action: Action dictionary from AI

        Returns:
            True if action succeeded, False otherwise
        """
        try:
            action_type = action.get("action")
            target = action.get("target", "")
            value = action.get("value", "")

            print(f"  → {action_type.upper()}: {action.get('reasoning', '')}")

            if action_type == "navigate":
                await self.page.goto(target, wait_until="domcontentloaded")
                await asyncio.sleep(2)  # Give page time to load
                return True

            elif action_type == "click":
                # Handle element index or selector
                if target.isdigit():
                    elements = await self.page.query_selector_all(
                        'button, a, input[type="submit"], [role="button"]'
                    )
                    idx = int(target)
                    if idx < len(elements):
                        await elements[idx].click()
                    else:
                        print(f"    ✗ Element index {idx} out of range")
                        return False
                else:
                    await self.page.click(target)
                await asyncio.sleep(1)
                return True

            elif action_type == "type":
                # Always try to find text inputs by common patterns first
                try:
                    # Try common search box selectors
                    search_box = await self.page.query_selector(
                        'input[name="field-keywords"], input[id*="search"], '
                        'input[type="search"], input[type="text"]'
                    )
                    if search_box:
                        await search_box.fill(value)
                        # Also press Enter to submit
                        await search_box.press("Enter")
                        await asyncio.sleep(2)
                        return True
                except Exception as e:
                    print(f"    ✗ Error typing: {e}")
                    return False

                return False

            elif action_type == "wait":
                await self.page.wait_for_selector(target, timeout=10000)
                return True

            elif action_type == "done":
                return True

            else:
                print(f"    ✗ Unknown action type: {action_type}")
                return False

        except PlaywrightTimeoutError:
            print(f"    ✗ Timeout waiting for element: {target}")
            return False
        except Exception as e:
            print(f"    ✗ Error executing action: {e}")
            return False

    async def execute_goal(self, goal: str, max_steps: int = 15) -> Dict[str, Any]:
        """
        Execute a goal using AI to determine steps dynamically

        Args:
            goal: Plain English description of what to accomplish
            max_steps: Maximum number of steps to attempt

        Returns:
            Dictionary with success status and final result
        """
        result = {
            "success": False,
            "goal": goal,
            "steps_taken": 0,
            "message": ""
        }

        try:
            # Initialize browser
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(headless=True)
            self.page = await self.browser.new_page()
            self.page.set_default_timeout(30000)

            print(f"\n{'='*60}")
            print(f"AI Robot Driver - Executing Goal")
            print(f"{'='*60}")
            print(f"Goal: {goal}\n")

            for step in range(max_steps):
                result["steps_taken"] = step + 1

                # Get current page context
                context = await self.get_page_context()

                # Ask AI for next action
                prompt = self.create_action_prompt(goal, context)

                print(f"Step {step + 1}: Analyzing page and planning action...")

                # Call Gemini AI
                response = self.model.generate_content(prompt)

                # Parse AI response
                response_text = response.text.strip()

                # Extract JSON from response
                if "```json" in response_text:
                    response_text = response_text.split("```json")[1].split("```")[0].strip()
                elif "```" in response_text:
                    response_text = response_text.split("```")[1].split("```")[0].strip()

                try:
                    action = json.loads(response_text)
                except json.JSONDecodeError:
                    print(f"  ✗ Could not parse AI response as JSON")
                    continue

                # Check if done
                if action.get("action") == "done":
                    result["success"] = True
                    result["message"] = f"Goal completed: {action.get('reasoning', '')}"
                    print(f"\n✓ {result['message']}")
                    break

                # Execute action
                success = await self.execute_action(action)

                if not success:
                    print(f"  ⚠ Action failed, will try alternative approach")

                # Small delay between actions
                await asyncio.sleep(1)

            if not result["success"]:
                result["message"] = f"Reached maximum steps ({max_steps}) without completing goal"
                print(f"\n⚠ {result['message']}")

        except Exception as e:
            result["message"] = f"Error: {str(e)}"
            print(f"\n✗ {result['message']}")

        finally:
            # Cleanup
            if self.browser:
                await self.browser.close()
            if self.playwright:
                await self.playwright.stop()

        print(f"{'='*60}\n")
        return result


async def main():
    """Main entry point for AI robot driver"""
    try:
        driver = AIRobotDriver()

        # Example goal
        goal = "Go to Amazon and find the price of a wireless mouse"

        result = await driver.execute_goal(goal)

        if result["success"]:
            print(f"SUCCESS: {result['message']}")
            print(f"Steps taken: {result['steps_taken']}")
        else:
            print(f"FAILED: {result['message']}")
            print(f"Steps attempted: {result['steps_taken']}")

    except ValueError as e:
        print(f"Configuration Error: {e}")
        print("Please set GEMINI_API_KEY in your .env file")
        print("Get your free API key from: https://aistudio.google.com/apikey")


if __name__ == "__main__":
    asyncio.run(main())
