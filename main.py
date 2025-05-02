import os
import sys
import time
import asyncio
import requests
import random
from colorama import Fore, Style, init

init(autoreset=True)

# Cores
green = Fore.GREEN
white = Fore.WHITE
magenta = Fore.LIGHTMAGENTA_EX
red = Fore.RED
reset = Style.RESET_ALL

# Terminal utilitários
def clear_cmd():
    os.system('cls' if os.name == 'nt' else 'clear')

def centralizar_texto(texto, largura=80):
    return texto.center(largura)

def mostrar_banner_verde_musgo():
    clear_cmd()
    banner = [
        "• ▌ ▄ ·. ▪   ▐ ▄  ▄▄ •             ",
        "·██ ▐███▪██ •█▌▐█▐█ ▀ ▪▪     ▪     ",
        "▐█ ▌▐▌▐█·▐█·▐█▐▐▌▄█ ▀█▄ ▄█▀▄  ▄█▀▄ ",
        "██ ██▌▐█▌▐█▌██▐█▌▐█▄▪▐█▐█▌.▐▌▐█▌.▐▌",
        "▀▀  █▪▀▀▀ ▀▀▀▀▀ █▪·▀▀▀▀  ▀█▄▀▪ ▀█▄▀▪"
    ]
    largura_terminal = os.get_terminal_size().columns
    for linha in banner:
        print(green + centralizar_texto(linha, largura_terminal))
        time.sleep(0.05)
    print(white + centralizar_texto("Painel DM Nuker - by @gqai", largura_terminal) + reset)

async def digitar_texto_animado(texto, delay=0.002, cor=Fore.LIGHTMAGENTA_EX):
    for linha in texto.splitlines():
        for caractere in linha:
            print(cor + caractere, end='', flush=True)
            await asyncio.sleep(delay)
        print()

async def mostrar_creditos():
    clear_cmd()
    mostrar_banner_verde_musgo()
    ascii_art = r"""
                     :::!~!!!!!:.
                  .xUHWH!! !!?M88WHX:.
                .X*#M@$!!  !X!M$$$$$$WWx:.
               :!!!!!!?H! :!$!$$$$$$$$$$8X:
              !!~  ~:~!! :~!$!#$$$$$$$$$$8X:
             :!~::!H!<   ~.U$X!?R$$$$$$$$MM!           
             ~!~!!!!~~ .:XW$$$U!!?$$$$$$RMM!                                       
               !:~~~ .:!M"T#$$$$WX??#MRRMMM!
               ~?WuxiW*`   `"#$$$$8!!!!??!!!   
             :X- M$$$$       `"T#$T~!8$WUXU~
            :%`  ~#$$$m:        ~!~ ?$$$$$$
          :!`.-   ~T$$$$8xx.  .xWW- ~""##*"
.....   -~~:<` !    ~?T#$$@@W@*?$$      /`
W$@@M!!! .!~~ !!     .:XUW$W!~ `"~:    :
#"~~`.:x%`!!  !H:   !WM$$$$Ti.: .!WUn+!`
:::~:!!`:X~ .: ?H.!u "$$$B$$$!W:U!T$$M~
.~~   :X@!.-~   ?@WTWo("*$$$W$TH$! `
Wi.~!X$?!-~    : ?$$$B$Wu("**$RM!
$R@i.~~ !     :   ~$$$$$B$$en:`` 
?MXT@Wx.~    :     ~"##*$$$$M~
"""
    await digitar_texto_animado(ascii_art, delay=0.0008, cor=magenta)
    texto_credito = (
        "\n\nProjeto feito por @gqai (mingoo) com intuito de aprendizado\n"
        "https://instagram.com/mingoocry"
    )
    await digitar_texto_animado(texto_credito, delay=0.01, cor=white)
    input("\nPressione Enter para voltar ao menu...")

# Lógica de limpeza de DMs
def fetch_messages(headers, channel_id, author_id):
    messages = []
    url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
    print(f"{Fore.CYAN}Buscando mensagens...{reset}")

    while True:
        params = {"limit": 100}
        if messages:
            params["before"] = messages[-1]

        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            if response.status_code != 200:
                print(f"{red}Erro ao acessar o canal. Status Code: {response.status_code}{reset}")
                return []
            data = response.json()
            if not data:
                break

            user_messages = [msg["id"] for msg in data if msg["author"]["id"] == author_id]
            messages.extend(user_messages)

            if len(data) < 100:
                break

        except requests.RequestException as e:
            print(f"{red}Erro na requisição: {e}{reset}")
            break

    print(f"{green}Encontradas {len(messages)} mensagens.{reset}")
    return messages

def delete_messages(headers, channel_id, messages):
    url_template = f"https://discord.com/api/v9/channels/{channel_id}/messages/{{}}"
    total = len(messages)

    for i, msg_id in enumerate(messages, 1):
        try:
            response = requests.delete(url_template.format(msg_id), headers=headers, timeout=10)
            if response.status_code != 204:
                print(f"\n{red}Falha ao deletar mensagem {msg_id}. Status: {response.status_code}{reset}")
            percent = (i / total) * 100
            bar = '■' * int(percent // 2) + '.' * (50 - int(percent // 2))
            print(f"\rProgresso: [{green}{bar}{reset}] {percent:.2f}%", end='', flush=True)
            time.sleep(random.uniform(1.0, 1.9))
        except requests.RequestException as e:
            print(f"\n{red}Erro ao tentar deletar: {e}{reset}")

def clear_messages(token, channel_id):
    headers = {
        "Authorization": token,
        "User-Agent": "Mozilla/5.0"
    }
    try:
        user_response = requests.get("https://discord.com/api/v9/users/@me", headers=headers, timeout=10)
        if user_response.status_code != 200:
            print(f"{red}Erro ao obter ID do usuário. Status: {user_response.status_code}{reset}")
            return
        author_id = user_response.json().get("id")
        messages = fetch_messages(headers, channel_id, author_id)

        if messages:
            print(f"{green}Iniciando exclusão...{reset}")
            delete_messages(headers, channel_id, messages)
            print(f"\n{green}Todas as mensagens foram deletadas com sucesso!{reset}")
        else:
            print(f"{red}Nenhuma mensagem encontrada para deletar.{reset}")

    except requests.RequestException as e:
        print(f"{red}Erro na conexão: {e}{reset}")

# Menu principal
async def main():
    clear_cmd()
    print(f"{white}Clear Dm's{reset}")
    token = input("Digite seu token de usuário: ").strip()

    if not token:
        print(f"{red}Token não pode estar vazio.{reset}")
        sys.exit(1)

    while True:
        mostrar_banner_verde_musgo()
        print(f"{white}\n1 - Limpar DMs")
        print("2 - Créditos")
        print("0 - Sair\n")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            channel_id = input("ID do Canal: ").strip()
            if not channel_id:
                print(f"{red}ID do canal não pode estar vazio!{reset}")
                input("Pressione Enter para continuar...")
                continue
            clear_messages(token, channel_id)
            input("\nPressione Enter para continuar...")
        elif opcao == "2":
            await mostrar_creditos()
        elif opcao == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida.")
            time.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
