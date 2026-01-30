# import time
# import random
# import pandas as pd
# from selenium import webdriver
# from selenium.webdriver.common.by import By # libreria para localizar elementos
# from selenium.webdriver.common.keys import Keys # libreria para usar teclas especiales
# from selenium.webdriver.chrome.service import Service
# # from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# # Configuration variables

# USER_X = "Predecir27ULL"
# PASSWORD_X = "Mario123"
# EMAIL_X = "alu0101395036@ull.edu.es"
# SEARCH_QUERY = "elecciones españa 2023 -filter:retweets"
# MAX_TWEETS = 100 # Maximum number of tweets to scrape (100 for demo purposes)

# def initialize_driver():
#     options = webdriver.ChromeOptions()
    
#     # 1. Rutas de perfil (Igual que antes)
#     user_data_dir = "/Users/marioguerraperez/Library/Application Support/Google/Chrome" 
#     options.add_argument(f"--user-data-dir={user_data_dir}")
#     options.add_argument("--profile-directory=Default") 
    
#     # 2. Configuración de Puerto (Igual que antes)
#     options.add_argument("--remote-debugging-port=9222")

#     # 3. --- FIX VITAL PARA QUE NO SE QUEDE CONGELADO ---
#     # Esto permite que Selenium se conecte al navegador abierto
#     options.add_argument("--remote-allow-origins=*") 
#     # --------------------------------------------------

#     # 4. Otras opciones
#     options.add_argument("--disable-blink-features=AutomationControlled") 
#     options.add_experimental_option("excludeSwitches", ["enable-automation"])
#     options.add_experimental_option('useAutomationExtension', False)
#     options.add_argument("--disable-notifications")
#     options.add_argument("--start-maximized")
    
#     driver = webdriver.Chrome(options=options)
    
#     # Añadimos un tiempo de espera explícito para que la página cargue
#     driver.set_page_load_timeout(30) 
    
#     return driver

# # def login_twitter(driver):
# #   print ("Logging in to Twitter...")
# #   driver.get("https://twitter.com/i/flow/login")
# #   time.sleep(random.uniform(4, 7))  # Random sleep to mimic human behavior
# #   print ("Entering username...")
# #   try:
# #     user_input = WebDriverWait(driver, 10).until(
# #       EC.presence_of_element_located((By.XPATH, "//input[@name='text']")) # Wait for password field to load
# #     )
# #     user_input.send_keys(USER_X)
# #     user_input.send_keys(Keys.RETURN)
# #     time.sleep(random.uniform(2, 4))
# #     print("Login successful.")
    
    
# #   except Exception as e:
# #     print("An error occurred during login:", e)
# #     return False
  
# #   print("Entering password...")
# #   try:
# #     pass_input = WebDriverWait(driver, 10).until(
# #       EC.presence_of_element_located((By.NAME, "password")) # Wait for password field to load
# #     )
# #     print ("Password field located.")
# #   except Exception as e:
# #     print("An error occurred locating password field:", e)
# #     try:
# #       verify_input = WebDriverWait(driver, 5).until(
# #         EC.presence_of_element_located((By.XPATH, "//input[@name='text']")) # O data-testid='ocfEnterTextTextInput'
# #       )
# #       print ("Introduce email for verification...")
# #       verify_input.send_keys(EMAIL_X)
# #       verify_input.send_keys(Keys.RETURN)
# #       time.sleep(random.uniform(3, 5))
      
# #       pass_input = WebDriverWait(driver, 10).until(
# #         EC.presence_of_element_located((By.NAME, "password")) # Wait for password field to load
# #       )
# #       print ("Password field located after email verification.")
# #     except Exception as e:
# #       print("An error occurred during email verification:", e)
# #       return False
# #   try:
# #     pass_input.send_keys(PASSWORD_X)
# #     pass_input.send_keys(Keys.RETURN)
# #     time.sleep(random.uniform(5, 7))
# #   except Exception as e:
# #     print("An error occurred entering password:", e)
# #     return False
# #   if "flow" not in driver.current_url:
# #     print("Logged in successfully.")
# #     return True
# #   else:
# #     print("Login failed.")
# #     return False
  
  
# def check_login_status(driver):
#   driver.get("https://twitter.com/home")
#   time.sleep(random.uniform(3, 5))
#   if "home" in driver.current_url:
#     print("User is logged in.")
#     return True
#   else:
#     print("User is not logged in.")
#     print("Login handling required.")
#     time.sleep(30) # time to manually login
#     return "home" in driver.current_url

