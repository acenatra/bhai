import asyncio
from playwright.async_api import async_playwright

class WebBhai:
    def __init__(self):
        self.playwright_manager = None
        self.browser = None
        self.context = None
        self.page = None

    async def start(self, headed=True):
        if not self.playwright_manager:
            self.playwright_manager = await async_playwright().start()
            # We use headed=True by default for YouTube so the user can see/hear the video
            self.browser = await self.playwright_manager.chromium.launch(headless=not headed)
            self.context = await self.browser.new_context()
            self.page = await self.context.new_page()
            print("🌐 Bhai's Web Browser is active!")

    async def navigate(self, url):
        await self.start()
        print(f"🌐 Navigating to: {url}")
        await self.page.goto(url)

    async def search(self, query):
        await self.start()
        print(f"🌐 Searching for: {query}")
        try:
            # Try common search selectors
            search_input = await self.page.wait_for_selector('input[name="q"], input[name="search"], input[type="search"]', timeout=5000)
            await search_input.fill(query)
            await search_input.press("Enter")
        except Exception as e:
            print(f"⚠️ Search failed: {e}. Trying simple navigation.")
            await self.page.goto(f"https://www.google.com/search?q={query}")

    async def play_youtube(self, song_name):
        await self.start()
        print(f"🎵 Bhai is playing '{song_name}' on YouTube...")
        try:
            # 1. Go to YouTube search directly
            await self.page.goto(f"https://www.youtube.com/results?search_query={song_name}")
            
            # 2. Click the first video result
            # YouTube video titles are usually under ytd-video-renderer #video-title
            video_selector = 'ytd-video-renderer #video-title'
            await self.page.wait_for_selector(video_selector, timeout=10000)
            await self.page.click(video_selector)
            
            print("✅ Video clicked! Enjoy the music.")
        except Exception as e:
            print(f"⚠️ Failed to play YouTube: {e}")

    async def stop(self):
        if self.browser:
            await self.browser.close()
        if self.playwright_manager:
            await self.playwright_manager.stop()

# Wrapper for synchronous calls from main loop
def run_web_action(action, params):
    wb = WebBhai()
    async def _run():
        if action == "web_browse":
            url = params.get("url")
            query = params.get("query")
            if url:
                await wb.navigate(url)
            if query:
                await wb.search(query)
            # Keep browser open for results
            await asyncio.sleep(8)
            
        elif action == "play_youtube":
            song = params.get("query") or params.get("song_name")
            if song:
                await wb.play_youtube(song)
                # Keep browser open for a long time since it's a song
                await asyncio.sleep(300) # Play for 5 mins or until user stops
        
        await wb.stop()
    
    try:
        asyncio.run(_run())
    except Exception as e:
        print(f"⚠️ Web Action Error: {e}")

if __name__ == "__main__":
    # Test YouTube playback
    run_web_action("play_youtube", {"query": "dil dil pakistan"})
