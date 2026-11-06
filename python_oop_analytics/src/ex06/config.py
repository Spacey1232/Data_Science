import os
telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")
num_of_steps = 3
data_path = "data.csv"
report_template = (
    "В моем эксперименте с подбрасыванием монеты из "
    "{total_observations} наблюдений решка выпала "
    "{count_res} раз, а орёл — {count_orel} раз.\n"
    "Вероятности составляют {fraction_res:.2%} и "
    "{fraction_orel:.2%} соответственно.\n"
    "Я прогнозирую, что в следующих {num_of_steps} наблюдениях "
    "решка выпадет {predicted_res} раз, "
    "а орёл — {predicted_orel} раз."
)