# if __name__ == "__main__":
#   # test the login function
#   driver = None
#   try:
#     driver = initialize_driver()
#     if check_login_status(driver):
#       print("Already logged in.")
#     else:
#       print("Not logged in, attempting login...")
    
#   except Exception as e:
#     print("An error occurred:", e)
#   finally:
#     print ("Closing the driver...")
#     if driver is not None:
#       time.sleep(15)
#       driver.quit()


import time
import pickle
import os
import random
import pandas as pd
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC # libreria para condiciones esperadas
from urllib.parse import quote_plus # para URL encoding

#SEARCH_QUERY = "elecciones españa 2027 lang:es -filter:retweets"
MAX_TWEETS = 1000  # Reducido para ser menos agresivo

def initialize_driver():
  options = uc.ChromeOptions()
  
  options.add_argument("--disable-notifications")
  options.add_argument("--disable-popup-blocking")
  options.add_argument("--disable-dev-shm-usage")
  options.add_argument("--no-sandbox")
  options.add_argument("--disable-gpu")
  
  try:
    driver = uc.Chrome(options=options, use_subprocess=False, version_main=144)  # use_subprocess=False para mayor estabilidad, version_main=144 para compatibilidad
    driver.set_page_load_timeout(45)
    time.sleep(2)  # Pequeña pausa después de crear el driver
    return driver
  except Exception as e:
    print(f"Error inicializando driver: {e}")
    raise

def load_cookies(driver, max_retries=3):
  cookies_path = "src/data_loaders/twitter_cookies.pkl"
  if not os.path.exists(cookies_path):
    print("No se encontraron cookies guardadas. Ejecuta setup_login.py primero y siga las instrucciones.")
    return False
  
  for attempt in range(max_retries):
    print(f"[Intento {attempt + 1}/{max_retries}] Cargando cookies...")
    try:
      # Verifica si el driver aún está vivo
      _ = driver.current_url
      
      driver.get("https://x.com/")
      time.sleep(random.uniform(3, 5))
      
      cookies = pickle.load(open(cookies_path, "rb"))
      for cookie in cookies:
        try:
          driver.add_cookie(cookie)
        except:
          pass  # Ignorar cookies que no se puedan añadir
      
      print("Refrescando la página para aplicar cookies...")
      driver.refresh()
      time.sleep(5)
      
      current_url = driver.current_url
      if "home" in current_url or "search" in current_url or "x.com" in current_url:
        print("✓ Login exitoso mediante cookies.")
        return True
      
      print("⚠ Las cookies no funcionaron en este intento, reintentando...")
      time.sleep(3)
      
    except Exception as e:
      print(f"[!] Error al cargar cookies (intento {attempt + 1}): {type(e).__name__}")
      # Si el driver está muerto, no vale la pena reintentar
      if "no such window" in str(e).lower() or "target window" in str(e).lower():
        print("Driver está muerto, necesita reinicializarse.")
        return False
      time.sleep(3)
      continue
  
  print("✗ No se pudieron cargar las cookies tras varios intentos.")
  return False
  
def wait_for_results_or_retry(driver, timeout=20, max_retries=5):
  for attempt in range(max_retries):
    try:
      time.sleep(random.uniform(3, 6))  # Espera aleatoria para parecer más humano

      # Si aparece el mensaje de error
      error_nodes = driver.find_elements(By.XPATH, "//*[contains(text(),'Something went wrong')]")
      if error_nodes:
        print(f"[X] Error de carga (attempt {attempt+1}/{max_retries}). Reintentando...")

        # Intenta click en Retry si existe
        retry_btn = driver.find_elements(By.XPATH, "//div[@role='button']//span[text()='Retry']/ancestor::div[@role='button']")
        if retry_btn:
          try:
            retry_btn[0].click()
            time.sleep(5)
          except:
            driver.refresh()
            time.sleep(5)
        else:
          driver.refresh()
          time.sleep(5)
        continue

      # Si ya hay tweets, sal
      tweets = driver.find_elements(By.XPATH, "//article[@data-testid='tweet']")
      if tweets:
        print(f"[✓] Resultados cargados ({len(tweets)} tweets iniciales)")
        return True
      
      time.sleep(3)

    except Exception as e:
      print(f"[!] Excepción en wait_for_results: {e}")
      time.sleep(3)
      continue

  print("[X] No se pudieron cargar los resultados tras varios intentos")
  return False

  
