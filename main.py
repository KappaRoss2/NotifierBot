from aiogram.utils import executor
from handlers.intro import process_start_command
from handlers.serials import process_add_serial_command
from handlers.general import process_info_command
from loader import dp


# Скрипт для запуска бота
if __name__ == '__main__':
    executor.start_polling(dp)