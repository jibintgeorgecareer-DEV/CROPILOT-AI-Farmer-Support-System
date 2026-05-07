from django.db import models
from django.contrib.auth.models import User

# =====================================================
# ROLE & AUTHENTICATION
# =====================================================
class Profile(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('farmer', 'Farmer'),
        ('officer', 'Officer'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} ({self.role})"


# =====================================================
# FARMER MODULE
# =====================================================
class Farmer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) #ref id to User (id)
    phone = models.CharField(max_length=15)
    region = models.CharField(max_length=100)
    address = models.TextField(blank=True)
    profile = models.ImageField(upload_to='farmer_pic',default='farmer_pic/default.jpg')

    def __str__(self):
        return self.user.username


# =====================================================
# AGRICULTURE OFFICER MODULE
# =====================================================
class AgricultureOfficer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    region = models.CharField(max_length=100)
    qualification = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username

#ChatBot ==============================
class ChatBot(models.Model):
    question = models.TextField()
    answers = models.TextField()

    def __str__(self):
        return self.question 




# =====================================================
# ADMIN MODULE – CROPS & SOIL
# =====================================================
class Crop(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="crop",null=True ,blank=True)
    suitable_soil = models.CharField(max_length=100,null=True ,blank=True)
    season = models.CharField(max_length=50,null=True ,blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.name


class Soil(models.Model):
    soil_type = models.CharField(max_length=100)
    nitrogen = models.FloatField()
    phosphorus = models.FloatField()
    potassium = models.FloatField()

    def __str__(self):
        return self.soil_type


# =====================================================
# AI MODULE – DISEASE DETECTION
# =====================================================
class DiseaseReport(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    crop_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='leaves/')
    detected_disease = models.CharField(max_length=100)
    confidence = models.FloatField(null=True, blank=True)   
    treatment = models.TextField(blank=True)
    verified_by_officer = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.crop_name} - {self.detected_disease}"


# =====================================================
# FARMER ↔ OFFICER COMMUNICATION
# =====================================================
class FarmerQuery(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    question = models.TextField()
    reply = models.TextField(blank=True)
    replied = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question
    
class FertilizerRecommendation(models.Model):
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    fertilizer = models.CharField(max_length=100)
    dosage = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f"{self.crop.name} - {self.fertilizer}"


class SoilRecommendation(models.Model):
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    soil_type = models.CharField(max_length=100)
    description_en = models.TextField()
    description_ml = models.TextField()   # Malayalam description

    def __str__(self):
        return f"{self.crop.name} - {self.soil_type}"


# =====================================================
# MARKET PRICE (AI / ADMIN)
# =====================================================
class MarketPrice(models.Model):
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    price = models.FloatField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.crop.name} - ₹{self.price}"


# =====================================================
# FEEDBACK
# =====================================================
class Feedback(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.farmer.user.username}"