def extract_tweets(driver, search_query):
  print(f"Looking for: {search_query}")
  query_url = quote_plus(search_query)
  
  try:
    driver.get(f"https://x.com/search?q={query_url}&src=typed_query&f=live")
    time.sleep(random.uniform(6, 10))  # Espera aleatoria inicial más larga
    
    if not wait_for_results_or_retry(driver, timeout=20, max_retries=5):
      print("No se pudieron cargar los resultados de búsqueda tras varios intentos.")
      return pd.DataFrame([])
    
    try:
      WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, '//article[@data-testid="tweet"]'))
      )
      print("Search results loaded.")
    except:
      print("Timeout esperando tweets, continuando con lo que haya...")
      time.sleep(3)
      
    tweets_data = []
    tweets_ids = set()
    last_height = driver.execute_script("return document.body.scrollHeight")
    no_changes_counter = 0
    scroll_count = 0
    max_scrolls = 25  # Reducido para ser menos agresivo
    
    while len(tweets_data) < MAX_TWEETS and scroll_count < max_scrolls:
      try:
        cards = driver.find_elements(By.XPATH, '//article[@data-testid="tweet"]')
        
        for card in cards:
          try:
            text_elem = card.find_element(By.XPATH, './/div[@data-testid="tweetText"]')
            text = text_elem.text.replace("\n", " ")
            
            if text not in tweets_ids:
              try:
                user_elem = card.find_element(By.XPATH, './/div[@data-testid="User-Name"]//span[contains(text(), "@")]')
                username = user_elem.text
                if username == "@grok":
                  continue
              except:
                username = "Unknown"
              
              tweets_ids.add(text)
              tweets_data.append({
                "username": username,
                "text": text,
                "extract_date": time.strftime("%Y-%m-%d %H:%M:%S")
              })
              if len(tweets_data) % 50 == 0:
                print(f"({len(tweets_data)} / {MAX_TWEETS}) {username}: {text[:50]}...")
          except Exception as e:
            continue
        
        # Scroll down con comportamiento más humano
        scroll_pause = random.uniform(6, 10)  # Pausas más largas y aleatorias
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause)
        scroll_count += 1
        
        # Pausa extra cada 5 scrolls para simular lectura
        if scroll_count % 5 == 0:
          extra_pause = random.uniform(3, 7)
          print(f"[Pausa de lectura: {extra_pause:.1f}s]")
          time.sleep(extra_pause)
        
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        if new_height == last_height:
          no_changes_counter += 1
          # Aumenta el umbral para detectar fin de resultados
          if no_changes_counter >= 5:  
            print(f"No se encontraron más tweets nuevos (intentos sin cambios: {no_changes_counter}).")
            break
        else:
          no_changes_counter = 0
        
        last_height = new_height
        
        # Muestra progreso cada cierto tiempo
        if scroll_count % 10 == 0:
          print(f"[Scroll {scroll_count}/{max_scrolls}] Tweets extraídos: {len(tweets_data)}")
        
      except Exception as e:
        print(f"Error durante scroll: {e}")
        break
    
    print(f"\n✓ Scraping completado: {len(tweets_data)} tweets extraídos en {scroll_count} scrolls")
        
  except Exception as e:
    print(f"Error general en extract_tweets: {e}")
    return pd.DataFrame([])
    
  return pd.DataFrame(tweets_data)
