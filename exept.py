import models


class FacebookException(Exception):
    def __init__(self, message, network_id):
        Exception.__init__(self, message)

        self.network = models.NetWork.objects.get(network_id=network_id, network=models.NetWork.FACEBOOK)