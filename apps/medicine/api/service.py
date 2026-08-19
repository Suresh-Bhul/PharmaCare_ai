from apps.inventory.api.service import create_inventory_txn
from apps.inventory.models import TransactionType
from apps.medicine.models import MedicineBatch


def create_medicine_batch(**kwargs):
    medicine = kwargs.get('medicine')
    batch_number = kwargs.get('batch_number')
    manufacturing_date = kwargs.get('manufacturing_date')
    expiry_date = kwargs.get('expiry_date')
    quantity = kwargs.get('quantity')
    purchase_price = kwargs.get('purchase_price')
    selling_price = kwargs.get('selling_price')
    supplier = kwargs.get('supplier')
    received_date = kwargs.get('received_date', '2023-01-07')

    data = MedicineBatch.objects.create(
        medicine = medicine,
        batch_number = batch_number,
        manufacturing_date = manufacturing_date,
        expiry_date = expiry_date,
        quantity = quantity,
        purchase_price = purchase_price,
        selling_price = selling_price,
        supplier = supplier,
        received_date = received_date,
        status = True
    )
    create_inventory_txn(
        batch = data,
        transaction_type = TransactionType.PURCHASE,
        quantity = quantity,
        reference_id = f'Ref-{supplier.company_name[:4]}-MB{data.id}',
        previous_stock = 0,
        new_stock =  quantity,
    )
    return data