import requests
from bs4 import BeautifulSoup
from plyer import notification
import hashlib
import os
from datetime import datetime
# CÓDIGO INSERIDO
import smtplib
import ssl
from email.message import EmailMessage
# FIM DO CÓDIGO INSERIDO
# CÓDIGO INSERIDO
from dotenv import load_dotenv

ARQUIVO_ESTADO = 'estado_ansa.txt'
# FIM DO CÓDIGO INSERIDO

# Carrega as variáveis do arquivo .env
load_dotenv()
# FIM DO CÓDIGO INSERIDO


def verificar_atualizacao():
    # URL da página do concurso (substitua pela URL real do Cebraspe/ANSA)
    url = "https://www.cebraspe.org.br/concursos/ansa_26"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    hora_atual = datetime.now().strftime('%H:%M:%S')
    print(f"[{hora_atual}] Iniciando verificação no site do Cebraspe (ANSA)...")

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # CÓDIGO EXCLUÍDO
        # area_editais = soup.find('ul', class_='page-concursos__cargos-list')
        # FIM DO CÓDIGO EXCLUÍDO

        # CÓDIGO INSERIDO
        texto_pagina = soup.get_text(strip=True)
        hash_atual = hashlib.md5(texto_pagina.encode('utf-8')).hexdigest()
        # FIM DO CÓDIGO INSERIDO

        if os.path.exists(ARQUIVO_ESTADO):
            with open(ARQUIVO_ESTADO, 'r') as f:
                hash_anterior = f.read().strip()

            if hash_atual != hash_anterior:
                print(f"[{hora_atual}] ⚠️ ALTERAÇÃO DETECTADA! O site foi modificado.")

                # CÓDIGO EXCLUÍDO
                # enviar_notificacao("Atualização ANSA!", "A seção de editais sofreu alteração. Verifique o site.")
                # FIM DO CÓDIGO EXCLUÍDO

                # CÓDIGO INSERIDO
                enviar_notificacao("Atualização ANSA!",
                                   "Qualquer tipo de alteração foi detectada na página. Verifique o site.")
                # FIM DO CÓDIGO INSERIDO

                with open(ARQUIVO_ESTADO, 'w') as f:
                    f.write(hash_atual)
            else:
                # CÓDIGO EXCLUÍDO
                # print(f"[{hora_atual}] ✅ Nenhuma alteração na seção de editais.")
                # FIM DO CÓDIGO EXCLUÍDO

                # CÓDIGO INSERIDO
                print(f"[{hora_atual}] ✅ Nenhuma alteração detectada no site.")
                # FIM DO CÓDIGO INSERIDO
        else:
            # CÓDIGO EXCLUÍDO
            # print(f"[{hora_atual}] 📌 Primeira execução. Salvando o estado atual da seção de editais...")
            # FIM DO CÓDIGO EXCLUÍDO

            # CÓDIGO INSERIDO
            print(f"[{hora_atual}] 📌 Primeira execução. Salvando o estado global do site para futuras comparações...")
            # FIM DO CÓDIGO INSERIDO

            with open(ARQUIVO_ESTADO, 'w') as f:
                f.write(hash_atual)

        # CÓDIGO EXCLUÍDO
        # else:
        #     print(f"[{hora_atual}] ❌ Erro: Não foi possível localizar a lista da seção 'Editais, comunicados e informações'.")
        # FIM DO CÓDIGO EXCLUÍDO

    except Exception as e:
        print(f"[{hora_atual}] ❌ Erro ao acessar a página: {e}")


# CÓDIGO MODIFICADO
def enviar_notificacao(titulo, mensagem):
    # CÓDIGO EXCLUÍDO
    # try:
    #     notification.notify(
    #         title=titulo,
    #         message=mensagem,
    #         app_name="Monitor Cebraspe",
    #         timeout=10
    #     )
    #     print("🔔 Notificação nativa enviada com sucesso no Windows.")
    # except Exception as e:
    #     print(f"❌ Erro ao tentar disparar a notificação do Windows: {e}")
    # FIM DO CÓDIGO EXCLUÍDO

    # CÓDIGO INSERIDO
    email_remetente = os.getenv('GMAIL_USER')
    senha_app = os.getenv('GMAIL_PASS')
    email_destinatario = os.getenv('GMAIL_TO')

    if not email_remetente or not senha_app or not email_destinatario:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Erro: Credenciais de e-mail não encontradas no arquivo .env")
        return
    # FIM DO CÓDIGO INSERIDO

    msg = EmailMessage()
    msg['Subject'] = titulo
    msg['From'] = email_remetente
    msg['To'] = email_destinatario
    msg.set_content(mensagem)

    context = ssl.create_default_context()

    try:
        # Estabelece conexão segura com o servidor SMTP do Gmail na porta 465
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_remetente, senha_app)
            smtp.send_message(msg)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 📧 E-mail de notificação enviado com sucesso para {email_destinatario}.")
    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Erro ao tentar enviar o e-mail: {e}")
    # FIM DO CÓDIGO INSERIDO

if __name__ == "__main__":
    verificar_atualizacao()