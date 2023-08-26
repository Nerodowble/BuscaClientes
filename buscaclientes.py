from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time

# Inicializar o driver do Chrome

chrome_path = r'C:\Users\willi\Desktop\ChromeDriver\chromedriver.exe'
service = Service(chrome_path)
driver = webdriver.Chrome(service=service)
# Opções para desabilitar a verificação de SSL
options = webdriver.ChromeOptions()
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--ignore-certificate-errors')

# Inicializar o driver do Chrome com as opções
driver = webdriver.Chrome(service=service, options=options)

# Abrir o LinkedIn
driver.get("https://www.linkedin.com/checkpoint/rm/sign-in-another-account?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")

# Esperar o carregamento da página de login
time.sleep(5)

# Localizar os elementos de login e senha usando XPath
login_element = driver.find_element(By.ID, "username")
senha_element = driver.find_element(By.ID, "password")

# Preencher os campos de login e senha
login_element.send_keys("willian.lima@legalbot.com.br")
senha_element.send_keys("Trymore1@3")

# Localizar o botão de login e clicar nele
botao_login = driver.find_element(By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "from__button--floating", " " ))]')
botao_login.click()

# Aguardar o redirecionamento
time.sleep(10)

# Esperar até que o campo de pesquisa esteja visível e interagível
wait = WebDriverWait(driver, 3)
barra_pesquisa = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#global-nav-search input')))

# Clicar na barra de pesquisa
barra_pesquisa.click()

# Inserir um exemplo de busca
barra_pesquisa.send_keys("Compliance")

# Pressionar Enter para realizar a pesquisa
barra_pesquisa.send_keys(Keys.RETURN)

time.sleep(5)

wait = WebDriverWait(driver, 10)
botao_pessoas = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div[3]/div[2]/div/div[1]/main/div/div/div[5]/div/div[2]/a')))
botao_pessoas.click()

# Aguardar um pouco para carregar a página de todos os resultados
time.sleep(3)

# Localizar todos os elementos que contêm os nomes dos perfis
nomes_elementos = driver.find_elements(By.XPATH, '/html/body/div[5]/div[3]/div[2]/div/div[1]/main/div/div/div[3]/div/ul/li/div/div/div[2]/div[1]/div[1]/div/span[1]/span/a/span/span[1]')

# Filtrar apenas os elementos com nomes diferentes de "Usuário do LinkedIn"
perfis_nao_genericos = [elemento for elemento in nomes_elementos if elemento.text != "Usuário do LinkedIn"]

# Acessar as páginas dos perfis não genéricos
for i in range(len(perfis_nao_genericos)):
    # Localizar novamente todos os elementos que contêm os nomes dos perfis
    nomes_elementos = driver.find_elements(By.XPATH, '/html/body/div[5]/div[3]/div[2]/div/div[1]/main/div/div/div[3]/div/ul/li/div/div/div[2]/div[1]/div[1]/div/span[1]/span/a/span/span[1]')

    # Filtrar apenas os elementos com nomes diferentes de "Usuário do LinkedIn"
    perfis_nao_genericos = [elemento for elemento in nomes_elementos if elemento.text != "Usuário do LinkedIn"]

    # Acessar o perfil atual
    if i < len(perfis_nao_genericos):
        perfil = perfis_nao_genericos[i]
        nome_perfil = perfil.text
        perfil.click()  # Clicar no link para acessar a página do perfil

        # Aguardar um pouco para carregar a página do perfil
        time.sleep(3)

        try:
            # Clicar no botão "Sobre" se ele existir
            botao_sobre = driver.find_element(By.XPATH, '//*[@id="top-card-text-details-contact-info"]')
            botao_sobre.click()
            time.sleep(3)

            try:
                # Localizar e imprimir o nome
                nome = driver.find_element(By.CSS_SELECTOR, 'h1.text-heading-xlarge.inline.t-24.v-align-middle.break-words').text
                print("Nome:", nome)
            except Exception as e:
                print("Nome não encontrado")

            try:
                # Localizar e imprimir o perfil do LinkedIn
                perfil_linkedin = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[2]/section/div/section[1]/div/a')
                print("Perfil LinkedIn:", perfil_linkedin.get_attribute("href"))
            except Exception as e:
                print("Perfil do LinkedIn não encontrado")

            try:
                # Localizar e imprimir o email pessoal
                email_pessoal = driver.find_element(By.CSS_SELECTOR, 'section.pv-contact-info__contact-type.ci-email a.pv-contact-info__contact-link')
                print("Email pessoal:", email_pessoal.get_attribute("href"))
            except Exception as e:
                print("Email pessoal não encontrado")

        except Exception as e:
            print("Não foi possível acessar as informações do perfil:", e)

        # Voltar à página de resultados de pesquisa
        driver.back()

        # Aguardar um pouco após voltar à página de resultados
        time.sleep(3)

        # Voltar à página de resultados de pesquisa
        driver.back()

while True:
    try:
        # Verificar se o botão de avançar está presente e clicável
        botao_avancar = driver.find_element(By.XPATH, '//button[contains(text(), "Avançar")]')
        if botao_avancar.is_enabled():
            botao_avancar.click()
            time.sleep(3)
        else:
            print("Botão de avançar não está clicável.")
            break
    except NoSuchElementException:
        print("Fim das páginas.")
        break

# Fechar o navegador
driver.quit()
