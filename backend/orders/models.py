from django.db import models
from django.conf import settings

class PaymentMethod(models.Model):
    payment_method_id = models.AutoField(primary_key=True, db_column='payment_method_id', verbose_name='ID способа оплаты')
    payment_method_name = models.CharField(max_length=100, unique=True, db_column='payment_method_name', verbose_name='Название способа оплаты')

    class Meta:
        db_table = 'payment_method'
        verbose_name = 'Способ оплаты'
        verbose_name_plural = 'Способы оплаты'

    def __str__(self):
        return self.payment_method_name

class OrderStatus(models.Model):
    status_id = models.AutoField(primary_key=True, db_column='status_id', verbose_name='ID статуса')
    status_name = models.CharField(max_length=100, unique=True, db_column='status_name', verbose_name='Название статуса')
    status_description = models.TextField(blank=True, null=True, db_column='status_description', verbose_name='Описание статуса')

    class Meta:
        db_table = 'order_status'
        verbose_name = 'Статус заказа'
        verbose_name_plural = 'Статусы заказов'

    def __str__(self):
        return self.status_name

class Order(models.Model):
    order_id = models.AutoField(primary_key=True, db_column='order_id', verbose_name='ID заказа')
    order_date = models.DateTimeField(auto_now_add=True, db_column='order_date', verbose_name='Дата заказа')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, db_column='total_amount', verbose_name='Общая сумма')

    # Связи
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_column='user_user_id', verbose_name='Пользователь')
    order_status = models.ForeignKey(OrderStatus, on_delete=models.SET_NULL, null=True, db_column='order_status_status_id', verbose_name='Статус заказа')
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True, db_column='payment_method_payment_method_id', verbose_name='Способ оплаты')
    delivery_address = models.ForeignKey('users.DeliveryAddress', on_delete=models.SET_NULL, null=True, db_column='delivery_address_address_id', verbose_name='Адрес доставки')

    class Meta:
        db_table = 'order'
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f"Order #{self.order_id} - {self.user.email}"

class OrderItem(models.Model):
    order_item_id = models.AutoField(primary_key=True, db_column='order_item_id', verbose_name='ID позиции заказа')
    product_quantity = models.IntegerField(db_column='product_quantity', verbose_name='Количество товара')
    product_price_at_order = models.DecimalField(max_digits=10, decimal_places=2, db_column='product_price_at_order', verbose_name='Цена товара на момент заказа')

    # Связи
    order = models.ForeignKey(
        Order, 
        on_delete=models.CASCADE, 
        related_name='items',  # ← ВОТ СЮДА ДОБАВЛЯЕТСЯ related_name
        db_column='order_order_id', 
        verbose_name='Заказ'
    )
    product = models.ForeignKey('catalog.Product', on_delete=models.CASCADE, db_column='product_product_id', verbose_name='Товар')

    class Meta:
        db_table = 'order_item'
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказов'

    def __str__(self):
        return f"Item #{self.order_item_id} for Order #{self.order.order_id}"