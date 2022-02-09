from main.models import Post


def post_exists(id: int) -> bool:
    return Post.objects.filter(id=id).exists()
