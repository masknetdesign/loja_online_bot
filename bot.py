from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext
import logging

# Configuração do logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Token do bot
TOKEN = '7389961581:AAF56SL-2yL2h721l6BHCaLzavjF_B8ZNjw'

# Lista de produtos
products = [
    {'id': 'prod1', 'name': 'Produto 1', 'price': 10.00},
    {'id': 'prod2', 'name': 'Produto 2', 'price': 20.00},
    {'id': 'prod3', 'name': 'Produto 3', 'price': 30.00},
]

# Dicionário para armazenar o carrinho de compras dos usuários
user_cart = {}

# Comando /start
async def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Ver Produtos", callback_data='view_products')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Bem-vindo à nossa loja online! Selecione uma opção:', reply_markup=reply_markup)

# Função para exibir os produtos
async def view_products(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    keyboard = [[InlineKeyboardButton(product['name'], callback_data=f'add_{product["id"]}') for product in products]]
    keyboard.append([InlineKeyboardButton("Ver Carrinho", callback_data='view_cart')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text="Selecione um produto para adicionar ao carrinho:", reply_markup=reply_markup)

# Função para adicionar produto ao carrinho
async def add_to_cart(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    user_id = query.from_user.id
    product_id = query.data.split('_')[1]
    product = next((p for p in products if p['id'] == product_id), None)

    if user_id not in user_cart:
        user_cart[user_id] = []

    if product:
        user_cart[user_id].append(product)
        await query.answer(f'{product["name"]} adicionado ao carrinho!')

    await view_products(update, context)

# Função para exibir o carrinho
async def view_cart(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    user_id = query.from_user.id
    cart = user_cart.get(user_id, [])

    if not cart:
        await query.edit_message_text(text="Seu carrinho está vazio.")
        return

    cart_items = "\n".join([f"{item['name']} - R$ {item['price']:.2f}" for item in cart])
    total = sum(item['price'] for item in cart)
    text = f"Seu carrinho:\n\n{cart_items}\n\nTotal: R$ {total:.2f}"

    keyboard = [[InlineKeyboardButton("Continuar Comprando", callback_data='view_products')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=text, reply_markup=reply_markup)

# Configuração dos handlers
def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(view_products, pattern='view_products'))
    application.add_handler(CallbackQueryHandler(add_to_cart, pattern='add_'))
    application.add_handler(CallbackQueryHandler(view_cart, pattern='view_cart'))

    application.run_polling()

if __name__ == '__main__':
    main()
