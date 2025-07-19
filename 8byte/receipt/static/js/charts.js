document.addEventListener('DOMContentLoaded', () => {
    // Ensure upload button is visible initially
    const uploadButton = document.getElementById('upload-button');
    const uploadText = document.getElementById('upload-text');
    const uploadSpinner = document.getElementById('upload-spinner');
    if (uploadButton) {
        uploadButton.style.display = 'inline-flex';
        uploadText.classList.remove('hidden');
        uploadSpinner.classList.add('hidden');
    }

    // Vendor Distribution Chart
    const vendorData = {{ aggregates.vendor_distribution|safe }};
    new Chart(document.getElementById('vendorChart'), {
        type: 'bar',
        data: {
            labels: Object.keys(vendorData),
            datasets: [{
                label: 'Vendor Frequency',
                data: Object.values(vendorData),
                backgroundColor: 'rgba(59, 130, 246, 0.5)',
                borderColor: 'rgba(59, 130, 246, 1)',
                borderWidth: 1
            }]
        },
        options: {
            animation: {
                duration: 1000,
                easing: 'easeInOutQuad'
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Number of Receipts'
                    }
                }
            }
        }
    });

    // Monthly Trend Chart
    const trendData = {{ aggregates.monthly_trend|safe }};
    new Chart(document.getElementById('trendChart'), {
        type: 'line',
        data: {
            labels: Object.keys(trendData),
            datasets: [{
                label: 'Monthly Spend',
                data: Object.values(trendData),
                fill: false,
                borderColor: 'rgb(59, 130, 246)',
                tension: 0.1
            }]
        },
        options: {
            animation: {
                duration: 1000,
                easing: 'easeInOutQuad'
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Spend ($)'
                    }
                }
            }
        }
    });

    // Search Functionality
    const searchInput = document.getElementById('search');
    const sortSelect = document.getElementById('sort');
    const receiptsTable = document.getElementById('receipts-table');
    
    if (searchInput && receiptsTable) {
        searchInput.addEventListener('input', () => {
            const query = searchInput.value.toLowerCase();
            const rows = receiptsTable.getElementsByTagName('tr');
            for (let row of rows) {
                const vendor = row.cells[0]?.textContent.toLowerCase() || '';
                const category = row.cells[3]?.textContent.toLowerCase() || '';
                row.style.display = (vendor.includes(query) || category.includes(query)) ? '' : 'none';
            }
        });
    }

    // Sort Functionality (client-side for demo purposes)
    if (sortSelect && receiptsTable) {
        sortSelect.addEventListener('change', () => {
            const sortKey = sortSelect.value;
            const rows = Array.from(receiptsTable.getElementsByTagName('tr'));
            rows.sort((a, b) => {
                let aValue, bValue;
                if (sortKey === 'amount') {
                    aValue = parseFloat(a.cells[2].textContent.replace('$', '')) || 0;
                    bValue = parseFloat(b.cells[2].textContent.replace('$', '')) || 0;
                } else if (sortKey === 'date') {
                    aValue = new Date(a.cells[1].textContent);
                    bValue = new Date(b.cells[1].textContent);
                } else {
                    aValue = a.cells[0].textContent.toLowerCase();
                    bValue = b.cells[0].textContent.toLowerCase();
                }
                return aValue > bValue ? 1 : -1;
            });
            receiptsTable.innerHTML = '';
            rows.forEach(row => receiptsTable.appendChild(row));
        });
    }

    // Form Submission with Loading Spinner
    const uploadForm = document.getElementById('upload-form');
    if (uploadForm && uploadButton) {
        uploadForm.addEventListener('submit', (e) => {
            const fileInput = document.getElementById('file');
            if (!fileInput.value) {
                e.preventDefault();
                alert('Please select a file to upload.');
                return;
            }
            uploadText.classList.add('hidden');
            uploadSpinner.classList.remove('hidden');
            uploadButton.disabled = true;
        });
    }
});