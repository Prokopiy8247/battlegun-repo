from django.contrib import admin
from .models import Category, Product, ProductImage, ProductSpecification

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'is_active', 'sort_order']
    list_filter = ['is_active', 'parent']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'sku', 'price', 'brand', 'stock', 'is_active', 'category']
    list_filter = ['is_active', 'category', 'brand', 'created_at']
    search_fields = ['name', 'sku', 'brand']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline, ProductSpecificationInline]
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'sku', 'category', 'price', 'discount_price', 'stock', 'is_active')
        }),
        ('Description', {
            'fields': ('description_short', 'description')
        }),
        ('Airsoft Details', {
            'fields': ('brand', 'color', 'weight_g', 'power_supply', 'material', 'muzzle_velocity_fps')
        }),
    )
