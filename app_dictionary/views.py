from django.shortcuts import render,redirect
from django.contrib import messages
from app_dictionary.models import *
from .forms import ItemForm,RegisterForm
from django.contrib.auth.decorators import login_required
from .models import ItemModel,BillModel,ItemlistModel
from django.http import JsonResponse
# User=''
from django.contrib.auth import get_user_model
User = get_user_model()
from datetime import datetime,timedelta
import random
from twilio.rest import Client
from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ValidationError
from functools import wraps

def custom_admin_login_required(function):
    @wraps(function)
    def wraps(request,*args,**kwargs):
        if request.user and request.user.is_authenticated and request.user.is_superuser:
            return function(request,*args,**kwargs)
        else:
            return redirect(f"{settings.LOGIN_URL}?next={request.path}")


def home(request):
    return render(request,'home.html')

def dictionary(request):
    dict = dictionary_model.objects.all().order_by('id')
    try:
        response = request.get('https://www.example.com',timeout=5)
        is_online = response.status_code == 200
    except:
        is_online = False
    return render(request,'dictionary.html',{'dict':dict,'is_online':is_online})

def dictionary_add(request):
    try:
        response = request.get('https://www.example.com',timeout=5)
        is_online = response.status_code == 200
    except:
        is_online = False
    return render(request,'dictionary_add.html',{'is_online':is_online})

def add_words(request):
    if request.method == "POST":
        eng = request.POST.getlist('eng[]')
        mal = request.POST.getlist('mal[]')
        for i in range(len(eng)):
            print(f'{eng[i]} = {mal[i]}\n')
            dict = dictionary_model(eng_word=eng[i],mal_word=mal[i])
            dict.save()
    messages.info(request,'saved successfull')
    return redirect('dictionary_add')

def upload_file(request):
    if 'file' in request.FILES:
        file = request.FILES['file']
        file_content = file.read()
        words =  file_content.decode().split()
        for i in range(len(words)):
            if words[i].isalpha():
                dict1 = dictionary_model(eng_word=words[i])
            else:
                dict1.mal_word = words[i]
                dict1.save()
    return redirect('dictionary_add')

def delete_all(request):
    dict = dictionary_model.objects.all()
    dict.delete()
    return redirect('dictionary')

def test_words(request,pk):
    if pk == 0:
        dict = dictionary_model.objects.first()
    else:
        dict = dictionary_model.objects.get(id=pk)
    return render(request,'test_words.html',{"dict":dict})

def next_word(request,pk):
    try:
        next_word = dictionary_model.objects.filter(pk__gt=pk).order_by('pk').first()
        dict = next_word
        return render(request,'test_words.html',{"dict":dict})
    except:
        dict = dictionary_model.objects.last()
        return  render(request,'test_words.html',{"dict":dict})

def prev_word(request,pk):
    try:
        next_word = dictionary_model.objects.filter(pk__lt=pk).order_by('-pk').first()
        dict = next_word
        return render(request,'test_words.html',{"dict":dict})
    except:
        dict = dictionary_model.objects.first()
        return  render(request,'test_words.html',{"dict":dict})

def edit_word(request,pk):
    dict = dictionary_model.objects.get(id=pk)
    return render(request,'edit_word.html',{"dict":dict})

def save_word(request,pk):
    if request.method == "POST":
        eng = request.POST.get('eng')
        mal = request.POST['mal']
        dict = dictionary_model.objects.get(id=pk)
        dict.eng_word = eng
        dict.mal_word = mal
        dict.save()
        messages.info(request,'Word Successfully Saved  !')
    return redirect('test_words',pk=pk)



#======================  curryshop ===========================================

def index(request):
    return render(request,'curry_shop_index.html',{})

def register(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST,request.FILES)
        if form.is_valid():
            user = form.save()
            profile = ProfileModel.objects.create(
                user = user
            )
            return redirect('login')
    return render(request,'curry_shop_register.html',{'form':form})

@login_required
def profile(request):
    user = request.user
    user_data = User.objects.get(id=user.id)
    return render(request,'curry_shop_profile.html',{'user_data':user_data})

@login_required
def add_item(request):
    new_bill_count = BillModel.objects.filter(accept_status='notaccepted').count()

    form = ItemForm()
    if request.method == 'POST':
        form = ItemForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            # messages.success(request,f'Item {request.POST.get('name')} created successfully !')
            messages.success(request,f"Item {request.POST.get('name')} added successfull")
            if 'add_next' in request.POST:
                return redirect('add_item')
            else:
                return redirect('itemlist')
    return render(request,'curry_shop_add_item.html',{'form':form,
                                                      'new_bill_count':new_bill_count})

