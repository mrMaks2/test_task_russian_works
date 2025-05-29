from django.db import models

class Organization(models.Model):
    inn = models.CharField(max_length=12, unique=True)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    def __str__(self):
        return self.inn

class Payment(models.Model):
    operation_id = models.UUIDField(unique=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    document_number = models.CharField(max_length=255)
    document_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.operation_id)

class BalanceLog(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    old_balance = models.DecimalField(max_digits=15, decimal_places=2)
    new_balance = models.DecimalField(max_digits=15, decimal_places=2)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True)  # Ссылка на платеж

    def __str__(self):
        return f"Balance change for {self.organization.inn} at {self.timestamp}"