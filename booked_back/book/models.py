from django.db import models
from user.models import Profile
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Feeling(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name
    
class Genre(models.Model):
    name=models.CharField(max_length=255)
    def __str__(self):
        return self.name

class EI(models.Model):
    name=models.CharField(max_length=255)
    def __str__(self):
        return self.name
    
class NS(models.Model):
    name=models.CharField(max_length=255)
    def __str__(self):
        return self.name
    
class FT(models.Model):
    name=models.CharField(max_length=255)
    def __str__(self):
        return self.name
    
class JP(models.Model):
    name=models.CharField(max_length=255)
    def __str__(self):
        return self.name
    
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    genre=models.ManyToManyField(Genre,through="GenreCount",related_name='books')
    description = models.TextField()
    ei=models.ManyToManyField(EI,through="EICount",related_name='books')
    ns=models.ManyToManyField(NS,through="NSCount",related_name='books')
    ft=models.ManyToManyField(FT,through="FTCount",related_name='books')
    jp=models.ManyToManyField(JP,through="JPCount",related_name='books')
    fellings = models.ManyToManyField(Feeling, through='FillingCount', related_name='books')
    def __str__(self):
        return self.title
    #user_mbti = models.ManyToManyField(Profile, through='UserMBTICount', related_name='books')
    
    
class BookReview(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='reviews')
    review_title=models.CharField(max_length=255)
    book_title = models.CharField(max_length=255)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews',null=True,blank=True)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='reviews')
    feeling = models.ForeignKey(Feeling, on_delete=models.CASCADE, related_name='reviews')
    ei = models.ForeignKey(EI, on_delete=models.CASCADE, related_name='reviews')
    ns = models.ForeignKey(NS, on_delete=models.CASCADE, related_name='reviews')
    ft = models.ForeignKey(FT, on_delete=models.CASCADE, related_name='reviews')
    jp = models.ForeignKey(JP, on_delete=models.CASCADE, related_name='reviews')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like=models.ManyToManyField(Profile,related_name='likes',blank=True)
    pickpage=models.CharField(max_length=255,null=True,blank=True)
    pickwriting=models.CharField(max_length=255,null=True,blank=True)
    
    def __str__(self):
        return self.review_title
    
    def get_like_count(self):
        return self.like.count()
    
    def save(self, *args, **kwargs):
        if not self.pk:
            # 책 제목과 대응되는 book 모델이 없을 경우 새로운 book 모델을 생성하여 연결합니다.
            book, _ = Book.objects.get_or_create(title=self.book_title)
            self.book = book
        super().save(*args, **kwargs)
        
        genre_count, _ = GenreCount.objects.get_or_create(book=self.book, category=self.genre)
        genre_count.mention_count = BookReview.objects.filter(book=self.book, genre=self.genre).count()
        genre_count.save()
        feeling_count, _ = FillingCount.objects.get_or_create(book=self.book, category=self.feeling)
        feeling_count.mention_count = BookReview.objects.filter(book=self.book, feeling=self.feeling).count()
        feeling_count.save()
        ei_count, _ = EICount.objects.get_or_create(book=self.book, category=self.ei)
        ei_count.mention_count = BookReview.objects.filter(book=self.book, ei=self.ei).count()
        ei_count.save()
        ns_count, _ = NSCount.objects.get_or_create(book=self.book, category=self.ns)
        ns_count.mention_count = BookReview.objects.filter(book=self.book, ns=self.ns).count()
        ns_count.save()
        ft_count, _ = FTCount.objects.get_or_create(book=self.book, category=self.ft)
        ft_count.mention_count = BookReview.objects.filter(book=self.book, ft=self.ft).count()
        ft_count.save()
        jp_count, _ = JPCount.objects.get_or_create(book=self.book, category=self.jp)
        jp_count.mention_count = BookReview.objects.filter(book=self.book, jp=self.jp).count()
        jp_count.save()
        
        
    # BookReview 모델의 post_save 시그널 리시버
@receiver(post_save, sender=BookReview)
def update_genre_count(sender, instance, created, **kwargs):
    if created:
        # 새로운 독후감이 작성될 때만 업데이트합니다.
        genre_count, _ = GenreCount.objects.get_or_create(book=instance.book, category=instance.genre)
        genre_count.mention_count = BookReview.objects.filter(book=instance.book, genre=instance.genre).count()
        genre_count.save()
        feeling_count, _ = FillingCount.objects.get_or_create(book=instance.book, category=instance.feeling)
        feeling_count.mention_count = BookReview.objects.filter(book=instance.book, feeling=instance.feeling).count()
        feeling_count.save()
        ei_count, _ = EICount.objects.get_or_create(book=instance.book, category=instance.ei)
        ei_count.mention_count = BookReview.objects.filter(book=instance.book, ei=instance.ei).count()
        ei_count.save()
        ns_count, _ = NSCount.objects.get_or_create(book=instance.book, category=instance.ns)
        ns_count.mention_count = BookReview.objects.filter(book=instance.book, ns=instance.ns).count()
        ns_count.save()
        ft_count, _ = FTCount.objects.get_or_create(book=instance.book, category=instance.ft)
        ft_count.mention_count = BookReview.objects.filter(book=instance.book, ft=instance.ft).count()
        ft_count.save()
        jp_count, _ = JPCount.objects.get_or_create(book=instance.book, category=instance.jp)
        jp_count.mention_count = BookReview.objects.filter(book=instance.book, jp=instance.jp).count()
        jp_count.save()

class FillingCount(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    category = models.ForeignKey(Feeling, on_delete=models.CASCADE)
    mention_count = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.book.title}: {self.category.name} ({self.mention_count}개)"

    class Meta:
        verbose_name_plural = "Feeling Counts"
    

class GenreCount(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    category = models.ForeignKey(Genre, on_delete=models.CASCADE)
    mention_count = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.book.title}: {self.category.name} ({self.mention_count}개)"

    class Meta:
        verbose_name_plural = "Genre Counts"
    
   
class EICount(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    category = models.ForeignKey(EI, on_delete=models.CASCADE)
    mention_count = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.book.title}: {self.category.name} ({self.mention_count}개)"

    class Meta:
        verbose_name_plural = "EI Counts"
    
    
class NSCount(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    category = models.ForeignKey(NS, on_delete=models.CASCADE)
    mention_count = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.book.title}: {self.category.name} ({self.mention_count}개)"

    class Meta:
        verbose_name_plural = "NS Counts"
    
    
class FTCount(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    category = models.ForeignKey(FT, on_delete=models.CASCADE)
    mention_count = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.book.title}: {self.category.name} ({self.mention_count}개)"

    class Meta:
        verbose_name_plural = "FT Counts"
    
    
class JPCount(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    category = models.ForeignKey(JP, on_delete=models.CASCADE)
    mention_count = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.book.title}: {self.category.name} ({self.mention_count}개)"

    class Meta:
        verbose_name_plural = "JP Counts"
    
    
'''class UserMBTICount(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    category = models.ForeignKey(Profile, on_delete=models.CASCADE)
    mention_count = models.IntegerField(default=0)'''