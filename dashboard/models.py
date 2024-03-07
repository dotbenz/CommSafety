from django.db import models
from django.contrib.auth.models import User

class AnonymousReport(models.Model):
    CRIME_CHOICES = [
        ('SELECT_CRIME', 'Select a crime'),  # Placeholder option
        ('THEFT', 'Theft'),
        ('MURDER', 'Murder'),
        ('KIDNAPPING', 'Kidnapping'),
        ('CYBERCRIME', 'Cybercrime'),
        ('BURGLARY', 'Burglary'),
        ('TRAFFICKING', 'Trafficking'),
        ('BANDITRY', 'Banditry'),
        ('MANSLAUGHTER', 'Manslaughter'),
        ('RAPE', 'Rape'),
        ('ROBBERY', 'Robbery'),
        ('EXAM_MALPRACTICE', 'Exam Malpractice'),
        ('ASSAULT', 'Assault'),
        ('FRAUD', 'Fraud'),
        ('VANDALISM', 'Vandalism'),
        ('CHILD ABUSE', 'Child Abuse'),
        ('ARSON', 'Arson'),
        ('CULTISM', 'Cultism'),
        ('OTHERS', 'Others'),
    ]

    DEFAULT_CRIME = 'SELECT_CRIME'  # Set default crime

    crime = models.CharField(max_length=50, choices=CRIME_CHOICES, default=DEFAULT_CRIME)
    description = models.TextField()
    crime_location = models.CharField(max_length=100)
    image_evidence = models.ImageField(upload_to='crime_reports/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Anonymous Report #{self.id}"
    


class CitizenReport(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
    ]

    CRIME_CHOICES = [
        ('SELECT_CRIME', 'Select a crime'),  # Placeholder option
        ('THEFT', 'Theft'),
        ('MURDER', 'Murder'),
        ('KIDNAPPING', 'Kidnapping'),
        ('CYBERCRIME', 'Cybercrime'),
        ('BURGLARY', 'Burglary'),
        ('TRAFFICKING', 'Trafficking'),
        ('BANDITRY', 'Banditry'),
        ('MANSLAUGHTER', 'Manslaughter'),
        ('RAPE', 'Rape'),
        ('ROBBERY', 'Robbery'),
        ('EXAM_MALPRACTICE', 'Exam Malpractice'),
        ('ASSAULT', 'Assault'),
        ('FRAUD', 'Fraud'),
        ('VANDALISM', 'Vandalism'),
        ('CHILD ABUSE', 'Child Abuse'),
        ('ARSON', 'Arson'),
        ('CULTISM', 'Cultism'),
        ('OTHERS', 'Others'),
    ]

    DEFAULT_CRIME = 'SELECT_CRIME'  # Set default crime
    DEFAULT_STATUS = 'PENDING'  # Set default status

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crime = models.CharField(max_length=50, choices=CRIME_CHOICES, default=DEFAULT_CRIME)
    description = models.TextField()
    crime_location = models.CharField(max_length=100)
    image_evidence = models.ImageField(upload_to='crime_reports/')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=DEFAULT_STATUS)

    def __str__(self):
        return f"Citizen Report #{self.id}"
    

    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=50)
    image = models.ImageField(default='default.png',
                              upload_to='profile_images')

    def __str__(self):
        return f'{self.user.username}-Profile'