@login_required
def itemlist(request):
    items = ItemModel.objects.all().order_by('name')
    new_bill_count = BillModel.objects.filter(accept_status='notaccepted').count()
    return render(request,'curry_shop_itemlist.html',{'items':items,
                                                      'new_bill_count':new_bill_count})

@login_required
def item_details(request,pk):
    item = ItemModel.objects.get(id=pk) or None
    form = ItemForm(instance=item)

    new_bill_count = BillModel.objects.filter(accept_status='notaccepted').count()
    if request.method=="POST":
        form = ItemForm(request.POST,request.FILES,instance=item)
        if form.is_valid():
            form.save()
            return redirect('itemlist')
    return render(request,'curry_shop_item_details.html',{'item':item,
                                               'form':form,
                                               'new_bill_count':new_bill_count})

@login_required
def delete_item(request,pk):
    item = ItemModel.objects.get(id=pk)
    item.delete()
    return redirect('itemlist')

@login_required
def billitem(request):
    items = ItemModel.objects.all().order_by('name')
    new_bill_count = BillModel.objects.filter(accept_status='notaccepted').count()
    return render(request,'curry_shop_billitem.html',{'items':items,
                                                      'new_bill_count':new_bill_count})

@login_required
def addbill(request):
    try:
        # user=''
        user = User.objects.get(id=request.user.id)
    except:
        user=None

    if request.method=="POST":
        name = request.POST.getlist('itemname') or []
        temp_prize = request.POST.getlist('itemprize') or []
        temp_qty = request.POST.getlist('itemqty') or []
        total = request.POST.getlist('itemtotal') or []
        grnd_total = request.POST.get('grnd_total') or 0
        paid_amount = request.POST.get('paid_amount') or 0
        bal_amount = request.POST.get('bal_amount') or 0
        
        prize = [ 0.00 if i=='' else i for i in temp_prize]
        qty = [ 0.00 if i=='' else i for i in temp_qty]
        print(f"{name}{type(name)} {temp_prize}{type(temp_prize)} {temp_qty}{type(temp_qty)} {total}{type(total)} {grnd_total}{type(grnd_total)} {paid_amount}{type(paid_amount)} {bal_amount}{type(bal_amount)}")
        if name and prize and qty and total and grnd_total and paid_amount and bal_amount:
            bill = BillModel(
                user=user,
                grand_total=float(grnd_total),
                paid=float(paid_amount),
                bal=float(bal_amount),
            )
            bill.save()
            for i in range(len(name)):
                print(f'{name[i]}{type(name[i])} {prize[i]}{type(prize[i])} {qty[i]}{type(qty[i])} {total[i]}{total[i]}')
                itemlist = ItemlistModel(
                    bill=bill,
                    name=name[i],
                    prize=prize[i],
                    qty=qty[i],
                    total=float(total[i]),
                )
                itemlist.save()
            messages.success(request,f"Bill created successfull")
        else:
            messages.info(request,f"Fill All the fields.")
            return redirect('billitem')
    if 'billnext' in request.POST:
        return redirect('billitem')
    else:
        return redirect('bill_list')

@login_required
def new_bill_list(request):
    bills = BillModel.objects.filter(accept_status='notaccepted')
    new_bill_count = bills.count()
    itemlist = ItemlistModel.objects.all()
    return render(request,'curry_shop_new_bill_list.html',{
        'bills':bills,
        'itemlist':itemlist,
        'new_bill_count':new_bill_count})

@login_required
def bill_list(request):
    new_bill_count = BillModel.objects.filter(accept_status='notaccepted').count()
    bills = BillModel.objects.filter(accept_status='accepted').exclude(dispatched_status='dispatched')
    itemlist = ItemlistModel.objects.all()
    return render(request,'curry_shop_bill_list.html',{
        'bills':bills,
        'itemlist':itemlist,
        'new_bill_count':new_bill_count})


@login_required
def all_items(request):
    all_items = ItemModel.objects.all()
    user_data = User.objects.get(id=request.user.id)
    new_bill_count = BillModel.objects.filter(accept_status='notaccepted').count()
    return render(request,'all_items.html',{'all_items':all_items,
                                            'new_bill_count':new_bill_count,
                                            'user_data':user_data})

