from src.data_transfers.data_transfer import DataTransfer


class LoginData(DataTransfer):
    def required_fields(self) -> list:
        return ['username', 'password']
