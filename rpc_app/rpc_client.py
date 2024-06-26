import os
import json
import ssl
import urllib.request
import urllib.error
import tempfile
from django.conf import settings


class JRPCController:
    """
    Класс для выполнения JSON-RPC вызовов с использованием двустороннего TLS.
    Атрибуты:
        api_url (str): URL JSON-RPC API.
        api_cert (str): Содержимое клиентского сертификата.
        api_key (str): Содержимое клиентского ключа.
    """

    def __init__(self):
        """
        Инициализация JRPCController, загрузка URL API и содержимого сертификата и ключа из настроек.
        """
        self.api_url = settings.JSON_RPC_API_URL
        self.api_cert = settings.CLIENT_CERTIFICATE
        self.api_key = settings.CLIENT_KEY

    def create_connector(self):
        """
        Создание SSL контекста с клиентским сертификатом и ключом.
        Возвращает:
            ssl.SSLContext: Настроенный SSL контекст.
        """

        # Создание временных файлов для сертификата и ключа
        certfile = tempfile.NamedTemporaryFile(delete=False)
        certfile.write(self.api_cert.encode("utf-8"))
        certfile.close()
        keyfile = tempfile.NamedTemporaryFile(delete=False)
        keyfile.write(self.api_key.encode("utf-8"))
        keyfile.close()

        # Создание SSL контекста с использованием временных файлов
        ssl_ctx = ssl.create_default_context()
        ssl_ctx.load_cert_chain(certfile.name, keyfile.name)

        # Удаление временных файлов
        os.remove(certfile.name)
        os.remove(keyfile.name)

        return ssl_ctx

    def post_jrpc(self, payload):
        """
        Отправка JSON-RPC запроса на сервер.
        Args:
            payload (dict): Словарь с данными запроса JSON-RPC.
        Returns:
            dict: Ответ от JSON-RPC сервера. В случае ошибки возвращает словарь с ключом 'error'.
        """

        ssl_context = self.create_connector()
        request_data = json.dumps(payload).encode('utf-8')

        request = urllib.request.Request(self.api_url, data=request_data, headers={'Content-Type': 'application/json'})

        try:
            with urllib.request.urlopen(request, context=ssl_context) as response:
                response_data = response.read().decode('utf-8')
                return json.loads(response_data)
        except urllib.error.HTTPError as e:
            return {'error': str(e)}
        except urllib.error.URLError as e:
            return {'error': str(e)}

    def test(self):
        """
        Тестовый метод для вызова метода auth.check на JSON-RPC сервере.
        Returns:
            dict: Ответ от JSON-RPC сервера на метод auth.check. В случае ошибки возвращает словарь с ключом 'error'.
        """

        payload = {
            "method": "auth.check",
            "params": [],
            "jsonrpc": "2.0",
            "id": 0,
        }
        return self.post_jrpc(payload)
