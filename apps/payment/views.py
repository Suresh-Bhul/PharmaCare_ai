from django.shortcuts import render, get_object_or_404

from apps.inventory.api.service import create_inventory_txn
from apps.inventory.models import TransactionType
from apps.payment.models import PaymentLog, PaymentStatus 
from apps.sales.models import PaymentStatus as SalePaymentStatus, Sales, SalesItem

# Create your views here.
def payment_callback(request):
    data = request.GET
    payment = get_object_or_404(PaymentLog, pidx=data['pidx'])
    sale = get_object_or_404(Sales, id=data['purchase_order_id'])
    if data['status'] == "Completed":
        payment.status = PaymentStatus.COMPLETED
        payment.transaction_id = data['transaction_id']
        sale.payment_status = SalePaymentStatus.PAID
        
        payment.save()
        sale.save()

        sales_item = SalesItem.objects.filter(sale=sale)
        for item in sales_item:
            create_inventory_txn(
                batch = item.batch,
                transaction_type = TransactionType.SALE,
                quantity = item.quantity,
                reference_id = item.id,
                previous_stock = item.batch.quantity,
                new_stock = item.batch.quantity - item.quantity,
            )
            item.batch.quantity -= item.quantity
            item.batch.save()    
    else:
        payment.status = PaymentStatus.FAILED
        sale.payment_status = SalePaymentStatus.FAILED
        sale.save()
        payment.save()

    context = {
        "data": request.GET
    }
    return render(request, 'payment/callback.html/', context)
   