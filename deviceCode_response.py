class DeviceCodeResponse:
    def __init__(self, user_code: str, device_code: str, verification_uri: str, expires_in: int, interval: int, message: str):
        self.user_code = user_code
        self.device_code = device_code
        self.verification_uri = verification_uri
        self.expires_in = expires_in
        self.interval = interval
        self.message = message

    def __str__(self):
        return "\n".join(key + ": " + str(value) for key, value in self.__dict__.items())

    @staticmethod
    def from_dict(obj: any) -> 'DeviceCodeResponse':
        assert isinstance(obj, dict)
        user_code = obj.get("user_code")
        device_code = obj.get("device_code")
        verification_uri = obj.get("verification_uri")
        expires_in = obj.get("expires_in")
        interval = obj.get("interval")
        message = obj.get("message")
        return DeviceCodeResponse(user_code, device_code, verification_uri, expires_in, interval, message)
    