@login_required
def create_order(request):
    if request.method=="POST":
        item_id = request.POST.getlist('item_id') or []
        ordered_item_name = request.POST.getlist('ordered_item_name') or []
        qty = request.POST.getlist('qty') or []
        price = request.POST.getlist('price') or []
        total_price = request.POST.getlist('total_price') or []
        grand_total = float(request.POST.get('grant_total'))

        # validation check1
        if(len(item_id)!=len(ordered_item_name)!=len(qty)!=len(price)!=len(total_price)):
            return JsonResponse({'error':'error'})
        print('validation check1 completed')

        # validation check2
        for i in range(len(item_id)):
            item = ItemModel.objects.get(id=item_id[i])
            tot = int(qty[i])*float(item.prize)
            print(f'{ordered_item_name} {qty[i]} * {float(item.prize)} = {tot}\n {tot}=={total_price[i]}\n {type(tot)}=={type(total_price[i])}')
            if float(tot) != float(total_price[i]):
                return JsonResponse({'error':'error'})
        print('validation check2 completed')

        bill = BillModel(
            user=request.user,
            grand_total= grand_total,
            ordered_time= datetime.now()
        )
        bill.save()
        print("================= [data here] ================")
        for i in range(len(item_id)):
            print(f'{item_id[i]}\t{ordered_item_name[i]}\t{qty[i]}\t{total_price[i]}\t{grand_total}\t')
            item = ItemModel.objects.get(id=item_id[i])
            item_list = ItemlistModel(
                bill = bill,
                name=ordered_item_name[i],
                prize= item.prize,
                qty= int(qty[i]),
                total=float(total_price[i])
            )
            item_list.save()
            print("success")
    return JsonResponse({"success":"order created"})

@login_required
def reject_order(request):
    id = request.POST.get('id')
    bill = BillModel.objects.get(id=id)
    bill.accept_status='rejected'
    bill.reject_reason = request.POST.get('reason') or None
    bill.accept_or_reject_time = None
    bill.save()
    return JsonResponse({'success':'success'})

@login_required
def accept_order(request):
    id = request.POST.get('id')
    bill = BillModel.objects.get(id=id)
    bill.accept_status='accepted'
    bill.accept_or_reject_time = datetime.now()
    bill.save()
    new_time = timedelta(minutes=30,seconds=0)
    bill.expected_delevery_time = bill.accept_or_reject_time + new_time
    bill.save()
    return JsonResponse({'success':'success'})
    
@login_required
def order_ready(request):
    bill = BillModel.objects.get(id=request.POST.get('id'))
    print(bill.ready_status)
    if bill.ready_status == 'notready':
        bill.ready_status = 'ready'
        bill.prepared_time = datetime.now()
        bill.packed_time = datetime.now()
    else:
        bill.prepared_time = None
        bill.packed_time = None
        bill.ready_status = 'notready'
    bill.save()
    print(bill.ready_status)

    return redirect('bill_list')

@login_required
def order_call(request):
    bill = BillModel.objects.get(id=request.POST.get('id'))
    print(bill.called_status)
    if bill.called_status == 'notcalled':
        bill.called_status = 'called'
    # else:
    #     bill.called_status = 'notcalled'
    bill.save()
    print(bill.called_status)

    return redirect('bill_list')

@login_required
def my_order(request):
    user = request.user
    try:
        profile = ProfileModel.objects.get(user=request.user.id)
    except ProfileModel.DoesNotExist:
        return render(request,'curry_shop_my_order.html',{
                                                      'bills':None,
                                                      'itemlist':None,
                                                      'profile':None,
                                                      'user_data':None})
    all_bills = BillModel.objects.filter(user=user).order_by('-ordered_time')
    user_data = User.objects.get(id=request.user.id)
    if profile.order_filter == 'date':
        if profile.order_sort == 'accending':
            bills = all_bills.order_by('ordered_time')
        else:
            bills = all_bills.order_by('-ordered_time')
    else:
        rejected = all_bills.filter(accept_status='rejected')
        delevered = all_bills.filter(delevered_status='delevered').exclude(id__in=rejected)
        bills_except_rejected_and_delivered = all_bills.exclude(accept_status='rejected',delevered_status='delevered').exclude(id__in=delevered).exclude(id__in=rejected)
        if profile.order_sort == 'accending':
            bills = list(bills_except_rejected_and_delivered.order_by('ordered_time'))+list(delevered.order_by('ordered_time'))+list(rejected.order_by('ordered_time'))
        else:
            bills = list(bills_except_rejected_and_delivered.order_by('-ordered_time'))+list(delevered.order_by('-ordered_time'))+list(rejected.order_by('-ordered_time'))
    itemlist = ItemlistModel.objects.filter(bill__in=bills)
    return render(request,'curry_shop_my_order.html',{
                                                      'bills':bills,
                                                      'itemlist':itemlist,
                                                      'profile':profile,
                                                      'user_data':user_data})

