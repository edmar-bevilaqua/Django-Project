from django.db.models import TextChoices

# Creating a choices class to keep integrity
class ChoicesCategory(TextChoices):
    BANHO = "BAN", "Banho"
    TOSA = "TOS", "Tosa"
    ADESTRAMENTO = "ADE", "Adestramento Canino"
    HOSPEDAGEM = "HOS", "Hospedagem"
    VETERINARIO = "VET", "Serviços Veterinários"