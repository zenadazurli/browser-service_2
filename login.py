import asyncio
import re
import json
import os
from playwright.async_api import async_playwright

# Credenziali
EMAIL = "sandrominori50+ulugarecexisa@gmail.com"
PASSWORD = "DDnmVV45!!"

async def login_and_get_cookies():
    print("🚀 Avvio Playwright con intercettazione...")
    
    cookies_found = {}
    
    async with async_playwright() as p:
        # Avvia browser
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        
        # === INTERCETTA LE RISPOSTE ===
        async def capture_response(response):
            url = response.url
            print(f"📡 Response: {response.status} - {url[:80]}")
            
            # Intercetta la risposta di login (302 redirect)
            if "/logon/" in url and response.status == 302:
                print("\n🎯 RISPOSTA DI LOGIN INTERCETTATA!")
                
                set_cookie = response.headers.get('set-cookie', '')
                print(f"🍪 Set-Cookie: {set_cookie[:200]}")
                
                # Estrai sesids e user_id
                sesids_match = re.search(r'sesids=([^;]+)', set_cookie)
                user_id_match = re.search(r'user_id=([^;]+)', set_cookie)
                
                if sesids_match:
                    cookies_found['sesids'] = sesids_match.group(1)
                    print(f"✅ sesids = {cookies_found['sesids']}")
                
                if user_id_match:
                    cookies_found['user_id'] = user_id_match.group(1)
                    print(f"✅ user_id = {cookies_found['user_id']}")
            
            # Intercetta anche la dashboard
            elif "/account/" in url or "/surf/" in url:
                print(f"✅ Dashboard raggiunta: {url}")
        
        # Attiva l'intercettatore
        page.on('response', capture_response)
        
        # 1. Vai alla pagina di login
        print("\n🌐 Apertura pagina login...")
        await page.goto("https://www.easyhits4u.com/logon/", wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)
        
        # 2. Attendi che React carichi il form
        print("⏳ Attesa caricamento form...")
        await page.wait_for_selector('input[name="username"]', timeout=30000)
        
        # 3. Compila form
        print("📝 Compilazione form...")
        await page.fill('input[name="username"]', EMAIL)
        await page.fill('input[name="password"]', PASSWORD)
        
        # 4. Clicca login
        print("🔑 Invio login...")
        await page.click('button.btn_green')
        
        # 5. Attesa che il redirect completi
        print("⏳ Attesa redirect...")
        await page.wait_for_timeout(15000)
        
        # 6. Verifica URL finale
        current_url = page.url
        print(f"\n📍 URL finale: {current_url}")
        
        # 7. Se non abbiamo catturato i cookie, prova a prenderli dal contesto
        if not cookies_found:
            print("\n🍪 Tentativo lettura cookie dal contesto...")
            all_cookies = await context.cookies()
            for cookie in all_cookies:
                if cookie['name'] in ['sesids', 'user_id']:
                    cookies_found[cookie['name']] = cookie['value']
                    print(f"✅ {cookie['name']} = {cookie['value']}")
        
        # 8. Salva cookie su file
        with open("/tmp/cookies.json", "w") as f:
            json.dump(cookies_found, f)
        print("\n💾 Cookie salvati in /tmp/cookies.json")
        
        await browser.close()
        return cookies_found

async def main():
    print("=" * 60)
    print("Playwright - Intercettazione Cookie EasyHits4U")
    print("=" * 60)
    
    try:
        cookies = await login_and_get_cookies()
        
        print("\n" + "=" * 60)
        if cookies.get('sesids') and cookies.get('user_id'):
            print("🎉🎉🎉 SUCCESSO! 🎉🎉🎉")
            print(f"   sesids = {cookies['sesids']}")
            print(f"   user_id = {cookies['user_id']}")
        else:
            print("❌ Cookie non trovati")
            print(f"   Trovati: {cookies}")
    except Exception as e:
        print(f"❌ Errore: {e}")
    
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())