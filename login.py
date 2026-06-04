import asyncio
import re
import json
from playwright.async_api import async_playwright

EMAIL = "sandrominori50+ulugarecexisa@gmail.com"
PASSWORD = "DDnmVV45!!"

async def login_and_get_cookies():
    print("🚀 Avvio Playwright...")
    
    cookies_found = {}
    
    try:
        async with async_playwright() as p:
            print("📱 Lancio browser...")
            browser = await p.chromium.launch(
                headless=True,
                args=['--no-sandbox', '--disable-setuid-sandbox']
            )
            print("✅ Browser avviato")
            
            context = await browser.new_context()
            page = await context.new_page()
            
            # Intercetta risposte
            async def capture_response(response):
                if "/logon/" in response.url and response.status == 302:
                    print("🎯 Login response catturata!")
                    set_cookie = response.headers.get('set-cookie', '')
                    sesids = re.search(r'sesids=([^;]+)', set_cookie)
                    user_id = re.search(r'user_id=([^;]+)', set_cookie)
                    if sesids:
                        cookies_found['sesids'] = sesids.group(1)
                        print(f"✅ sesids = {sesids.group(1)}")
                    if user_id:
                        cookies_found['user_id'] = user_id.group(1)
                        print(f"✅ user_id = {user_id.group(1)}")
            
            page.on('response', capture_response)
            
            print("🌐 Apertura pagina...")
            await page.goto("https://www.easyhits4u.com/logon/")
            await page.wait_for_timeout(5000)
            
            print("📝 Compilazione form...")
            await page.fill('input[name="username"]', EMAIL)
            await page.fill('input[name="password"]', PASSWORD)
            
            print("🔑 Click login...")
            await page.click('button.btn_green')
            
            print("⏳ Attesa...")
            await page.wait_for_timeout(15000)
            
            await browser.close()
            
    except Exception as e:
        print(f"❌ Errore: {e}")
    
    return cookies_found

if __name__ == "__main__":
    print("=" * 60)
    result = asyncio.run(login_and_get_cookies())
    print("=" * 60)
    print(f"🎉 Risultato: {result}")
    print("=" * 60)
