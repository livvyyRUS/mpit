Для запуска нужно:
1) Запустить сервер ngrok на порте 2222 через http (Ngrok может не всегда работать в России)
2) Запустить файл backend.py командой
```commandline
fastapi run backend.py --host localhost --port 12345
```
3) Запустить бота bot.py
4) Запустить main.py