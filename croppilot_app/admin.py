from django.contrib import admin
from .models import (
    Profile,
    Farmer,
    AgricultureOfficer,
    Crop,
    Soil,
    DiseaseReport,
    FarmerQuery,
    MarketPrice,
    Feedback
)
from .models import SoilRecommendation, FertilizerRecommendation

@admin.register(SoilRecommendation)
class SoilRecommendationAdmin(admin.ModelAdmin):
    list_display = ('crop', 'soil_type')


@admin.register(FertilizerRecommendation)
class FertilizerRecommendationAdmin(admin.ModelAdmin):
    list_display = ('crop', 'fertilizer')

# ===============================
# AUTH / ROLE
# ===============================
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role',)


# ===============================
# FARMER
# ===============================
@admin.register(Farmer)
class FarmerAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'region')
    search_fields = ('user__username', 'region')


# ===============================
# AGRICULTURE OFFICER
# ===============================
@admin.register(AgricultureOfficer)
class OfficerAdmin(admin.ModelAdmin):
    list_display = ('user', 'region', 'qualification')
    search_fields = ('user__username', 'region')


# ===============================
# CROP & SOIL
# ===============================
@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ('name', 'suitable_soil', 'season')
    search_fields = ('name',)


@admin.register(Soil)
class SoilAdmin(admin.ModelAdmin):
    list_display = ('soil_type', 'nitrogen', 'phosphorus', 'potassium')


# ===============================
# AI – DISEASE REPORT
# ===============================
@admin.register(DiseaseReport)
class DiseaseReportAdmin(admin.ModelAdmin):
    list_display = (
        'crop_name',
        'detected_disease',
        'farmer',
        'verified_by_officer',
        'created_at'
    )
    list_filter = ('verified_by_officer', 'detected_disease')
    search_fields = ('crop_name', 'detected_disease')


# ===============================
# FARMER ↔ OFFICER QUERY
# ===============================
@admin.register(FarmerQuery)
class FarmerQueryAdmin(admin.ModelAdmin):
    list_display = ('farmer', 'question', 'replied', 'created_at')


# ===============================
# MARKET PRICE
# ===============================
@admin.register(MarketPrice)
class MarketPriceAdmin(admin.ModelAdmin):
    list_display = ('crop', 'price', 'date')
    list_filter = ('date',)


# ===============================
# FEEDBACK
# ===============================
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('farmer', 'created_at')
