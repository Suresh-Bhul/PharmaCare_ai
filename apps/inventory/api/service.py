from apps.inventory.models import InventoryTxn


def create_inventory_txn(**kwargs):
    batch = kwargs.get('batch')
    transaction_type = kwargs.get('transaction_type')
    quantity = kwargs.get('quantity')
    reference_id=kwargs.get('reference_id')
    previous_stock = kwargs.get('previous_stock')
    new_stock = kwargs.get('new_stock')

    inv = InventoryTxn.objects.create(
        batch = batch,
        transaction_type = transaction_type,
        quantity = quantity,
        reference_id=reference_id,
        previous_stock = previous_stock,
        new_stock =  new_stock,
    )
    return inv


