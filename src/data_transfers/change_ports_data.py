from src.data_transfers.data_transfer import DataTransfer


class ChangePortsData(DataTransfer):
    def required_fields(self) -> list:
        return [
            'token', 
            'interface_port', 
            'peer_port'
        ]
