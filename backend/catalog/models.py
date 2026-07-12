from django.db import models

class ProductCategory(models.Model):
    category_id = models.AutoField(primary_key=True, db_column='category_id', verbose_name='ID категории')
    category_name = models.CharField(max_length=150, unique=True, db_column='category_name', verbose_name='Название категории')
    category_description = models.TextField(blank=True, null=True, db_column='category_description', verbose_name='Описание категории')

    class Meta:
        db_table = 'product_category'
        verbose_name = 'Категория товара'
        verbose_name_plural = 'Категории товаров'

    def __str__(self):
        return self.category_name

class Brand(models.Model):
    brand_id = models.AutoField(primary_key=True, db_column='brand_id', verbose_name='ID бренда')
    brand_name = models.CharField(max_length=150, unique=True, db_column='brand_name', verbose_name='Название бренда')
    brand_country = models.CharField(max_length=100, blank=True, null=True, db_column='brand_country', verbose_name='Страна бренда')
    brand_description = models.TextField(blank=True, null=True, db_column='brand_description', verbose_name='Описание бренда')

    class Meta:
        db_table = 'brand'
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'

    def __str__(self):
        return self.brand_name

class Product(models.Model):
    product_id = models.AutoField(primary_key=True, db_column='product_id', verbose_name='ID товара')
    product_name = models.CharField(max_length=200, db_column='product_name', verbose_name='Название товара')
    product_description = models.TextField(blank=True, null=True, db_column='product_description', verbose_name='Описание товара')
    purpose = models.CharField(max_length=200, blank=True, null=True, db_column='purpose', verbose_name='Назначение')
    price = models.DecimalField(max_digits=10, decimal_places=2, db_column='price', verbose_name='Цена')
    stock_quantity = models.IntegerField(db_column='stock_quantity', verbose_name='Количество на складе')
    product_image = models.URLField( # хранятся ссылки на изображения, а не сами изображения
        max_length=500,
        blank=True, 
        null=True, 
        db_column='product_image',
        verbose_name='Изображение товара'
    )

    # Связи
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, db_column='brand_brand_id', verbose_name='Бренд')
    product_category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, db_column='product_category_category_id', verbose_name='Категория товара')

    class Meta:
        db_table = 'product'
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.product_name