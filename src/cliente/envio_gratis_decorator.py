from .cliente_decorator import ClienteDecorator

class EnvioGratisDecorator(ClienteDecorator):
    def tiene_envio_gratis(self):
        return True
