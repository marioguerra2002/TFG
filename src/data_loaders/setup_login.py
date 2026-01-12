import time
import pickle
import undetected_chromedriver as uc

def guardar_cookies():
    print("🚀 Iniciando navegador INDETECTABLE...")
    
    # Esta librería se encarga sola de buscar tu Chrome y parchearlo
    # No necesitamos configurar rutas ni puertos raros.
    driver = uc.Chrome(use_subprocess=True)
    
    try:
        driver.get("https://x.com/i/flow/login")
        
        print("\n" + "="*60)
        print("🕵️  MODO INDETECTABLE ACTIVADO")
        print("1. Twitter ahora cree que eres un humano real.")
        print("2. Inicia sesión tranquilamente (tienes 3 minutos).")
        print("3. Si te pide código o captcha, resuélvelo.")
        print("4. CUANDO VEAS EL TIMELINE (Tus tweets), vuelve aquí.")
        print("="*60 + "\n")
        
        input("👉 PULSA ENTER AQUÍ CUANDO YA ESTÉS DENTRO DE TWITTER...")
        
        # Guardar cookies
        import os
        os.makedirs("src/data_loaders", exist_ok=True)
        cookies = driver.get_cookies()
        pickle.dump(cookies, open("src/data_loaders/twitter_cookies.pkl", "wb"))
        print("✅ ¡Cookies guardadas! Ahora Twitter recordará quién eres.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    guardar_cookies()