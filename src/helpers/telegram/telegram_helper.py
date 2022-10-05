from libs.python_library.config.config import Config
from libs.python_library.data.data_transfer_object import DataTransferObject
from src.mediators.request_mediator import RequestMediator


class TelegramHelper:
    @staticmethod
    def send_message(message: str, section: str) -> DataTransferObject:
        res = RequestMediator() \
            .set_url(Config.read('env.telegram.url')) \
            .set_payload({
                'chat_id': Config.read('env.telegram.channel_id'),
                'text': f'[ wireguard-{section} ]: {message}',
                'parse_mode': 'HTML'
            }) \
            .post() \
            .response()
        return res
    