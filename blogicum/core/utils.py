from django.db.models import Count
from django.utils import timezone

from blog.models import Post


def select_posts(only_published=True, **filters):
    published_filters = {'pub_date__lte': timezone.now(), 'is_published': True}
    if not only_published:
        published_filters = {}
    return (
        Post.objects.select_related('category', 'author')
        .prefetch_related('location')
        .filter(**published_filters, **filters)
        .annotate(comment_count=Count('comments'))
        .order_by('-pub_date')
    )
