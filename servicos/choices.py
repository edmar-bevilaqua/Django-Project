from django.db.models import TextChoices

class ChoicesCategory(TextChoices):
    BANHO = "BAN", "Banho"
    TOSA = "TOS", "Tosa"
    ADESTRAMENTO = "ADE", "Adestramento Canino"
    HOSPEDAGEM = "HOS", "Hospedagem"
    VETERINARIO = "VET", "Serviços Veterinários"