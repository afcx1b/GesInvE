from django.contrib import admin
from .models import Catalog, CatalogProduct, Offer, OfferDetail, Order, OrderDetail, Banner

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('idOffer', 'title', 'discount_percentage', 'start_date', 'end_date', 'status', 'is_global')
    search_fields = ('title', 'status')
    list_filter = ('status', 'is_global', 'start_date', 'end_date')

@admin.register(OfferDetail)
class OfferDetailAdmin(admin.ModelAdmin):
    list_display = ('idOfferDetail', 'offer', 'product', 'price_with_discount')
    search_fields = ('offer__title', 'product__product')
    list_filter = ('offer', 'product')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('idOrder', 'customer', 'order_type', 'status', 'order_date')
    search_fields = ('customer__username', 'status')
    list_filter = ('order_type', 'status', 'order_date')

@admin.register(OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ('idDetail', 'order', 'product', 'quantity', 'price')
    search_fields = ('order__idOrder', 'product__product')
    list_filter = ('order', 'product')

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('idBanner', 'title', 'start_date', 'end_date', 'is_active', 'position', 'layout')
    search_fields = ('title', 'position', 'layout')
    list_filter = ('is_active', 'position', 'layout', 'start_date', 'end_date')


@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):
    list_display = ('title', 'image')
    search_fields = ('title',)
    list_filter = ('title', 'created_at')

@admin.register(CatalogProduct)
class CatalogProductAdmin(admin.ModelAdmin):
    list_display = ('catalog', 'product')
    search_fields = ('catalog__title', 'product__name')
    list_filter = ('catalog', 'product')