from django.conf import settings
from django.db import models


class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True, db_column='cart_id', verbose_name='ID корзины')
    creation_date = models.DateTimeField(auto_now_add=True, db_column='creation_date', verbose_name='Дата создания')
    update_date = models.DateTimeField(auto_now=True, db_column='update_date', verbose_name='Дата обновления')
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column='user_user_id',
        verbose_name='Пользователь',
    )

    class Meta:
        db_table = 'cart'
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    @property
    def total_price(self):
        return sum(item.subtotal for item in self.items.select_related('product'))

    def __str__(self):
        return f'Корзина #{self.cart_id} пользователя {self.user.email}'


class CartItem(models.Model):
    cart_item_id = models.AutoField(primary_key=True, db_column='cart_item_id', verbose_name='ID позиции корзины')
    product_quantity = models.PositiveIntegerField(default=1, db_column='product_quantity', verbose_name='Количество товара')
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        db_column='cart_cart_id',
        verbose_name='Корзина',
    )
    product = models.ForeignKey(
        'catalog.Product',
        on_delete=models.CASCADE,
        db_column='product_product_id',
        verbose_name='Товар',
    )

    class Meta:
        db_table = 'cart_item'
        unique_together = (('cart', 'product'),)
        verbose_name = 'Позиция корзины'
        verbose_name_plural = 'Позиции корзины'

    @property
    def subtotal(self):
        return self.product.price * self.product_quantity

    def __str__(self):
        return f'{self.product_quantity} x {self.product.product_name}'
