document.addEventListener('DOMContentLoaded', function () {
    // Sidebar toggle (mobile)
    var toggleBtn = document.getElementById('sidebarToggle');
    var sidebar = document.getElementById('sidebar');
    if (toggleBtn && sidebar) {
        toggleBtn.addEventListener('click', function () {
            sidebar.classList.toggle('show');
        });
        document.addEventListener('click', function (e) {
            if (window.innerWidth < 992 && sidebar.classList.contains('show') &&
                !sidebar.contains(e.target) && e.target !== toggleBtn) {
                sidebar.classList.remove('show');
            }
        });
    }

    // Auto-dismiss alerts after 5s
    document.querySelectorAll('.messages-wrapper .alert').forEach(function (el) {
        setTimeout(function () {
            var bsAlert = bootstrap.Alert.getOrCreateInstance(el);
            bsAlert.close();
        }, 5000);
    });

    // Generic "confirm before delete" for any form/link with data-confirm
    document.querySelectorAll('[data-confirm]').forEach(function (el) {
        el.addEventListener('click', function (e) {
            if (!confirm(el.getAttribute('data-confirm') || 'Are you sure?')) {
                e.preventDefault();
            }
        });
    });

    // Client-side search filter for simple tables: <input data-table-search="tableId">
    document.querySelectorAll('[data-table-search]').forEach(function (input) {
        var table = document.getElementById(input.getAttribute('data-table-search'));
        if (!table) return;
        input.addEventListener('keyup', function () {
            var term = input.value.toLowerCase();
            table.querySelectorAll('tbody tr').forEach(function (row) {
                row.style.display = row.textContent.toLowerCase().indexOf(term) > -1 ? '' : 'none';
            });
        });
    });
});
