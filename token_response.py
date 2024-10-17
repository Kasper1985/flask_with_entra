class TokenResponse:
    def __init__(self, token_type, scope, expires_in, ext_expires_in, access_token, id_token):
        self.token_type = token_type
        self.scope = scope
        self.expires_in = expires_in
        self.ext_expires_in = ext_expires_in
        self.access_token = access_token
        self.id_token = id_token
    
    def __str__(self):
        return "\n".join(key + ": " + str(value) for key, value in self.__dict__.items())

    @staticmethod
    def from_dict(obj: any) -> 'TokenResponse':
        assert isinstance(obj, dict)
        token_type = obj.get("token_type")
        scope = obj.get("scope")
        expires_in = obj.get("expires_in")
        ext_expires_in = obj.get("ext_expires_in")
        access_token = obj.get("access_token")
        id_token = obj.get("id_token")
        return TokenResponse(token_type, scope, expires_in, ext_expires_in, access_token, id_token)