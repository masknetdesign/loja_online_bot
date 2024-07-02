from flask import Flask, render_template
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext
import logging

app = Flask(__name__)

# Configurações do bot
TOKEN = '7182537179:AAH41bIU2a7oR6cXnPxdYPhYto4fK5rqCl8'

# Configuração do logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Função principal do Flask para servir a página web
@app.route('/')
def index():
    return render_template('index.html')

# Comando /start do bot
async def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Abrir Loja Online", url='http://127.0.0.1:5000/')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Bem-vindo à nossa loja online! Clique abaixo para acessar:', reply_markup=reply_markup)

async def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))

    # Inicie o bot
    await application.start()
    # Execute o bot até que o processo receba um sinal para parar
    await application.updater.wait_for_shutdown()

if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    app.run(port=5000)
