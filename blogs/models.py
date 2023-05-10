from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import User, PermissionsMixin, AbstractUser
from django.db import models
from django.urls import reverse


class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """

        user = self.model(
            email=email,
            username=username,

        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(
            email,
            username=username,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class User(AbstractUser):
    is_blogger = models.BooleanField(default=False)
    objects = MyUserManager()

    def has_perm(self, perm, obj=None):
        if perm == 'blogs.is_blogger':
            return self.is_blogger
        return True


class Blogger(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(max_length=1000)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('blogger-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return self.name


class Blog(models.Model):
    title = models.CharField(max_length=200)
    blogger = models.ForeignKey('Blogger', on_delete=models.SET_NULL, null=True)
    post_date = models.DateField(null=True, blank=True)
    description = models.TextField(max_length=1000)

    class Meta:
        ordering = ['-post_date']

    def get_absolute_url(self):
        """Returns the url to access a particular blogger instance."""
        return reverse('blog-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return self.title


class Comment(models.Model):
    description = models.TextField(max_length=1000, help_text="Enter comment about blog here")
    post_date = models.DateField(null=True, blank=True)
    blog = models.ForeignKey('Blog', on_delete=models.RESTRICT, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['post_date']

    def __str__(self):
        len_title = 75
        if len(self.description) > len_title:
            titlestring = self.description[:len_title] + '...'
        else:
            titlestring = self.description
        return titlestring

