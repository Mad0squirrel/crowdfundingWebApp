from django.utils import timezone
from django.db import models

from django.db import models
from pkg_resources import require
from apps.authentication.models import Register
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.


class Category(models.Model):
    """
    Модель категории для проектов.
    """
    name = models.CharField(max_length=250)
    
    def __str__(self):
        """
        Возвращает имя категории в виде строки.
        """
        return self.name


class Tag(models.Model):
    """
    Модель тега, который может быть связан с проектами.
    """
    name = models.CharField(max_length=100,null=True, blank=True)

    def __str__(self):
        """
        Возвращает строковое представление объекта класса Tag.
        """
        return self.name


class Project(models.Model):
    """
    Класс Project описывает модель проекта в приложении.


    Атрибуты:
    ---------
    title: CharField с максимальной длиной 100 символов, название проекта.
    details: TextField, описание проекта.
    total_target: FloatField, общая сумма целевого финансирования проекта.
    start_time: DateTimeField с временной зоной, дата и время начала проекта.
    end_time: DateTimeField с временной зоной, дата и время окончания проекта.
    is_featured: BooleanField, флаг, указывающий, является ли проект выделенным на главной странице.
    category: ForeignKey на модель Category, категория проекта.
    user: ForeignKey на модель Register, пользователь, создавший проект.
    tag: ManyToManyField на модель Tag, теги, связанные с проектом.
    created_at: DateTimeField с авто-заполнением текущей даты и времени при создании объекта.
    """
    title = models.CharField(max_length=100)
    details = models.TextField()
    total_target = models.FloatField()
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=timezone.now)
    is_featured = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(Register, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
   

    def __str__(self):
        return self.title
    

class Image(models.Model):
    """
        Модель изображения.

        :param images: изображение в формате ImageField
        :type images: ImageField
        :param project: проект, к которому относится изображение
        :type project: Project
    """
    images = models.ImageField(upload_to="")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, default=None)


class Comment(models.Model):
    """
    Модель комментария к проекту.


    Атрибуты:
    ---------
    comment: текст комментария.
    project: внешний ключ на модель проекта, к которому относится комментарий.
    user: внешний ключ на модель пользователя, который написал комментарий.
    created_at: дата и время создания комментария.
    """
    comment = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(Register, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(f'comment by {self.user.first_name} on {self.project.title} project.')


class Donation(models.Model):
    """
    Модель, представляющая пожертвование.

    Атрибуты:
    ---------
    donation (FloatField): сумма пожертвования;
    project (ForeignKey): ссылка на проект, на который было сделано пожертвование;
    user (ForeignKey): ссылка на пользователя, который сделал пожертвование;
    created_at (DateTimeField): дата и время создания записи.
    """
    donation = models.FloatField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(Register, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Project_Report(models.Model):
    """
    Класс Project_Report представляет отчет о проекте, который был сделан пользователем.
    Класс наследуется от models.Model.


    Атрибуты:
    ---------
    report - отчет о проекте, выбирается из списка возможных значений, хранится в виде строки (CharField).
    project - внешний ключ на проект (ForeignKey). Указывает на Project, на который создан отчет.
    При удалении связанного проекта, отчеты также будут удалены (on_delete=models.CASCADE).
    user - внешний ключ на пользователя (ForeignKey). Указывает на Register, который создал отчет.
    При удалении связанного пользователя, отчеты также будут удалены (on_delete=models.CASCADE).
    """
    REPOT_DATA=[('ip','inappropriate'),('ags','aggressive')]
    report =  models.CharField(
        max_length=200,
        choices=REPOT_DATA,
        default='ip',
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(Register, on_delete=models.CASCADE)


class Comment_Report(models.Model):
    """
    Класс для представления отчета о нарушении правил в комментарии пользователей.


    Атрибуты:
    ---------
    report: строка, отражающая тип нарушения правил (по умолчанию 'ip' - неприемлемый комментарий);
    comment: внешний ключ на объект Comment, который был отмечен пользователем как нарушитель правил;
    user: внешний ключ на объект Register, который является автором отчета о нарушении правил.
    """
    REPOT_DATA=[('ip','inappropriate')]
    report =  models.CharField(
        max_length=200,
        choices=REPOT_DATA,
        default='ip',
    )
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(Register, on_delete=models.CASCADE)


class Reply(models.Model):
    """
    Модель, описывающая ответы на комментарии к проекту.


    Атрибуты:
    ---------
    reply - текст ответа на комментарий
    comment - комментарий, на который был дан ответ
    user - пользователь, который оставил ответ
    created_at - дата и время создания ответа
    """
    reply = models.CharField(max_length=30)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(Register, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Rate(models.Model):
    """
    Класс для хранения рейтинга проекта.


    Атрибуты:
    ---------
    rate (models.IntegerField) - оценка проекта, заданная пользователем. Должна быть целым числом.
    project (models.ForeignKey) - внешний ключ на проект, для которого задается оценка. Ссылается на модель Project.
    user (models.ForeignKey) - внешний ключ на пользователя, который оценил проект. Ссылается на модель Register.
    """
    rate = models.IntegerField()
    projcet = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(Register, on_delete=models.CASCADE)
