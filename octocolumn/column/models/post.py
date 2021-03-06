import time

from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from utils.filepath import cover_image_user_directory_path, preview_image_user_directory_path, \
    thumbnail_image_user_directory_path

__all__ = (
    'Post',
    'PostLike',
    'PreAuthorPost'
)


class Post(models.Model):
    # 1. 이 Post를 좋아요 한 개수를 저장할 수 있는 필드(like_count)를 생성 -> migration
    # 2. 이 Post에 연결된 PostLike의 개수를 가져와서 해당 필드에 저장하는 메서드 구현
    author = models.ForeignKey('member.User', null=True)
    title = models.CharField(max_length=255)
    main_content = models.TextField()
    preview = models.TextField(null=True)
    hit = models.PositiveIntegerField(default=0)
    buy_count = models.PositiveIntegerField(default=0)
    price = models.IntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    like_users = models.ManyToManyField(
        'member.User',
        related_name='like_posts',
        through='PostLike',
    )
    like_count = models.PositiveIntegerField(default=0)
    cover_image = models.ImageField('포스트커버 이미지',
                                    upload_to=cover_image_user_directory_path,
                                    blank=True,
                                    null=True
                                    )
    thumbnail = models.ImageField('섬네일 이미지',
                                  upload_to=thumbnail_image_user_directory_path,
                                  blank=True,
                                  null=True
                                  )

    tags = models.ManyToManyField('column.Tag',
                                  related_name='column',
                                  blank=True)

    recommend = models.ManyToManyField('column.Recommend',
                                       related_name='recommand',
                                       blank=True,
                                       )

    class Meta:
        ordering = ['-pk', ]
        verbose_name = '포스팅된 컬럼'
        verbose_name_plural = f'{verbose_name} 목록'

    def add_comment(self, user, content):
        # 자신을 post로 갖고, 전달받은 user를 author로 가지며
        # content를 content필드내용으로 넣는 Comment객체 생성
        return self.comment_set.create(author=user, content=content)

    # 이 메서드를 적절한 곳에서 호출
    def calc_like_count(self):
        time.sleep(2)
        self.like_count = self.like_users.count()
        self.save()

    @property
    def author_nickname(self):
        if self.author is not None:
            return self.author.nickname

    @property
    def tags_indexing(self):
        return [tag.title for tag in self.tags.all()]


class PostLike(models.Model):
    post = models.ForeignKey('column.Post',null=True)
    user = models.ForeignKey('member.User',null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            ('post', 'user'),
        )


class PreAuthorPost(models.Model):
    author = models.ForeignKey('member.User', null=True)
    title = models.CharField(max_length=255)
    main_content = models.TextField()
    preview = models.TextField(null=True)
    price = models.PositiveIntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    cover_image = models.ImageField(
        '포스트커버 이미지',
        upload_to=cover_image_user_directory_path,
        blank=True,
        null=True
    )

    thumbnail = models.ImageField(
        '섬네일 이미지',
        upload_to=thumbnail_image_user_directory_path,
        blank=True,
        null=True
    )

    tags = models.ManyToManyField('column.PreTag',
                                  related_name='pretag',
                                  blank=True)

    recommend = models.ManyToManyField('column.PreRecommend',
                                       related_name='prerecommand',
                                       blank=True,
                                       )

    class Meta:
        ordering = ['-created_date', ]
        verbose_name = '작가신청용 포스팅 컬럼'
        verbose_name_plural = f'{verbose_name} 목록'


@receiver(post_save, sender=PostLike, dispatch_uid='postlike_save_update_like_count')
@receiver(post_delete, sender=PostLike, dispatch_uid='postlike_delete_update_like_count')
def update_post_like_count(sender, instance, **kwargs):
    if kwargs['signals'].receivers[0][0][0] == 'postlike_save_update_like_count':
        instance.post.like_count += 1
    else:
        instance.post.like_count -= 1
    instance.post.save()
    print('Signal update_post_like_count, instance: {}'.format(
        instance
    ))
    # instance.post.calc_like_count()
    # task_update_post_like_count.delay(post_pk=instance.post.pk)


# class MyPost(models.Model):
#     update_date = models.DateTimeField(auto_now_add=True)
#     user = models.ForeignKey('member.User',null=True)
#     post = models.ForeignKey('column.Post',null=True)
#
#     def __str__(self):
#         return '{} : {}'.format(
#             self.user,
#             self.post,
#         )

