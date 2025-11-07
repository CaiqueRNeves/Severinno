"""Modelos responsáveis por salas e máquinas cadastradas no campus."""

from django.db import models


class Room(models.Model):
    """Representa uma sala ou laboratório físico."""

    name = models.CharField("nome da sala", max_length=120, unique=True)
    code = models.CharField("código interno", max_length=20, unique=True)
    location = models.CharField("localização", max_length=255)
    capacity = models.PositiveIntegerField("capacidade", default=0)
    description = models.TextField("observações", blank=True)
    is_active = models.BooleanField("ativa", default=True)
    created_at = models.DateTimeField("criada em", auto_now_add=True)
    updated_at = models.DateTimeField("atualizada em", auto_now=True)

    class Meta:
        verbose_name = "Sala"
        verbose_name_plural = "Salas"
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.code} - {self.name}"


class Machine(models.Model):
    """Cadastra máquinas associadas às salas, com especificações técnicas."""

    class MemoryType(models.TextChoices):
        DDR3 = "DDR3", "DDR3"
        DDR4 = "DDR4", "DDR4"
        DDR5 = "DDR5", "DDR5"
        LPDDR4 = "LPDDR4", "LPDDR4"
        OUTRO = "OUTRO", "Outro"

    room = models.ForeignKey(
        Room,
        related_name="machines",
        on_delete=models.CASCADE,
        verbose_name="sala",
    )
    hostname = models.CharField("identificador/hostname", max_length=60, blank=True)
    processador = models.CharField("processador", max_length=120)
    memoria = models.PositiveIntegerField("memória (GB)")
    tipo_memoria = models.CharField(
        "tipo da memória",
        max_length=20,
        choices=MemoryType.choices,
        default=MemoryType.DDR4,
    )
    armazenamento = models.CharField("armazenamento", max_length=120)
    placa_mae = models.CharField("placa mãe", max_length=120)
    numero_serie = models.CharField("número de série", max_length=100, unique=True)
    observacoes = models.TextField("observações", blank=True)
    is_available = models.BooleanField("disponível", default=True)
    created_at = models.DateTimeField("criada em", auto_now_add=True)
    updated_at = models.DateTimeField("atualizada em", auto_now=True)

    class Meta:
        verbose_name = "Máquina"
        verbose_name_plural = "Máquinas"
        ordering = ["room", "hostname", "numero_serie"]

    def __str__(self) -> str:
        return f"{self.hostname or self.numero_serie} ({self.room.code})"
