from abc import ABC, abstractmethod

from libs.python_library.data.data_transfer_object import DataTransferObject


class DataTransfer(ABC):
    def __init__(self, data: dict) -> None:
        self.data = data

    @abstractmethod
    def required_fields(self) -> list:
        return []

    def get(self) -> DataTransferObject:
        dto = DataTransferObject()
        for key in self.required_fields():
            # print(f'~~key[{key}]')
            if not key in self.data:
                raise Exception(f'invalid key: {key}')
            setattr(dto, key, self.data[key])
        return dto
