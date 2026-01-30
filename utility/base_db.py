from app.models.models import Lang, PostType, User



lang1 = Lang(
        code='en',
        name='English',
        )

lang2 = Lang(
        code='es',
        name='Spanish',
        )

post = PostType(
        name='post',
        )

poem = PostType(
        name='poem',
        )

story = PostType(
        name='story',
        )

author1 = User(
        username='Laotze',
        )

languages = [lang1, lang2]
types = [post, poem, story]
users = [author1]
