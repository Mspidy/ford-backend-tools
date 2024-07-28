from django.db import models

# Create your models here.
class TeacherDetails(models.Model):
    teacher_id = models.CharField(max_length=100)
    teacher_name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    pan_card = models.CharField(max_length=100)
    aadhar_card = models.CharField(max_length=100)
    mobile_number =  models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    salary =  models.CharField(max_length=100)
    alter_number =  models.CharField(max_length=100)
    date_of_birth = models.DateField()
    previous_school_name = models.CharField(max_length=250)
    transport_fees =  models.CharField(max_length=100)
    graduation_complete = models.BooleanField(default=False)
    bed_complete = models.BooleanField(default=False)
    created_by = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.teacher_id:
            last_instance = TeacherDetails.objects.order_by('-teacher_id').first()
            if last_instance:
                last_sequence = int(last_instance.teacher_id[2:])
                next_sequence = last_sequence + 1
                self.teacher_id = f"TR{str(next_sequence).zfill(4)}"
            else:
                self.teacher_id = "TR0001"
        super().save(*args, **kwargs)