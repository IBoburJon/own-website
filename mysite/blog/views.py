from django.core import paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post, Comment
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from taggit.models import Tag

def post_list(request, tag_slug=None):
    posts = Post.objects.all()
    comments = Comment.objects.all()
    tag=None
    context = {}

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])

    paginator = Paginator(posts, 4)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    

    if request.method == "POST":
        form = CommentForm(request.POST)
        context = {}
        if form.is_valid():
            form = CommentForm(request.POST)
            try:
                form.save()
                return redirect('blog:post_list')
            except:
                pass
        else:
            form = CommentForm()

    context = {'page': page,
                'posts': posts,
                'tag': tag,
                'comments': comments,}

    return render(request, 'blog/post/list.html', context)

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug = post,
                                   status = 'published',
                                   publish__year = year,
                                   publish__month = month,
                                   publish__day = day)

    comments = post.comments.filter(active=True)
    if request.method == 'POST':

        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()
    
    return render(request, 'blog/post/detail.html', {'post': post,
                                                     'comments': comments,
                                                     'comment_form': comment_form})



def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['email'])
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent,})
