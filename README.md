# yakuniy-2
yakuniy-2

Bu Telegram bot foydalanuvchilarga vazifalarni boshqarish imkonini beradi. Bot foydalanuvchilar o'z vazifalarini yaratish, yangilash va o'chirishlari mumkin. Adminlar esa foydalanuvchilarni bloklash va barcha vazifalarni ko'rish imkoniyatiga ega.

## Xususiyatlar

- **Foydalanuvchilar uchun:**
  - Yangi vazifalar yaratish
  - O'z vazifalarini ko'rish
  - Vazifalarni yangilash va o'chirish

- **Adminlar uchun:**
  - Foydalanuvchilarni bloklash va blokdan chiqarish
  - Barcha vazifalarni ko'rish

## Talablar

- Python 3.6 yoki undan yuqori
- `telebot` kutubxonasi
- `psycopg2` kutubxonasi
- PostgreSQL ma'lumotlar bazasi

## O'rnatish

1. **Loyihani klonlash:**

   ```bash
   git clone https://github.com/username/repo-name.git
   cd repo-name
Barchasini ko'rsatish
Talab qilingan kutubxonalarni o'rnating:

pip install pyTelegramBotAPI psycopg2
Ma'lumotlar bazasini tayyorlash:
PostgreSQL ma'lumotlar bazasini yarating va db_name, db_user, db_password parametrlarini o'zgartiring.

Bot tokenini o'zgartirish:
Kodda YOUR_TELEGRAM_BOT_TOKEN joyini o'zingizning Telegram bot tokeningiz bilan to'ldiring.

Ishga tushirish
Botni ishga tushirish uchun:

python bot.py
Foydalanish
Bot ishga tushgandan so'ng, Telegramda botga yozing va quyidagi buyruqlardan foydalaning:

/start - Botni ishga tushirish
/help - Buyruqlar ro'yxatini ko'rish
/mytasks - Mening vazifalarim
/newtask - Yangi vazifa yaratish
/updatetask - Vazifani yangilash
/deletetask - Vazifani o'chirish
/admin_login - Administrator sifatida kirish
/alltasks - Barcha vazifalarni ko'rish (admin)
/ban - Foydalanuvchini bloklash (admin)
/unban - Foydalanuvchini blokdan chiqarish (admin)
Litsenziya
Bu loyiha MIT Litsenziyasi bilan litsenziyalangan.

Aloqa
Agar sizda savollar yoki takliflar bo'lsa, GitHub Issues orqali murojaat qiling.


### O'zgartirishlar

- `username/repo-name` joylarini o'zingizning GitHub foydalanuvchi nomingiz va repozitoriya nomingiz bilan almashtiring.
- Litsenziya bo'limini o'zingizning loyihangizga mos ravishda o'zgartiring.
- Qo'shimcha bo'limlar yoki ma'lumotlarni qo'shishingiz mumkin.

Agar qo'shimcha savollar bo'lsa yoki yordam kerak bo'lsa, so'rang!
