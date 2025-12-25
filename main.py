import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Thay TOKEN của bạn vào đây
TOKEN = "8319117639:AAGBsQqvJv_pCNk6inUSM7MvH5MGxtgDBXE"

# Thiết lập logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Chào bạn! Hãy gửi cho mình Username TikTok để kiểm tra thông tin nhé.")

async def check_tiktok(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.text.strip().replace("@", "")
    await update.message.reply_text(f"🔍 Đang kiểm tra tài khoản: @{username}...")

    # Sử dụng API miễn phí (Lưu ý: API này có thể thay đổi theo thời gian)
    url = f"https://www.tiktok.com/@{username}"
    
    # Ở đây chúng ta sử dụng một API giả lập để lấy stats nhanh
    # Nếu muốn chuyên nghiệp hơn, bạn nên dùng RapidAPI
    api_url = f"https://countik.com/api/userinfo/{username}"
    
    try:
        response = requests.get(api_url)
        data = response.json()

        if data.get("status") == "success":
            name = data['nickname']
            followers = data['followerCount']
            following = data['followingCount']
            hearts = data['heartCount']
            videos = data['videoCount']
            bio = data['signature'] if data['signature'] else "Không có"

            msg = (
                f"👤 **Tên:** {name}\n"
                f"🆔 **Username:** @{username}\n"
                f"📝 **Tiểu sử:** {bio}\n"
                f"--- Thống kê ---\n"
                f"✅ **Followers:** {followers:,}\n"
                f"👥 **Đang Follow:** {following:,}\n"
                f"❤️ **Tổng lượt thích:** {hearts:,}\n"
                f"🎥 **Số video:** {videos:,}"
            )
            await update.message.reply_text(msg, parse_mode="Markdown")
        else:
            await update.message.reply_text("❌ Không tìm thấy người dùng này hoặc tài khoản bị khóa.")
    except Exception as e:
        await update.message.reply_text("⚠️ Có lỗi xảy ra khi lấy dữ liệu. Vui lòng thử lại sau.")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_tiktok))
    
    print("Bot đang chạy...")
    app.run_polling()

if __name__ == '__main__':
    main()