def send_otp(request):
    print('send otp view function start')
    number = request.POST.get('phone') or None
    if number:
        number = '+91'+str(number)
        otp = ''.join([ str(random.randint(1,9)) for _ in range(6)])
        acc_id = settings.TWILIO_ACCOUNT_SID
        auth_token = settings.TWILIO_AUTH_TOKEN
        from_phone = settings.TWILIO_PHONE_NUMBER

        client = Client(acc_id,auth_token)

        # message = client.messages.create(
        #     body= f'Your otp is {otp}',
        #     from_=from_phone,
        #     to=number
        # )
        print(otp)

        cache.set(f'otp_here',otp,timeout=500)

        return JsonResponse({"success":"Otp send successfully"})
    
def verify_otp(request):
    if request.method=="POST":
        otp_entered = int(request.POST.get('otp_entered'))
        otp = int(cache.get('otp_here'))
        if otp==otp_entered:
            return JsonResponse({"success":"success"}) 
    return JsonResponse({"error":"error"},status=400) 

@login_required
def dispatch_order(request):
    bill = BillModel.objects.get(id=request.POST.get('id'))
    print(bill.dispatched_status)
    if bill.dispatched_status == 'notdispatched':
        bill.dispatched_status = 'dispatched'
        bill.dispatched_time = datetime.now()
        if not bill.ready_time:
            bill.ready_status = 'ready'
            bill.ready_time = datetime.now()
        if not bill.prepared_time:
            bill.prepared_status = 'prepared'
            bill.prepared_time = datetime.now()
        if not bill.packed_time:
            bill.packed_status = 'packed'
            bill.packed_time = datetime.now()
    else:
        bill.dispatched_status = 'notdispatched'
        bill.dispatched_time = None
    bill.save()
    print(bill.dispatched_status)
    return JsonResponse({'success':'success'})

@login_required
def dispatched_list(request):
    bills = BillModel.objects.filter(dispatched_status='dispatched').exclude(delevered_status='delevered')
    new_bill_count = BillModel.objects.filter(accept_status='notaccepted').count()
    itemlist = ItemlistModel.objects.filter(bill__in=bills)
    return render(request,'curry_shop_dispatched_list.html',{'bills':bills,
                                                             'itemlist':itemlist,
                                                             'new_bill_count':new_bill_count})

@login_required
def delevered_order(request):
    bill = BillModel.objects.get(id=request.POST.get('id'))
    print(bill.delevered_status)
    if bill.delevered_status == 'notdelevered':
        bill.delevered_status = 'delevered'
    else:
        bill.delevered_status = 'notdelevered'
    bill.delevered_time = datetime.now()
    bill.save()
    print(bill.delevered_status)
    return JsonResponse({'success':'success'})

@login_required
def order_history(request):
    bills = BillModel.objects.filter(delevered_status='delevered')
    new_bill_count = BillModel.objects.filter(accept_status='notaccepted').count()
    itemlist = ItemlistModel.objects.filter(bill__in=bills)
    return render(request,'curry_shop_order_history.html',{'bills':bills,
                                                             'itemlist':itemlist,
                                                             'new_bill_count':new_bill_count})

@login_required
def change_filter(request):
    user = request.user.id
    profile = ProfileModel.objects.get(user=user)
    if profile.order_filter == 'date':
        profile.order_filter = 'type'
    else:
        profile.order_filter = 'date'
    profile.save()
    return redirect(request.META.get('HTTP_REFERER','/').replace('http://127.0.0.1:8000/',''))

    
@login_required
def change_sort(request):
    user = request.user.id
    profile = ProfileModel.objects.get(user=user)
    if profile.order_sort == 'accending':
        profile.order_sort = 'deccending'
    else:
        profile.order_sort = 'accending'
    profile.save()
    return redirect(request.META.get('HTTP_REFERER','/').replace('http://127.0.0.1:8000/',''))

@login_required
def get_the_reason(request):
    id = request.POST.get('id')
    bill = BillModel.objects.get(id=id)
    if bill.accept_status == "rejected":
        return JsonResponse({"reject_reason":bill.reject_reason})

@login_required
def my_order_track(request,pk):
    user_data = User.objects.get(id=request.user.id)
    bill = BillModel.objects.get(id=pk)
    profile = ProfileModel.objects.get(user=request.user.id)
    itemlist = ItemlistModel.objects.filter(bill=bill)
    return render(request,'curry_shop_my_order_track.html',{'bill':bill,
                                                            'profile':profile,
                                                            'user_data':user_data,
                                                            'itemlist':itemlist})
@login_required
def update_userdata(request,pk):
    if request.method=="POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        if request.FILES:
            image = request.FILES['image_field']
        else:
            image = ''
        user = User.objects.get(id=pk)
        if user:
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.phone = phone
            user.delivery_address = address
            if image != '':
                user.profile_image = image
            user.save()
            messages.success(request,f'User profile changes has saved.')
    return redirect('profile')