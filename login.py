import asyncio
import json
from browser_use import Browser

API_KEY = "bu_v46aP0o7dHtRzpC-4PSIp5bfr_Fsyz3_oX30bz81Jis"

async def login_and_get_cookies():
    print("🚀 Browser Use con accesso diretto al context...")
    
    # Crea browser con modalità cloud
    browser = Browser(
        use_cloud=True,
        headless=True,
        api_key=API_KEY
    )
    
    try:
        # Ottieni la pagina
        page = await browser.get_page()
        
        # 1. Vai al login
        print("🌐 Apertura login...")
        await page.goto("https://www.easyhits4u.com/logon/")
        await page.wait_for_timeout(3000)
        
        # 2. Compila form
        print("📝 Compilazione...")
        await page.fill('input[name="username"]', "sandrominori50+ulugarecexisa@gmail.com")
        await page.fill('input[name="password"]', "DDnmVV45!!")
        
        # 3. Invia
        print("🔑 Login...")
        await page.click('button.btn_green')
        
        # 4. Attesa redirect
        print("⏳ Attesa redirect...")
        await page.wait_for_timeout(15000)
        
        # 5. === ACCEDI AL CONTEXT E PRENDI I COOKIE ===
        print("\n🍪 Estrazione cookie dal context...")
        context = page.context
        all_cookies = await context.cookies()
        
        for cookie in all_cookies:
            if cookie['name'] in ['sesids', 'user_id']:
                print(f"✅ {cookie['name']} = {cookie['value']}")
        
        # Salva
        with open("/tmp/cookies.json", "w") as f:
            json.dump(all_cookies, f, indent=2)
        
        sesids = next((c['value'] for c in all_cookies if c['name'] == 'sesids'), None)
        user_id = next((c['value'] for c in all_cookies if c['name'] == 'user_id'), None)
        
        return sesids, user_id
        
    finally:
        await browser.close()

if __name__ == "__main__":
    import asyncio
    sesids, user_id = asyncio.run(login_and_get_cookies())
    print(f"\n🎉 Risultato: sesids={sesids}, user_id={user_id}")
