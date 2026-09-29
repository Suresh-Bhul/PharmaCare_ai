(function () {
    var cart = []; // { batchId, medicineId, name, batchNumber, expiryDate, maxQty, unitPrice, quantity }

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            document.cookie.split(';').forEach(function (cookie) {
                cookie = cookie.trim();
                if (cookie.substring(0, name.length + 1) === name + '=') {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                }
            });
        }
        return cookieValue;
    }

    function money(n) {
        return 'Rs. ' + Number(n).toFixed(2);
    }

    function renderResults(medicines) {
        var container = document.getElementById('posResults');
        container.innerHTML = '';
        if (!medicines.length) {
            container.innerHTML = '<div class="col-12 empty-state"><i class="bi bi-emoji-frown"></i>No matching medicines with available stock.</div>';
            return;
        }
        medicines.forEach(function (m) {
            var batch = m.batches[0]; // FEFO: earliest-expiring batch first
            var col = document.createElement('div');
            col.className = 'col-md-6 col-xl-4';
            col.innerHTML =
                '<div class="pos-product-card" data-medicine-id="' + m.id + '" data-batch-id="' + batch.id + '">' +
                    '<div class="d-flex justify-content-between">' +
                        '<div>' +
                            '<div class="fw-semibold">' + m.name + '</div>' +
                            '<div class="text-muted small">' + m.dosage_form + (m.strength ? ' &middot; ' + m.strength : '') + '</div>' +
                        '</div>' +
                        '<div class="text-end"><div class="fw-bold">' + money(batch.selling_price) + '</div></div>' +
                    '</div>' +
                    '<div class="d-flex justify-content-between mt-2 small text-muted">' +
                        '<span>Batch #' + batch.batch_number + '</span>' +
                        '<span>Stock: ' + batch.quantity + '</span>' +
                    '</div>' +
                '</div>';
            col.querySelector('.pos-product-card').addEventListener('click', function () {
                addToCart(m, batch);
            });
            container.appendChild(col);
        });
    }

    function search(term) {
        fetch(window.POS_URLS.search + '?q=' + encodeURIComponent(term))
            .then(function (r) { return r.json(); })
            .then(function (data) { renderResults(data.results || []); });
    }

    function addToCart(medicine, batch) {
        var existing = cart.find(function (c) { return c.batchId === batch.id; });
        if (existing) {
            if (existing.quantity < batch.quantity) existing.quantity += 1;
        } else {
            cart.push({
                batchId: batch.id,
                medicineId: medicine.id,
                name: medicine.name,
                batchNumber: batch.batch_number,
                expiryDate: batch.expiry_date,
                maxQty: batch.quantity,
                unitPrice: parseFloat(batch.selling_price),
                quantity: 1
            });
        }
        renderCart();
    }

    function renderCart() {
        var container = document.getElementById('posCartItems');
        var checkoutBtn = document.getElementById('posCheckoutBtn');

        if (!cart.length) {
            container.innerHTML = '<div class="empty-state py-4"><i class="bi bi-bag"></i>Cart is empty</div>';
            checkoutBtn.disabled = true;
        } else {
            container.innerHTML = '';
            cart.forEach(function (item, idx) {
                var row = document.createElement('div');
                row.className = 'pos-cart-item';
                row.innerHTML =
                    '<div>' +
                        '<div class="fw-semibold">' + item.name + '</div>' +
                        '<div class="text-muted small">' + money(item.unitPrice) + ' &times; ' +
                        '<input type="number" class="qty-input form-control form-control-sm d-inline-block" min="1" max="' + item.maxQty + '" value="' + item.quantity + '" data-idx="' + idx + '">' +
                        '</div>' +
                    '</div>' +
                    '<div class="text-end">' +
                        '<div class="fw-semibold">' + money(item.unitPrice * item.quantity) + '</div>' +
                        '<button class="btn btn-sm btn-link text-danger p-0" data-remove="' + idx + '">Remove</button>' +
                    '</div>';
                container.appendChild(row);
            });
            checkoutBtn.disabled = false;

            container.querySelectorAll('.qty-input').forEach(function (input) {
                input.addEventListener('change', function () {
                    var idx = parseInt(input.getAttribute('data-idx'), 10);
                    var val = Math.max(1, Math.min(parseInt(input.value || '1', 10), cart[idx].maxQty));
                    cart[idx].quantity = val;
                    renderCart();
                });
            });
            container.querySelectorAll('[data-remove]').forEach(function (btn) {
                btn.addEventListener('click', function () {
                    cart.splice(parseInt(btn.getAttribute('data-remove'), 10), 1);
                    renderCart();
                });
            });
        }

        updateTotals();
    }

    function updateTotals() {
        var subTotal = cart.reduce(function (sum, item) { return sum + item.unitPrice * item.quantity; }, 0);
        var discount = parseFloat(document.getElementById('posDiscount').value || '0');
        var total = Math.max(0, subTotal - discount);
        document.getElementById('posSubTotal').textContent = money(subTotal);
        document.getElementById('posTotal').textContent = money(total);
    }

    function showError(msg) {
        var box = document.getElementById('posError');
        box.textContent = msg;
        box.classList.remove('d-none');
    }
    function clearError() {
        document.getElementById('posError').classList.add('d-none');
    }

    function checkout() {
        clearError();
        var customerId = document.getElementById('posCustomer').value;
        if (!customerId) { showError('Please select a patient before checking out.'); return; }
        if (!cart.length) { showError('Cart is empty.'); return; }

        var payload = {
            customer_id: customerId,
            payment_method: document.getElementById('posPaymentMethod').value,
            discount: document.getElementById('posDiscount').value || '0',
            items: cart.map(function (item) {
                return { batch_id: item.batchId, quantity: item.quantity };
            })
        };

        var btn = document.getElementById('posCheckoutBtn');
        btn.disabled = true;
        btn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Processing...';

        fetch(window.POS_URLS.checkout, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(payload)
        })
        .then(function (r) { return r.json(); })
        .then(function (data) {
            if (data.success) {
                window.location.href = data.payment_url || data.redirect_url;
            } else {
                showError(data.error || 'Could not complete the sale.');
                btn.disabled = false;
                btn.innerHTML = '<i class="bi bi-check-circle"></i> Complete Sale';
            }
        })
        .catch(function () {
            showError('Network error. Please try again.');
            btn.disabled = false;
            btn.innerHTML = '<i class="bi bi-check-circle"></i> Complete Sale';
        });
    }

    document.addEventListener('DOMContentLoaded', function () {
        var searchInput = document.getElementById('posSearch');
        var debounceTimer;
        searchInput.addEventListener('keyup', function () {
            clearTimeout(debounceTimer);
            var term = searchInput.value.trim();
            debounceTimer = setTimeout(function () { search(term); }, 300);
        });
        search('');

        document.getElementById('posDiscount').addEventListener('input', updateTotals);
        document.getElementById('posCheckoutBtn').addEventListener('click', checkout);
    });
})();
