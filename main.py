import sys
import signal
from mcstatus import JavaServer
import plyer
from time import sleep


def check_server_status(address, port=25565):
    try:
        server = JavaServer.lookup(f"{address}:{port}")
        status = server.status()
        return {
            "online": True,
            "version": status.version.name,
            "motd": status.description,
            "players_online": status.players.online,
            "max_players": status.players.max,
            "ping": server.ping()
        }
    except Exception as e:
        return {
            "online": False,
            "error": str(e)
        }


def notify_players_change(previous_players, current_players):
    if previous_players != current_players:
        plyer.notification.notify(title='Изменение онлайна',
                                  message=f'Количество игроков изменилось с {previous_players} на {current_players}',
                                  app_name='Status', timeout=100)


def safe_exit(signal, frame):
    print("\nВыход из программы.")
    sys.exit(0)


# Обработка сигнала Ctrl+C для безопасного выхода
signal.signal(signal.SIGINT, safe_exit)

server_address = "IP"
server_port = 25565  # Порт по умолчанию для Minecraft

server_status = check_server_status(server_address, server_port)

if server_status["online"]:
    print(f"Версия: {server_status['version']}")
    print(f"Описание: {server_status['motd']}")
    print(f"Игроков онлайн: {server_status['players_online']}/{server_status['max_players']}")
else:
    print(f"Сервер не отвечает: {server_status['error']}")

previous_players = server_status['players_online']

try:
    while True:
        sleep(1)
        server_status = check_server_status(server_address, server_port)
        print(f"- {server_status['players_online']} {server_status['ping']}")

        notify_players_change(previous_players, server_status['players_online'])
        previous_players = server_status['players_online']
except KeyboardInterrupt:
    print("Выход из программы. Нажмите Enter для завершения.")
    input()
