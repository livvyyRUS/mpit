Для запуска нужно:

1) Запустить сервер ngrok на порте 2222 через http (Ngrok может не всегда работать в России)
2) Получить url адрес от ngrok, вставить в переменную url в файле bot.py
3) Запустить файл backend.py командой

```commandline
fastapi run backend.py --host localhost --port 12345
```

4) Запустить бота bot.py
5) Запустить main.py