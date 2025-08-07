from django.urls import reverse
from .models import Product
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductForm , CustomUserCreationForm , CommentForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth import views as auth_views
from .token import password_reset_token
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.core.mail import send_mail
from django.http import HttpResponse

#Authentication
class CustomPasswordResetView(auth_views.PasswordResetView):
    email_template_name = 'registration/password_reset_email.html'
    template_name = 'registration/password_reset_form.html'
    token_generator = password_reset_token
    success_url = '/accounts/reset-password/done/'

    def form_valid(self, form):
        print(f"Password reset requested for: {form.cleaned_data['email']}")
        print(f"Using token generator: {self.token_generator}")
        return super().form_valid(form)

#Sign Up View
# In views.py
def registration_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            next_url = request.POST.get('next') or request.GET.get('next') or 'product_list'
            return redirect(next_url)
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {
        'form': form,
        'next': request.GET.get('next', '')
    })

#Displays the products/Posts
@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'gallery/index1.html', {'products': products})

#Product Details inclusive of comments and likes #READ
@login_required
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    comments = product.comments.all().order_by('-date_posted')

    # Get next and previous posts (ordered by creation date)
    all_posts = list(Product.objects.order_by('-created_at'))
    current_index = all_posts.index(product)
    
    previous_post = all_posts[current_index + 1] if current_index < len(all_posts) - 1 else None
    next_post = all_posts[current_index - 1] if current_index > 0 else None

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.user = request.user
            comment.save()
            return redirect('product_detail', slug=product.slug)
    else:
        form = CommentForm()

    return render(request, 'gallery/index2.html', {
        'product': product,
        'comments': comments,
        'form': form,
        'previous_post': previous_post,
        'next_post': next_post,
    })

#Product/Post Creation #CREATE
@login_required
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.author = request.user  #Set the author to current user
            product.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'gallery/create.html', {'form': form})

#Editing Created Products/Posts #EDIT
@login_required
def edit_product(request, slug):
    product = get_object_or_404(Product, slug=slug)

    # Check if current user is the author
    if product.author != request.user:
        return HttpResponseForbidden("You don't have permission to edit this post")
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES ,instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'gallery/edit.html', {'form': form})

#Deleteing an existing Product/Post #DELETE
@login_required
def delete_product(request, slug):
    product = get_object_or_404(Product, slug=slug)

    #Check if current user is the author
    if product.author != request.user:
        return HttpResponseForbidden("You don't have permission to delete this post")
    
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'gallery/delete.html', {'product': product})

#Display Products/Posts on Home Page #READ
def home(request):
    product = Product.objects.all().order_by('-date_posted')
    return render (request, 'gallery/index1.html',{'product': product})

@login_required
def discover_posts(request):
    """Show only other users' posts"""
    if request.user.is_authenticated:
        products = Product.objects.exclude(author=request.user).order_by('-created_at')
    else:
        products = Product.objects.all().order_by('-created_at')
    return render(request, 'gallery/discover.html', {'products': products})

@login_required
def my_blogs(request):
    """Show only the logged-in user's posts"""
    products = Product.objects.select_related('author').filter(author=request.user).order_by('-created_at')
    return render(request, 'gallery/my_blogs.html', {'products': products})

@login_required
def like_post(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.user.is_authenticated:
        if product.likes.filter(id=request.user.id).exists():
            product.likes.remove(request.user)
        else:
            product.likes.add(request.user)
    return redirect(reverse('product_detail', args=[str(product.slug)])) #Where to redirect after like

    