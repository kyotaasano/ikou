from django.shortcuts import render, get_object_or_404,redirect
from django.shortcuts import render
from django.views.generic import View
from .forms import SearchForm, SearchAForm
from .forms import AddForm
import json
import requests
from django.http import HttpResponse
from .models import Memo 
from . import forms
from django.views.generic import TemplateView
from django.core.paginator import Paginator
#from datetime import datetime



SEARCH_URL = 'https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706?format=json&applicationId=1095746777661250287'

def index(request):
    products = Memo.objects.all().order_by('date')
    searchForm = SearchAForm(request.GET)
    if searchForm.is_valid():
        search = searchForm.cleaned_data['name']
        product = Memo.objects.filter(name__icontains=search)
    else:
        searchForm = SearchAForm()
        product = Memo.objects.all().order_by('date')
    contents = {
        "title":'買い物一覧',
        'products':products,
        '編集':'編集',
        '商品名':'商品名',
        '説明':'説明',
        '日付':'日付',
        'IMG':'IMG',
        'searchForm':searchForm,
        'product':product
        }
    return render(request,'myshop/base.html',contents)

def edit(request, id):
    if request.method == 'POST':
        memo = get_object_or_404(Memo, pk=id)
        memoForm = AddForm(request.POST, instance=memo)
        if memoForm.is_valid():
            memoForm.save()
            return redirect(to='/myshop')
    else:
        memo = get_object_or_404(Memo, pk=id)  
        memoForm = AddForm(instance=memo)
        contents = {
            'Form': memoForm,
            'info': memo,
        }
        return render(request, 'myshop/edit.html', contents)

def delete(request, id):
    memo = get_object_or_404(Memo, pk=id)
    memo.delete()
    return redirect(to='/myshop')

def create(request):
    if request.method == "POST":
        obj = Memo()
        memo = AddForm(request.POST, instance=obj)
        memo.save()
        return redirect(to='/myshop')
    iName = request.GET.get('iName')
    iDsc = request.GET.get('iDsc')
    #idate= datetime.datetime.now()
    iC = request.GET.get('iC')
    
    initial_dict = dict(name=iName,dsc=iDsc[:50],pic=iC,)
    form = AddForm(initial=initial_dict)
    context = {
        'form':form,
        'back':request.META.get('HTTP_REFERER'),
    }
    return render(request, 'myshop/create.html', context)

def get_api_data(params):
    api = requests.get(SEARCH_URL, params=params).text
    result = json.loads(api)
    items = result['Items']
    return items

class IndexView(View):

    def get(self, request, *args, **kwargs):
        form = SearchForm(request.POST or None)

        return render(request, 'myshop/index.html', {
            'form': form,
            })

    def post(self, request, *args, **kwargs):
        form = SearchForm(request.POST or None)

        if form.is_valid():
            keyword = form.cleaned_data['itemName']
            params = {
                'keyword': keyword,
                'hits': 28,
            }
            items = get_api_data(params)
            item_data = []
            for i in items:
                item = i['Item']
                itemName = item['itemName']
                image = item['mediumImageUrls'][0]['imageUrl']
                itemCode = item['itemCode']
                itemPrice = item['itemPrice']
                query = {
                        'itemName': itemName,
                        'image': image,
                        'itemCode': itemCode,
                        'itemPrice': itemPrice,
                }
                item_data.append(query)

            return render(request, 'myshop/item.html', {
                'item_data': item_data,
                'keyword': keyword
            })

        return render(request, 'myshop/index.html', {
            'form': form
        })

class DetailView(View):
    	
    def get(self, request, *args, **kwargs):
        itemCode = self.kwargs['itemCode']
        params = {
            'itemCode': itemCode
        }

        items = get_api_data(params)
        items = items[0]
        item = items['Item']
        itemName = item['itemName']
        image = item['mediumImageUrls'][0]['imageUrl']
        itemPrice = item['itemPrice']
        shopName = item['shopName']
        itemCode = item['itemCode']
        itemCaption = item['itemCaption']
        itemUrl = item['itemUrl']
        reviewAverage = item['reviewAverage']
        reviewCount = item['reviewCount']

        item_data = {
            'itemName': itemName,
            'image': image,
            'itemPrice': itemPrice,
            'shopName': shopName,
            'itemCode': itemCode,
            'itemCaption': itemCaption,
            'itemUrl': itemUrl,
            'reviewAverage': reviewAverage,
            'reviewCount': reviewCount,
            'average': float(reviewAverage) * 20
        }
       
        return render(request, 'myshop/detail.html', {
             'item_data': item_data      
        })
 
"""----------------------------------------------------------"""
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import SignUpForm

class SignUp(CreateView):
    form_class = SignUpForm
    template_name = "myshop/signup.html" 
    success_url = reverse_lazy('top')

    def form_valid(self, form):
        user = form.save() # formの情報を保存
        login(self.request, user) # 認証
        self.object = user 
        return HttpResponseRedirect(self.get_success_url())
   
        
        
