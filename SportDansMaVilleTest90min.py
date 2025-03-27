from playwright.async_api import async_playwright
import asyncio
import nest_asyncio

nest_asyncio.apply()

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Voir l'exécution
        page = await browser.new_page()
        
        # Accès à la page de réservation
        await page.goto("https://sport-dans-la-ville.doinsport.club/select-booking?guid=%221ce2c55d-6010-4f45-9b6f-1aafc04382fa%22&from=sport&activitySelectedId=%22cc4da804-1ef4-4f57-9fa4-4c203cdc06c8%22&categoryId=%22910503af-d67a-4f2b-a0df-838e0b4fb8ac%22")
        # Ouvrir le calendrier
        await page.locator("app-svg-container").get_by_role("img").click()
        
        # Sélection de la date du 9 mai
        for _ in range(6):
            date_element = page.get_by_label("mai 13,")
            if await date_element.is_visible():
                await date_element.click()
                break
            else:
                await page.locator("ion-calendar").get_by_role("button", name="chevron forward outline").click()

        # Recherche du créneau 16:00 - 20:00
        found_creneau = False
        for direction in ["right", "left"]:
            for _ in range(5):
                await page.locator(f"button.btn-arrow-{direction}").click()
                await page.wait_for_timeout(500)  # Laisser le temps à la page de se mettre à jour
                creneau = await page.locator("div.value").text_content()
                if "16:00 - 20:00" in creneau.lower():
                    found_creneau = True
                    break  # Sortir de la boucle de navigation
            if found_creneau:
                break  # Sortir de la boucle globale
        
        if found_creneau:
            await page.get_by_text("19:00").click()  # Sélection du créneau 19h     
            # Liste des terrains par ordre de préférence
            numero_terrain = [4, 5, 7, 6, 3, 2, 1]
            for i in numero_terrain:
                text_playwright = await page.get_by_text(f"Foot {i} Football 5vs5 - Exté").text_content()
                print(text_playwright)
                    if "Début19:00" in text_playwright and "90" in text_playwright:
                        await page.locator("app-card-playground").filter(has_text=f"Foot {i} Football 5vs5 - Exté").locator("ion-label").filter(has_text="90 min").click()
                        break  # On réserve dès qu'un créneau est trouvé

            # Procédure de réservation
            await page.fill('input[placeholder="john.doe@example.com"]', 'jolie.mountain@gmail.com')
            await page.get_by_text("Valider mon email").click()
            await page.fill('input[placeholder="******"]', 'Toulouse31')
            await page.get_by_text("Valider").click()
            await page.get_by_text("Suivant").click()
            await page.get_by_text("Payer et réserverPayer et ré").click()
            await page.get_by_text("Ajouter une carte").click()
            await page.locator("#ion-overlay-6 ion-radio").click()
            await page.get_by_text("Sélectionner").click()
            await page.get_by_text("Payer et réserver").nth(1).click()
            await page.wait_for_timeout(1000)
            await page.pause()

asyncio.run(main())
