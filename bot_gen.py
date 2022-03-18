from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from colorama import Fore, Back, Style

import os
from random import randint
from time import sleep
from bs4 import BeautifulSoup
from requests import get, post

# Gerador de CC
def gen_cc(count):
    url = "https://www.4devs.com.br:443/ferramentas_online.php"
    data = {"acao": "gerar_cc", "pontuacao": "S", "bandeira": "master"}
    req = post(url, data=data)
    soup = BeautifulSoup(req.text, 'html.parser')

    cartao_numero = soup.find_all('div', id='cartao_numero')[0].text
    # print(cartao_numero[0].text)

    data_validade = soup.find_all('div', id='data_validade')[0].text
    # print(data_validade[0].text)

    codigo_seguranca = soup.find_all('div', id='codigo_seguranca')[0].text
    # print(codigo_seguranca[0].text)
    return cartao_numero, data_validade, codigo_seguranca

print(f"Número Cartão: {gen_cc(1)[0]} \nData Validade: {gen_cc(1)[1]} \nCódigo Segurança: {gen_cc(1)[2]}")

# Generated CPF number
def gen_cpf(count):
    url = "https://www.4devs.com.br:443/ferramentas_online.php"
    data = {"acao": "gerar_cpf", "pontuacao": "S", "cpf_estado": 'SP'}
    for i in range(count):
        req = post(url, data=data)
        return req.text

driver = webdriver.Chrome(ChromeDriverManager().install())
option = Options()
option.headless = False
# option.add_argument("user-data-dir=C:\\User\\Kiqx\\AppData\\Local\\Google\\Chrome\\User Data\\Default") # Seta o diretório do user-data-dir
driver = webdriver.Chrome(ChromeDriverManager().install(), options=option)
driver.maximize_window()
driver.get('https://web.whatsapp.com/')
# sleep(10)
input(f'{Fore.YELLOW}Pressione ENTER após leitura do QRCODE...{Style.RESET_ALL}')

# # Procura por usuario ou grupo
# name = input(f'{Fore.GREEN}Insira nome de usuario ou grupo: {Style.RESET_ALL}')
# user = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//span[@title="{}"]'.format(name))))
# user.click()

# input(f"Press {Fore.GREEN}Enter{Style.RESET_ALL} to continue...")

# Abrir atual diretório
os.chdir(os.path.dirname(os.path.abspath(__file__)))

while True:
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="pane-side"]')))
    html_element = element.get_attribute('outerHTML')
    soup = BeautifulSoup(html_element, 'html.parser')
    try:
        # Quantidade de mensagem recebidas
        message_out = soup.find_all('span', class_='l7jjieqr cfzgl7ar ei5e7seu h0viaqh7 tpmajp1w c0uhu3dl riy2oczp dsh4tgtl sy6s5v3r gz7w46tb lyutrhe2 qfejxiq4 fewfhwl7 ovhn1urg ap18qm3b ikwl5qvt j90th5db aumms1qt')
        # print(f'{Fore.GREEN + message_out[-1].text + Style.RESET_ALL} mensagen(s) recebida(s)')

        # Quem enviou a mensagem
        user = soup.find_all('span', class_='l7jjieqr i0jNr')
        title = soup.find_all('span', class_='ggj6brxn gfz4du6o r7fjleex g0rxnol2 lhj4utae le5p0ye3 l7jjieqr i0jNr')
        print(f'[Message] {Fore.GREEN}{user[-1].text}{Style.RESET_ALL} diz: {Fore.GREEN}{title[-1].text}{Style.RESET_ALL}', end="\r")
        message = title[-1].text
        # sleep(randint(5, 15))

        # Mensagem
        title = soup.find_all('span', class_='ggj6brxn gfz4du6o r7fjleex g0rxnol2 lhj4utae le5p0ye3 l7jjieqr i0jNr')
        message = title[-1].text
        # print(f'{Fore.GREEN + message + Style.RESET_ALL}')
        # print(f'Mensagem recebida: {Fore.GREEN + title[-1].text + Style.RESET_ALL}')

        # # Grupo ou pessoa
        text = soup.find_all('span', class_='ggj6brxn gfz4du6o r7fjleex g0rxnol2 lhj4utae le5p0ye3 l7jjieqr i0jNr')
        user_id = text[-2].text
        # print(f'Grupo/Usuario { Fore.GREEN + text[-2].text + Style.RESET_ALL}\n')

        if message.startswith('#CPF'):
            user_message = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//span[@title="{}"]'.format(f"{user_id}"))))
            user_message.click()

            search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//div[@contenteditable="true"][@data-tab="10"]')))
            search_box.send_keys(f'[INFO] CPF {gen_cpf(1)} - Fonte: 4devs.com.br\n')

        if message.startswith('#CC'):
            user_message = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//span[@title="{}"]'.format(f"{user_id}"))))
            user_message.click()

            search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//div[@contenteditable="true"][@data-tab="10"]')))
            search_box.send_keys(f'[INFO] Número Cartão: {gen_cc(1)[0]} - Fonte: 4devs.com.br\n')
            search_box.send_keys(f'[INFO] Data Validade: {gen_cc(1)[1]} - Fonte: 4devs.com.br\n')
            search_box.send_keys(f'[INFO] Código Segurança: {gen_cc(1)[2]} - Fonte: 4devs.com.br\n')

    except Exception as e:
        # print(f"[{Fore.RED}ERROR{Style.RESET_ALL}]{Fore.RED}{e}{Style.RESET_ALL}", end="\r")
        print(f"[{Fore.YELLOW}WAIT{Style.RESET_ALL}] Aguardando mensagem... ", end="\r")
        pass
