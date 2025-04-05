from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Product, Cart, Order, Profile
from .forms import RegisterForm, ProfileForm

# 🏠 Home View
def home(request):
    products = Product.objects.all()
    query = request.GET.get('q')
    category = request.GET.get('category')

    if query:
        products = products.filter(name__icontains=query)
    if category:
        products = products.filter(category__iexact=category)

    return render(request, 'store/index.html', {'products': products})

# 🛍 Product Detail View
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'store/product_detail.html', {'product': product})

# ✅ Register View (with auto login)
def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True  # Ensure user is active
            user.save()
            # ✅ Optional: Auto-create profile if not using signals
            Profile.objects.get_or_create(user=user)
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'store/register.html', {'form': form})

# 🔐 Login View
def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'store/login.html', {'form': form})

# 🚪 Logout
def logout_user(request):
    logout(request)
    return redirect('home')

# 🛒 Add to Cart
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)

    if not created:
        cart_item.quantity += 1
    cart_item.save()

    print(f"CartItem saved: {cart_item}")  # 👈 DEBUG PRINT

    return redirect('cart')


# 🛒 View Cart

@login_required
def cart(request):
    items = Cart.objects.filter(user=request.user)
    total = sum(item.total_price() for item in items)
    return render(request, 'store/cart.html', {
        'items': items,
        'total': total
    })

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(Cart, id=item_id, user=request.user)
    item.delete()
    return redirect('cart')

# 💳 Checkout
@login_required
def checkout(request):
    items = Cart.objects.filter(user=request.user)
    if items:
        order = Order.objects.create(user=request.user)
        order.products.set(items)
        order.save()
        items.delete()
        return render(request, 'store/checkout.html', {'order': order})
    return redirect('cart')

# 👤 Profile
@login_required
def profile(request):
    # ✅ Fix: avoid "user has no profile"
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'store/profile.html', {'form': form})
