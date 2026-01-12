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
import pandas as pd
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

#SEARCH_QUERY = "elecciones españa 2027 lang:es -filter:retweets"
MAX_TWEETS = 1000000000000

def initialize_driver():
  options = uc.ChromeOptions()
  
  options.add_argument("--disable-notifications")
  
  driver = uc.Chrome(options=options, use_subprocess=True)
  return driver

def load_cookies(driver):
  cookies_path = "src/data_loaders/twitter_cookies.pkl"
  if not os.path.exists(cookies_path):
    print("No se encontraron cookies guardadas. Ejecuta setup_login.py primero y siga las instrucciones.")
    return False
  print ("reading cookies from twitter_cookies.pkl...")
  try:
    driver.get("https://x.com/")
    cookies = pickle.load(open(cookies_path, "rb"))
    for cookie in cookies:
      try:
        driver.add_cookie(cookie)
      except:
        pass # Ignorar cookies que no se puedan añadir (no critico)
    print("Refrescando la página para aplicar cookies...")
    driver.refresh()
    time.sleep(5) # Esperar a que la página cargue
    
    current_url = driver.current_url
    if "home" in current_url or "search" in current_url:
      print("Login exitoso mediante cookies.")
      return True
    print ("Las cookies no funcionaron, es posible que hayan expirado.")
    return False
  except Exception as e:
    print(f"Error al cargar cookies: {e}")
    return False
  
def extract_tweets(driver, search_query):
  print(f"Looking for: {search_query}")
  query_url = search_query.replace(" ", "%20") # el %20 es espacio en URL encoding
  
  driver.get(f"https://x.com/search?q={query_url}&src=typed_query&f=live")
  time.sleep(5) # Esperar a que la página cargue
  tweets_data = []
  tweets_ids = set()
  last_height = driver.execute_script("return document.body.scrollHeight") # Altura inicial de la página
  no_changes_counter = 0 # Contador para detectar si no hay más tweets nuevos
  while len(tweets_data) < MAX_TWEETS:
    cards = driver.find_elements(By.XPATH, '//article[@data-testid="tweet"]') # Localizar tweets en la página 
    for card in cards:
      try:
        text_elem = card.find_element(By.XPATH, './/div[@data-testid="tweetText"]')
        text = text_elem.text.replace("\n", " ")
        if text not in tweets_ids: # Evitar duplicados
          try:
            user_elem = card.find_element(By.XPATH, './/div[@data-testid="User-Name"]//span[contains(text(), "@")]')
            # si el nombre de usuario es @grok, no se coge, ya que es de IA
            username = user_elem.text
            if user_elem.text == "@grok":
              continue
          except:
            username = "Unknown"
          tweets_ids.add(text)
          tweets_data.append({
            "username": username,
            "text": text,
            "extract_date": time.strftime("%Y-%m-%d %H:%M:%S")
          })
          print(f"({len(tweets_data)} / {MAX_TWEETS}) {username}: {text[:50]}...")
      except:
        continue # Si hay error con un tweet, continuar con el siguiente
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # Scroll down
    time.sleep(3.5) # Esperar a que carguen más tweets
    new_height = driver.execute_script("return document.body.scrollHeight") # Nueva altura de la página 
    # comparar alturas para ver si hay más contenido. Si no cambia, puede que no haya más tweets
    if new_height == last_height:
      no_changes_counter += 1
      if no_changes_counter >= 3: # Si no hay cambios tras varios intentos, salir
        print("No se encontraron más tweets nuevos.")
        break
    else:
      no_changes_counter = 0
    last_height = new_height
    
  return pd.DataFrame(tweets_data)
if __name__ == "__main__":
  driver = initialize_driver()
  # array de palabras para en cada iteracion, hacer una busqueda diferente y que no sea siempre la misma
  #SEARCH_QUERIES = ["elecciones españa 2027 lang:es -filter:retweets", "política españa 2027 lang:es -filter:retweets", "gobierno españa 2027 lang:es -filter:retweets", "españa 2027 lang:es -filter:retweets", "perro xanche lang:es -filter:retweets"]
  SEARCH_QUERIES = ["política españa 2027 lang:es -filter:retweets", "perro xanche lang:es -filter:retweets"]
  try:
    if load_cookies(driver):
      for number_doc in range(SEARCH_QUERIES.__len__()):
        print("Extracting tweets...")
        df_tweets = extract_tweets(driver, SEARCH_QUERIES[number_doc - 1])
        
        import os
        os.makedirs("data/raw/social_media", exist_ok=True)
        print(f"Extracted {len(df_tweets)} tweets.")
        df_tweets.to_csv(f"data/raw/social_media/[{number_doc}]twitter_scraped_tweets_.csv", index=False, encoding="utf-8-sig")
        print(f"Tweets saved to data/raw/social_media/[{number_doc}]twitter_scraped_tweets_.csv")
    else:
      print("No se pudo iniciar sesión. Ejecuta setup_login.py primero.")
  except Exception as e:
    print(f"An error occurred: {e}")
  finally:
    print("Closing driver...")
    driver.quit()
    
  