if __name__ == "__main__":
  # array de palabras para en cada iteracion, hacer una busqueda diferente y que no sea siempre la misma
  #SEARCH_QUERIES = ["elecciones españa 2027 lang:es -filter:retweets", "política españa 2027 lang:es -filter:retweets", "gobierno españa 2027 lang:es -filter:retweets", "españa 2027 lang:es -filter:retweets", "perro xanche lang:es -filter:retweets"]
  SEARCH_QUERIES = [
    # Elecciones / marco general
    
    '"elecciones generales" lang:es -filter:retweets',
    '"elecciones 2027" lang:es -filter:retweets',
    '"campaña electoral" lang:es -filter:retweets',
    '"votar" lang:es -filter:retweets',
    '"voto" lang:es -filter:retweets',
    '"jornada electoral" lang:es -filter:retweets',
    '"debate electoral" lang:es -filter:retweets',

    # Partidos y líderes
    'PSOE lang:es -filter:retweets',
    '"Partido Socialista" lang:es -filter:retweets',
    '"Pedro Sánchez" lang:es -filter:retweets',
    'PP lang:es -filter:retweets',
    '"Partido Popular" lang:es -filter:retweets',
    'Feijóo lang:es -filter:retweets',
    '"Núñez Feijóo" lang:es -filter:retweets',
    'VOX lang:es -filter:retweets',
    'Abascal lang:es -filter:retweets',
    '"Santiago Abascal" lang:es -filter:retweets',
    'Sumar lang:es -filter:retweets',
    '"Yolanda Díaz" lang:es -filter:retweets',
    'Podemos lang:es -filter:retweets',
    '"Ione Belarra" lang:es -filter:retweets',
    '"Irene Montero" lang:es -filter:retweets',
    'ERC lang:es -filter:retweets',
    'Junts lang:es -filter:retweets',
    'PNV lang:es -filter:retweets',
    'Bildu lang:es -filter:retweets',

    # Intención de voto
    '"voy a votar" lang:es -filter:retweets',
    '"votaré a" lang:es -filter:retweets',
    '"mi voto" lang:es -filter:retweets',
    '"no pienso votar" lang:es -filter:retweets',
    '"cambiaré mi voto" lang:es -filter:retweets',
    '"esta vez votaré" lang:es -filter:retweets',
    '"mi voto será" lang:es -filter:retweets',
    '"mi voto va para" lang:es -filter:retweets',

    # Issues - Economía
    'inflación lang:es -filter:retweets',
    '"salario mínimo" lang:es -filter:retweets',
    '"coste de la vida" lang:es -filter:retweets',
    
    # Issues - Vivienda
    'hipoteca lang:es -filter:retweets',
    'alquiler lang:es -filter:retweets',
    'vivienda lang:es -filter:retweets',
    '"ley de vivienda" lang:es -filter:retweets',
    
    # Issues - Empleo
    'paro lang:es -filter:retweets',
    'desempleo lang:es -filter:retweets',
    '"reforma laboral" lang:es -filter:retweets',
    '"contrato indefinido" lang:es -filter:retweets',
    
    # Issues - Inmigración
    'inmigración lang:es -filter:retweets',
    'fronteras lang:es -filter:retweets',
    'menas lang:es -filter:retweets',
    '"regularización" lang:es -filter:retweets',
    
    # Issues - Independencia y Cataluña
    'amnistía lang:es -filter:retweets',
    'Cataluña lang:es -filter:retweets',
    'independencia lang:es -filter:retweets',
    'referéndum lang:es -filter:retweets',
    
    # Issues - Corrupción
    'corrupción lang:es -filter:retweets',
    'escándalo lang:es -filter:retweets',
    'dimisión lang:es -filter:retweets',

    # Hashtags generales
    '#Elecciones lang:es -filter:retweets',
    '#EleccionesGenerales lang:es -filter:retweets',
    '#España lang:es -filter:retweets',
    '#Política lang:es -filter:retweets',
    '#PSOE lang:es -filter:retweets',
    '#PP lang:es -filter:retweets',
    '#VOX lang:es -filter:retweets',
    '#Sumar lang:es -filter:retweets',
    '#Podemos lang:es -filter:retweets',

    # Polarización / emoción
    '"estoy harto" lang:es -filter:retweets',
    '"estoy harta" lang:es -filter:retweets',
    '"es una vergüenza" lang:es -filter:retweets',
    'indignante lang:es -filter:retweets',
    # Consultas 2.0 -> consultas que se han tenido que repetir por limite de tweets y otras extras
    '"Campaña electoral" lang:es -filter:retweets',
    '"Perro Xanche" lang:es -filter:retweets',
    'Podemos lang:es -filter:retweets',
    'Junts lang:es -filter:retweets',
    '"Voy a votar a" lang:es -filter:retweets',
    'Inflación" lang:es -filter:retweets',
    'Hipoteca" lang:es -filter:retweets',
    '"No pienso votar" lang:es -filter:retweets',
    '"Esta vez votaré" lang:es -filter:retweets',
    'Inmigración lang:es -filter:retweets',
    'fronteras lang:es -filter:retweets',
    '"#PP" lang:es -filter:retweets',
    'Amnistía lang:es -filter:retweets',
    'referéndum lang:es -filter:retweets',
    'Dimisión lang:es -filter:retweets',
    'Moncloa lang:es -filter:retweets',
    'okupa lang:es -filter:retweets',
    'boe lang:es -filter:retweets',
    'constitución lang:es -filter:retweets',
    'hacienda lang:es -filter:retweets',
    'sanchez lang:es -filter:retweets',
    'ministerio lang:es -filter:retweets',
    'parlamento lang:es -filter:retweets',
    'senado lang:es -filter:retweets',
    'urnas lang:es -filter:retweets',
    '"Colegio Electoral" lang:es -filter:retweets',
    '"Ley de la Vivienda" lang:es -filter:retweets',
    '"Reforma Laboral" lang:es -filter:retweets',
    '"Ministerio de transporte" lang:es -filter:retweets',
    '"Ministerio de educación" lang:es -filter:retweets',
    '"Ministerio de sanidad" lang:es -filter:retweets',
    '"Ministerio de defensa" lang:es -filter:retweets',
    '"Ministerio de interior" lang:es -filter:retweets',
    '"Ministerio de justicia" lang:es -filter:retweets',
    'Mazón lang:es -filter:retweets',
    'Dana lang:es -filter:retweets',
    '"Oscar Puente" lang:es -filter:retweets',
    'prostitución lang:es -filter:retweets',
    'prostitutas lang:es -filter:retweets',
    'pederastia lang:es -filter:retweets',
    'trafico sexual lang:es -filter:retweets',
    'trata de blancas lang:es -filter:retweets',
    'trafico lang:es -filter:retweets',
    'narcotráfico lang:es -filter:retweets',
    'drogas lang:es -filter:retweets',
    '"fontaneros PSOE" lang:es -filter:retweets',
    '"Caso Abalos" lang:es -filter:retweets',
    '"Caso Koldo" lang:es -filter:retweets',
    'Zapatero lang:es -filter:retweets',
    'Maduro Zapatero lang:es -filter:retweets',
    'Maduro Pedro Sanchez lang:es -filter:retweets',
    'Moros lang:es -filter:retweets',
    'Marroquies lang:es -filter:retweets',
    'Marruecos lang:es -filter:retweets', 
  ]
  for i in range(SEARCH_QUERIES.__len__()):
    print(f"\n{'='*60}")
    print(f"Search query {i + 1}/{len(SEARCH_QUERIES)}: {SEARCH_QUERIES[i]}")
    print(f"{'='*60}")
    driver = None
    cookies_loaded = False
    max_cookie_retries = 2  # Reducido porque si falla dos veces es mejor hacer nuevo driver
    
    try:
      # Reintentos para cargar cookies
      for cookie_attempt in range(max_cookie_retries):
        try:
          driver = initialize_driver()
          if load_cookies(driver, max_retries=2):
            cookies_loaded = True
            break
          else:
            print(f"✗ Fallo cargando cookies (intento {cookie_attempt + 1}/{max_cookie_retries})")
            if driver is not None:
              try:
                driver.quit()
                time.sleep(2)
              except:
                pass
            if cookie_attempt < max_cookie_retries - 1:
              print(f"Esperando 20 segundos antes de reintentar...")
              time.sleep(20)
        except Exception as e:
          print(f"✗ Error creando driver: {e}")
          if driver is not None:
            try:
              driver.quit()
            except:
              pass
      
      if not cookies_loaded:
        print("✗ No se pudo iniciar sesión tras varios intentos. Saltando esta búsqueda...")
        counter_search += 1
        continue
      
      print("Extracting tweets...")
      df_tweets = extract_tweets(driver, SEARCH_QUERIES[i])
      import os
      os.makedirs("data/raw/social_media", exist_ok=True)
      print(f"Extracted {len(df_tweets)} tweets.")
      df_tweets.to_csv(f"data/raw/social_media/[{i + 150}]twitter_scraped_tweets_.csv", index=False, encoding="utf-8-sig")
      print(f"✓ Tweets saved to data/raw/social_media/[{i + 150}]twitter_scraped_tweets_.csv")
    except Exception as e:
      print(f"✗ An error occurred: {e}")
    finally:
      if driver is not None:
        try:
          print("Closing driver...")
          driver.quit()
          time.sleep(1)
        except:
          pass
      # Aumenta tiempo de espera entre búsquedas con variación aleatoria
      wait_time = random.uniform(90, 120)  # Entre 1.5 y 2 minutos
      print(f"Waiting {wait_time:.0f} seconds before next query...")
      time.sleep(wait_time)
    
    
    
    
  
