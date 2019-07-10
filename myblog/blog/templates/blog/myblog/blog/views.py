from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post
from django.utils import timezone
from django.http.response import HttpResponse
from .forms import PostForm

# Create your views here.
def post_list(request):
    posts = Post.objects.filter(
        published_date__lte=timezone.now()).order_by(
            'published_date')
    return render(request, 'blog/post_list.html', 
                  {'posts':posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', 
                  {'post':post})
    
# post_new는 폼으로 연결해주는 함수이다.    
def post_new(request):
    # request는 사용자의 요청, method는 요청 방식
    # GET방식으로 들어온 요청인지 POST방식으로 들어온 요청인지 검사.
    # form의 method="post"이므로 form을 사용해 들어온 자료는 무조건 post여야함
    if request.method == "POST":
        form = PostForm(request.POST)
        # .is_valid()는 form을 통해 넘어온 자료가 유효한 자료인지 검증
        if form.is_valid():
            # 우선 form에서 입력한 title, text 정보를 넘겨받고
            # (pk, create_date관련 정보는 자동입력됨)
            post = form.save(commit = False)
            # 글쓴이 관련 정보 추가
            post.author = request.user
            # 배포 관련 정보 추가
            post.published_date = timezone.now()
            # 6개 컬럼에 대한 정보 완전히 입력 후 DB반영
            post.save()
            # 글 다 썼으면 detail 페이지에서 쓴 글 확인.
            return redirect('post_detail', pk=post.pk)
    else:
        # 만들어놨던 폼 양식을 가져오기 위해서는
        # 변수 = 폼양식() 를 써야 한다. () 가 우측에 붙음에 주의.
        # 현재 코드는 PostForm() 양식을 따라 만들것임을 보여준다.
        form = PostForm()
    # 저장한 폼 양식은 템플릿 파일에 같이 넘겨야 한다.
    return render(request, 'blog/post_edit.html',
                  {'form':form})

def post_edit(request, pk):
    # 글을 수정해야 하기 때문에 기존에 입력되어 있던 자료를 가져오는게 먼저임.
    post = get_object_or_404(Post, pk=pk)
    # get방식 post방식 구분
    if request.method == "POST":
        # post방식인 경우는 기존 자료 post에 새로 들어온 정보를 덮어씌움
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # published_date를 다시 현재 서버시간으로 변경
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        # 만약 post방식이 아닌 경우라면 get방식 이므로 수정 직전임
        # 따라서 폼으로 다시 연결해줘야함. 이 때 의 폼은 수정용 폼이며
        # 수정용 폼에는 기존에 써놨었던 글이 먼저 입력되어 있어야 하므로
        # 감안해서 기존 글의 내용이 담겨있는 post를 폼에 instance로 넘겨줌
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', 
                  {'form':form})





