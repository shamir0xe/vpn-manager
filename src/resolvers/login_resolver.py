from typing import Tuple, Union
from src.actions.server.authentication import Authentication
from src.resolvers.resolver import Resolver
from src.data_transfers.login_data import LoginData


class LoginResolver(Resolver):
    def resolve(self) -> Tuple[bool, Union[dict, str]]:
        data = LoginData(self.request.json).get()
        if Authentication.with_username(data.username, data.password):
            token = Authentication.create_token()
            return (True, {
                'token': token
            },)
        else:
            return (False,'wrong credentials')
