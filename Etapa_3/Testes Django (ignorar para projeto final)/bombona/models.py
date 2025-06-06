from django.db import models
from responsavel.models import Responsavel

class Bombona(models.Model):
    codigo = models.CharField(max_length=5, primary_key=True) # Um exemplo de código pode ser D1423
    volume = models.FloatField()
    tipo_residuo = models.CharField(max_length=100)
    responsavel = models.ForeignKey(
        Responsavel,
        on_delete=models.PROTECT,
        related_name='bombonas'
    )

    def __str__(self):
        return f"{self.codigo} - {self.tipo_residuo}"

    # Getters
    def getCodigo(self):
        return self.codigo

    def getVolume(self):
        return self.volume

    def getTipoResiduo(self):
        return self.tipo_residuo

    def getResponsavel(self):
        return self.responsavel

    # Setters
    def setVolume(self, novoVol):
        self.volume = novoVol

    def setTipoResiduo(self, novoTipo):
        self.tipo_residuo = novoTipo

    def setResponsavel(self, novoResp):
        self.responsavel = novoResp
