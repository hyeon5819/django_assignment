from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import *
from .forms import *
from django.http import HttpResponse


# Create your views here.
# 로그인 후 홈화면 띄우기(메인 페이지)
def main(request):
    return redirect('/home')


# 홈화면 GET 요청
def home(request):
    if request.method == 'GET':
        return render(request, 'erp/mainpage.html')


# 제품 리스트 보여주기 위해 데이터베이스에서 가져오기
@login_required
def product_list(request):
    if request.method == 'GET':
        database_list = Product.objects.all()
        return render(request, 'erp/product_list.html', {'database_list': database_list})


# 제품 등록 GET, POST 요청
@login_required
@user_passes_test(lambda user: user.is_staff, login_url='/error/')
def product_create(request):
    if request.method == 'GET':
        form = ProductForm()

        return render(request, 'erp/product_create.html', {'form': form})

    elif request.method == 'POST':
        form = ProductForm(request.POST)

        if form.is_valid():
            product = form.save(commit=False)
            product.save()

            # 추가 등록시 = 확인 / 홈으로 가기 = 취소
            return HttpResponse(
                '<script>if (confirm("상품이 등록되었습니다. 계속 등록하시겠습니까?")) {'
                'location.href="/product_create";} else {'
                'location.href="/home";}</script>'
            )


# 입고 처리
@login_required
@user_passes_test(lambda user: user.is_staff, login_url='/error/')
def inbound_create(request):
    if request.method == 'GET':
        form = InboundForm()
        products = Product.objects.all()

        return render(request, 'erp/inbound_create.html', {'products': products, 'form':form})

    elif request.method == 'POST':
        form = InboundForm(request.POST)

        if form.is_valid():
            product = form.cleaned_data['product']
            quantity = form.cleaned_data['quantity']
            inventory = product.inventory

            inbound = Inbound(product=product, quantity=quantity)
            inbound.save()

            inventory.inbound_quantity += quantity
            inventory.save()

            return redirect('inbound_create')


# 출고 처리
@login_required
@user_passes_test(lambda user: user.is_staff, login_url='/error/')
def outbound_create(request):
    if request.method == 'GET':
        form = OutboundForm()
        products = Product.objects.all()

        return render(request, 'erp/outbound_create.html', {'products': products, 'form':form})

    elif request.method == 'POST':
        form = OutboundForm(request.POST)

        if form.is_valid():
            product = form.cleaned_data['product']
            quantity = form.cleaned_data['quantity']
            inventory = product.inventory

            outbound = Outbound(product=product, quantity=quantity)
            outbound.save()

            inventory.outbound_quantity -= quantity
            inventory.save()

            return redirect('outbound_create')


# 재고 리스트 GET 요청
@login_required
@user_passes_test(lambda user: user.is_staff, login_url='/error/')
def inventory(request):
    products = Product.objects.all()

    return render(request, 'erp/inventory.html', {'products':products})


    # total_price = []
    # for product in products:
    #     total_inbound_price = product.inventory.inbound_quantity
    #     total_outbound_price = product.inventory.outbound_quantity
    #     total_sum = total_inbound_price + total_outbound_price
    #     total_price.append({'code':product.code,
    #                         'name':product.name,
    #                         'total_inbound_price':total_inbound_price,
    #                         'total_outbound_price':total_outbound_price,
    #                         'total_sum':total_sum,
    #                         })
    # return render(request, 'erp/inventory.html', {'products':products,
    #                                               'total_price':total_price,
    #                                               })


# staff권한 없을시 접근불가
def error(request):
    return render(request, 'erp/error.html')