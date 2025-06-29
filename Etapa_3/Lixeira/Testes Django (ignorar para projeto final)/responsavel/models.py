from django.db import models

class Responsavel(models.Model):
    cpf = models.CharField(max_length=11, primary_key=True)  # Apenas números, ex: 12345678900
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=11)  # Apenas números, ex: 11987654321
    setor = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nome} - {self.cpf}"

    # Getters
    def getCPF(self):
        return self.cpf

    def getNome(self):
        return self.nome

    def getTelefone(self):
        return self.telefone

    def getSetor(self):
        return self.setor

    # Setters
    def setNome(self, novoNome):
        self.nome = novoNome

    def setTelefone(self, novoTelefone):
        self.telefone = novoTelefone

    def setSetor(self, novoSetor):
        self.setor = novoSetor
