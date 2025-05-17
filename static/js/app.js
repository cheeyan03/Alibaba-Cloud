// Main JavaScript functionality for FinTrack application

document.addEventListener('DOMContentLoaded', function() {
    // Initialize modals
    initModals();
    
    // Initialize transaction form
    initTransactionForm();
    
    // Initialize currency converter
    initCurrencyConverter();
    
    // Initialize dropdown menus
    initDropdowns();
    
    // Initialize settings page
    initSettingsPage();
    
    // Initialize dashboard
    initDashboard();
    
    // Initialize data export/import
    initDataExportImport();
    
    // Initialize tax calculator
    initTaxCalculator();
});

// ============ Modal Functionality ============
function initModals() {
    // Get all modal trigger buttons
    const modalTriggers = {
        'addTransactionBtn': 'transactionModal',
        'uploadReceiptBtn': 'receiptModal'
    };
    
    // Add event listeners to modal triggers
    for (const [triggerId, modalId] of Object.entries(modalTriggers)) {
        const triggerBtn = document.getElementById(triggerId);
        const modal = document.getElementById(modalId);
        
        if (triggerBtn && modal) {
            triggerBtn.addEventListener('click', () => {
                openModal(modal);
            });
            
            // Add close button functionality
            const closeBtn = modal.querySelector('.modal-close');
            const cancelBtn = modal.querySelector('.modal-cancel');
            
            if (closeBtn) {
                closeBtn.addEventListener('click', () => {
                    closeModal(modal);
                });
            }
            
            if (cancelBtn) {
                cancelBtn.addEventListener('click', () => {
                    closeModal(modal);
                });
            }
        }
    }
    
    // Close modal when clicking outside
    window.addEventListener('click', (e) => {
        if (e.target.classList.contains('modal')) {
            closeModal(e.target);
        }
    });
}

function openModal(modal) {
    if (modal) {
        modal.style.display = 'flex';
        document.body.style.overflow = 'hidden'; // Prevent background scrolling
    }
}

function closeModal(modal) {
    if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto'; // Restore scrolling
    }
}

// ============ Transaction Form Functionality ============
function initTransactionForm() {
    const transactionForm = document.querySelector('#transactionModal');
    if (!transactionForm) return;
    
    // Toggle between income and expense
    const toggleBtns = transactionForm.querySelectorAll('.toggle-btn');
    toggleBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            toggleBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            // Update form fields based on type
            const type = btn.dataset.type;
            updateFormForType(type);
        });
    });
    
    // File input preview for receipt
    const fileInput = transactionForm.querySelector('#transaction-receipt');
    if (fileInput) {
        fileInput.addEventListener('change', handleFileSelect);
    }
    
    // Save transaction
    const saveBtn = transactionForm.querySelector('.modal-save');
    if (saveBtn) {
        saveBtn.addEventListener('click', () => {
            saveTransaction();
            closeModal(transactionForm);
        });
    }
}

function updateFormForType(type) {
    const categorySelect = document.getElementById('transaction-category');
    const taxStatusSelect = document.getElementById('transaction-tax-status');
    
    if (!categorySelect || !taxStatusSelect) return;
    
    // Update category options based on type
    if (type === 'income') {
        // Update tax status options for income
        clearOptions(taxStatusSelect);
        addOption(taxStatusSelect, 'taxable', 'Taxable Income');
        addOption(taxStatusSelect, 'non-taxable', 'Non-Taxable Income');
        
        // Update category options for income
        clearOptions(categorySelect);
        addOption(categorySelect, '', 'Select a category');
        addOption(categorySelect, 'development', 'Development');
        addOption(categorySelect, 'design', 'Design');
        addOption(categorySelect, 'consulting', 'Consulting');
        addOption(categorySelect, 'writing', 'Content Writing');
        addOption(categorySelect, 'other-income', 'Other Income');
    } else {
        // Update tax status options for expense
        clearOptions(taxStatusSelect);
        addOption(taxStatusSelect, 'deductible', 'Tax Deductible Expense');
        addOption(taxStatusSelect, 'non-deductible', 'Non-Deductible Expense');
        
        // Update category options for expense
        clearOptions(categorySelect);
        addOption(categorySelect, '', 'Select a category');
        addOption(categorySelect, 'software', 'Software');
        addOption(categorySelect, 'equipment', 'Equipment');
        addOption(categorySelect, 'travel', 'Travel');
        addOption(categorySelect, 'office', 'Office');
        addOption(categorySelect, 'professional', 'Professional Services');
        addOption(categorySelect, 'utilities', 'Utilities');
    }
}

function clearOptions(selectElement) {
    while (selectElement.options.length > 0) {
        selectElement.remove(0);
    }
}

function addOption(selectElement, value, text) {
    const option = document.createElement('option');
    option.value = value;
    option.textContent = text;
    selectElement.add(option);
}

function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
        // File preview container
        const preview = document.getElementById('receipt-preview');
        if (preview) {
            // Clear previous preview
            preview.innerHTML = '';
            
            // Show loading state
            const loadingMsg = document.createElement('div');
            loadingMsg.classList.add('upload-status');
            loadingMsg.textContent = 'Processing receipt...';
            preview.appendChild(loadingMsg);
            
            const reader = new FileReader();
            reader.onload = function(e) {
                // Create image preview
                const img = document.createElement('img');
                img.src = e.target.result;
                img.classList.add('receipt-thumbnail');
                
                // Replace loading message with image
                preview.innerHTML = '';
                preview.appendChild(img);
                
                // In a real app, you would send the file to the server for OCR processing
                setTimeout(() => {
                    // Simulate OCR processing result with extracted data
                    extractReceiptData(file);
                }, 1500);
            };
            
            reader.readAsDataURL(file);
        }
        
        console.log('File selected:', file.name, file.type, file.size);
    }
}

function extractReceiptData(file) {
    // In a real app, this data would come from the server after OCR processing
    // This is a simulation of extracted data
    const mockExtractedData = {
        vendor: 'Tech Store',
        date: '2023-11-15',
        amount: '299.99',
        currency: 'USD',
        items: [
            { name: 'Wireless Keyboard', price: '89.99' },
            { name: 'Mouse', price: '59.99' },
            { name: 'Monitor Stand', price: '150.01' }
        ],
        taxAmount: '18.00'
    };
    
    // Populate the transaction form with the extracted data
    populateTransactionFormFromReceipt(mockExtractedData);
    
    // Show success notification
    const preview = document.getElementById('receipt-preview');
    if (preview) {
        const successMsg = document.createElement('div');
        successMsg.classList.add('upload-status', 'success');
        successMsg.textContent = 'Receipt processed successfully!';
        preview.appendChild(successMsg);
    }
}

function populateTransactionFormFromReceipt(data) {
    // Find form elements
    const vendorInput = document.getElementById('transaction-client-vendor');
    const dateInput = document.getElementById('transaction-date');
    const amountInput = document.getElementById('transaction-amount');
    const currencySelect = document.getElementById('transaction-currency');
    const descriptionInput = document.getElementById('transaction-description');
    const notesInput = document.getElementById('transaction-notes');
    
    // Set form values based on extracted data
    if (vendorInput) vendorInput.value = data.vendor;
    if (dateInput) dateInput.value = data.date;
    if (amountInput) amountInput.value = data.amount;
    if (currencySelect) currencySelect.value = data.currency;
    if (descriptionInput) descriptionInput.value = `Receipt from ${data.vendor}`;
    
    // Populate notes with item details
    if (notesInput && data.items && data.items.length > 0) {
        let itemsText = 'Items:\n';
        data.items.forEach(item => {
            itemsText += `- ${item.name}: ${item.price}\n`;
        });
        itemsText += `\nTax: ${data.taxAmount}`;
        notesInput.value = itemsText;
    }
    
    // Set transaction type to expense (since receipts are typically for expenses)
    const expenseButton = document.querySelector('.toggle-btn[data-type="expense"]');
    if (expenseButton) {
        // Simulate a click on the expense button
        expenseButton.click();
    }
}

function saveTransaction() {
    // Get form values
    const type = document.querySelector('.toggle-btn.active').dataset.type;
    const date = document.getElementById('transaction-date').value;
    const amount = document.getElementById('transaction-amount').value;
    const currency = document.getElementById('transaction-currency').value;
    const description = document.getElementById('transaction-description').value;
    const category = document.getElementById('transaction-category').value;
    const clientVendor = document.getElementById('transaction-client-vendor').value;
    const taxStatus = document.getElementById('transaction-tax-status').value;
    const notes = document.getElementById('transaction-notes').value;
    
    // Create transaction object
    const transaction = {
        type,
        date,
        amount,
        currency,
        description,
        category,
        clientVendor,
        taxStatus,
        notes,
        createdAt: new Date().toISOString()
    };
    
    // In a real app, you would save this to a database
    // For this demo, we just log the transaction
    console.log('Transaction saved:', transaction);
    
    // Reset form
    document.getElementById('transactionModal').reset();
    
    // Show success message (in a real app)
    alert('Transaction saved successfully!');
}

// ============ Currency Converter Functionality ============
function initCurrencyConverter() {
    const converterForm = document.querySelector('.converter-form');
    if (!converterForm) return;
    
    // Get form elements
    const amountInput = document.getElementById('amount');
    const fromCurrency = document.getElementById('from-currency');
    const toCurrency = document.getElementById('to-currency');
    const swapButton = document.querySelector('.currency-swap');
    
    // Add event listeners
    if (amountInput && fromCurrency && toCurrency) {
        amountInput.addEventListener('input', updateConversion);
        fromCurrency.addEventListener('change', updateConversion);
        toCurrency.addEventListener('change', updateConversion);
    }
    
    if (swapButton) {
        swapButton.addEventListener('click', swapCurrencies);
    }
    
    // Initial conversion
    updateConversion();
}

function swapCurrencies() {
    const fromCurrency = document.getElementById('from-currency');
    const toCurrency = document.getElementById('to-currency');
    
    if (!fromCurrency || !toCurrency) return;
    
    const tempValue = fromCurrency.value;
    fromCurrency.value = toCurrency.value;
    toCurrency.value = tempValue;
    
    updateConversion();
}

function updateConversion() {
    const amountInput = document.getElementById('amount');
    const fromCurrency = document.getElementById('from-currency');
    const toCurrency = document.getElementById('to-currency');
    const conversionValue = document.querySelector('.conversion-value');
    const conversionRate = document.querySelector('.conversion-rate');
    
    if (!amountInput || !fromCurrency || !toCurrency || !conversionValue || !conversionRate) return;
    
    const amount = parseFloat(amountInput.value) || 0;
    const from = fromCurrency.value;
    const to = toCurrency.value;
    
    // In a real app, you would fetch exchange rates from an API
    // For this demo, we use hardcoded rates
    const rates = {
        'USD': { 'MYR': 4.20, 'EUR': 0.93, 'GBP': 0.79, 'SGD': 1.35 },
        'MYR': { 'USD': 0.24, 'EUR': 0.22, 'GBP': 0.19, 'SGD': 0.32 },
        'EUR': { 'USD': 1.08, 'MYR': 4.95, 'GBP': 0.86, 'SGD': 1.46 },
        'GBP': { 'USD': 1.26, 'MYR': 5.80, 'EUR': 1.17, 'SGD': 1.70 },
        'SGD': { 'USD': 0.74, 'MYR': 3.40, 'EUR': 0.68, 'GBP': 0.59 }
    };
    
    let rate;
    
    // If same currency, rate is 1
    if (from === to) {
        rate = 1;
    } else {
        // Get rate from our rates object
        rate = rates[from] && rates[from][to] ? rates[from][to] : 0;
    }
    
    const convertedAmount = amount * rate;
    
    // Format the currencies for display
    const currencySymbols = {
        'USD': '$',
        'MYR': 'RM',
        'EUR': '€',
        'GBP': '£',
        'SGD': 'S$'
    };
    
    const fromSymbol = currencySymbols[from] || from;
    const toSymbol = currencySymbols[to] || to;
    
    // Format the numbers with commas
    const formattedAmount = amount.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    const formattedConverted = convertedAmount.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    
    // Update the UI
    conversionValue.textContent = `${fromSymbol} ${formattedAmount} = ${toSymbol} ${formattedConverted}`;
    conversionRate.textContent = `1 ${from} = ${rate.toFixed(4)} ${to}`;
}

// ============ Dropdown Menu Functionality ============
function initDropdowns() {
    // Get all dropdown elements
    const dropdowns = document.querySelectorAll('.dropdown');
    
    dropdowns.forEach(dropdown => {
        const trigger = dropdown.querySelector('.dropdown-trigger');
        const menu = dropdown.querySelector('.dropdown-menu');
        
        if (trigger && menu) {
            // Toggle dropdown on click
            trigger.addEventListener('click', (e) => {
                e.stopPropagation();
                
                // Close any open dropdowns first
                document.querySelectorAll('.dropdown-menu.active').forEach(openMenu => {
                    if (openMenu !== menu) {
                        openMenu.classList.remove('active');
                    }
                });
                
                // Toggle current dropdown
                menu.classList.toggle('active');
            });
            
            // Handle dropdown item clicks
            const items = menu.querySelectorAll('.dropdown-item');
            items.forEach(item => {
                item.addEventListener('click', () => {
                    // Update trigger text if it has a value property
                    if (item.dataset.value) {
                        const display = trigger.querySelector('.dropdown-display');
                        if (display) {
                            display.textContent = item.textContent;
                            display.dataset.value = item.dataset.value;
                        }
                    }
                    
                    // Execute custom action if provided
                    if (item.dataset.action) {
                        // Execute the function specified in data-action
                        const actionFunction = window[item.dataset.action];
                        if (typeof actionFunction === 'function') {
                            actionFunction();
                        }
                    }
                    
                    // Close the dropdown
                    menu.classList.remove('active');
                });
            });
        }
    });
    
    // Close dropdowns when clicking outside
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.dropdown')) {
            document.querySelectorAll('.dropdown-menu.active').forEach(menu => {
                menu.classList.remove('active');
            });
        }
    });
}

// ============ Settings Page Functionality ============
function initSettingsPage() {
    const settingsPage = document.querySelector('.settings-content');
    if (!settingsPage) return;
    
    // Settings navigation
    const menuItems = document.querySelectorAll('.settings-menu-item');
    const panels = document.querySelectorAll('.settings-panel');
    
    menuItems.forEach(item => {
        item.addEventListener('click', () => {
            const targetId = item.dataset.target;
            
            // Update active menu item
            menuItems.forEach(mi => mi.classList.remove('active'));
            item.classList.add('active');
            
            // Show target panel
            panels.forEach(panel => {
                panel.classList.remove('active');
                if (panel.id === targetId) {
                    panel.classList.add('active');
                }
            });
        });
    });
    
    // Dark mode toggle
    const darkModeToggle = document.getElementById('dark-mode-toggle');
    if (darkModeToggle) {
        // Check if dark mode is already enabled
        if (localStorage.getItem('darkMode') === 'enabled') {
            document.body.classList.add('dark-mode');
            darkModeToggle.checked = true;
        }
        
        darkModeToggle.addEventListener('change', () => {
            if (darkModeToggle.checked) {
                document.body.classList.add('dark-mode');
                localStorage.setItem('darkMode', 'enabled');
            } else {
                document.body.classList.remove('dark-mode');
                localStorage.setItem('darkMode', 'disabled');
            }
        });
    }
    
    // Save settings button
    const saveSettingsBtn = document.getElementById('saveSettingsBtn');
    if (saveSettingsBtn) {
        saveSettingsBtn.addEventListener('click', () => {
            saveSettings();
        });
    }
    
    // Profile image upload
    const profileImage = document.querySelector('.profile-image');
    if (profileImage) {
        profileImage.addEventListener('click', () => {
            // Create a file input element
            const fileInput = document.createElement('input');
            fileInput.type = 'file';
            fileInput.accept = 'image/*';
            fileInput.style.display = 'none';
            
            // Append to body and trigger click
            document.body.appendChild(fileInput);
            fileInput.click();
            
            // Handle file selection
            fileInput.addEventListener('change', (e) => {
                const file = e.target.files[0];
                if (file) {
                    const reader = new FileReader();
                    reader.onload = (event) => {
                        // In a real app, you'd upload the image to a server
                        // For this demo, we just update the image source
                        const img = profileImage.querySelector('img');
                        if (img) {
                            img.src = event.target.result;
                        }
                    };
                    reader.readAsDataURL(file);
                }
                
                // Remove the input element
                document.body.removeChild(fileInput);
            });
        });
    }
}

function saveSettings() {
    // Collect all settings values
    const settings = {
        profile: {
            displayName: document.getElementById('display-name')?.value,
            role: document.getElementById('user-role')?.value,
            email: document.getElementById('email')?.value,
            phone: document.getElementById('phone')?.value,
            language: document.getElementById('language')?.value
        },
        preferences: {
            darkMode: document.getElementById('dark-mode-toggle')?.checked,
            defaultView: document.querySelector('#preferences select')?.value,
            dateFormat: document.querySelector('[value="dd-mm-yyyy"]')?.parentElement?.value,
            autoSave: document.getElementById('autosave-toggle')?.checked
        },
        notifications: {
            email: document.getElementById('email-notifications')?.checked,
            browser: document.getElementById('browser-notifications')?.checked,
            tax: document.getElementById('tax-reminders')?.checked,
            invoice: document.getElementById('invoice-reminders')?.checked,
            reports: document.getElementById('report-notifications')?.checked
        },
        tax: {
            taxId: document.getElementById('tax-id')?.value,
            businessType: document.getElementById('business-type')?.value,
            fiscalYear: document.getElementById('fiscal-year')?.value,
            threshold: document.getElementById('tax-threshold')?.value
        },
        currency: {
            primary: document.getElementById('primary-currency')?.value,
            provider: document.getElementById('exchange-provider')?.value,
            updateFrequency: document.getElementById('update-frequency')?.value,
            active: getActiveCurrencies()
        }
    };
    
    // In a real app, you'd send this to a server
    // For this demo, we just save to localStorage
    localStorage.setItem('fintrackSettings', JSON.stringify(settings));
    
    // Show success message
    alert('Settings saved successfully!');
    
    // Log the settings object
    console.log('Settings saved:', settings);
}

function getActiveCurrencies() {
    const activeCurrencies = [];
    const currencyCheckboxes = document.querySelectorAll('[id^="currency-"]');
    
    currencyCheckboxes.forEach(checkbox => {
        if (checkbox.checked) {
            // Extract currency code from the ID (e.g., "currency-usd" -> "usd")
            const currencyCode = checkbox.id.split('-')[1];
            activeCurrencies.push(currencyCode);
        }
    });
    
    return activeCurrencies;
}

// ============ Dashboard & Data Visualization Functionality ============
function initDashboard() {
    // Initialize dashboard elements when the dashboard page loads
    const dashboard = document.querySelector('.dashboard-content');
    if (!dashboard) return;
    
    // Initialize charts
    initIncomeExpenseChart();
    initCategoryDistributionChart();
    initBalanceTrendChart();
    
    // Initialize summary cards
    updateSummaryCards();
    
    // Initialize recent transactions table
    loadRecentTransactions();
    
    // Initialize reminder notifications
    loadReminders();
}

function initIncomeExpenseChart() {
    const chartContainer = document.getElementById('income-expense-chart');
    if (!chartContainer) return;
    
    // Sample data - in a real app, this would come from an API or database
    const monthlyData = {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        income: [3500, 4200, 3800, 5100, 4700, 6200],
        expenses: [2800, 3100, 2700, 3400, 3200, 3800]
    };
    
    // Create chart using chart.js or any other library
    // This is a placeholder for the actual chart creation
    console.log('Income/Expense chart initialized with data:', monthlyData);
    
    // In a real implementation, you would use a library like Chart.js:
    /*
    new Chart(chartContainer.getContext('2d'), {
        type: 'bar',
        data: {
            labels: monthlyData.labels,
            datasets: [
                {
                    label: 'Income',
                    data: monthlyData.income,
                    backgroundColor: '#4CAF50'
                },
                {
                    label: 'Expenses',
                    data: monthlyData.expenses,
                    backgroundColor: '#F44336'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
    */
}

function initCategoryDistributionChart() {
    const chartContainer = document.getElementById('category-distribution-chart');
    if (!chartContainer) return;
    
    // Sample data for category distribution
    const categoryData = {
        labels: ['Software', 'Equipment', 'Travel', 'Office', 'Professional', 'Utilities'],
        values: [25, 30, 15, 10, 15, 5],
        colors: ['#4CAF50', '#2196F3', '#FF9800', '#9C27B0', '#607D8B', '#E91E63']
    };
    
    // Create chart using chart.js or any other library
    console.log('Category distribution chart initialized with data:', categoryData);
    
    // In a real implementation, you would use a library like Chart.js:
    /*
    new Chart(chartContainer.getContext('2d'), {
        type: 'pie',
        data: {
            labels: categoryData.labels,
            datasets: [
                {
                    data: categoryData.values,
                    backgroundColor: categoryData.colors
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right'
                }
            }
        }
    });
    */
}

function initBalanceTrendChart() {
    const chartContainer = document.getElementById('balance-trend-chart');
    if (!chartContainer) return;
    
    // Sample data for balance trend
    const trendData = {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        balance: [1200, 2300, 3400, 5100, 6600, 9000]
    };
    
    // Create chart using chart.js or any other library
    console.log('Balance trend chart initialized with data:', trendData);
    
    // In a real implementation, you would use a library like Chart.js:
    /*
    new Chart(chartContainer.getContext('2d'), {
        type: 'line',
        data: {
            labels: trendData.labels,
            datasets: [
                {
                    label: 'Account Balance',
                    data: trendData.balance,
                    fill: false,
                    borderColor: '#3f51b5',
                    tension: 0.1
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });
    */
}

function updateSummaryCards() {
    // Update summary cards with latest data
    const totalIncomeEl = document.getElementById('total-income');
    const totalExpensesEl = document.getElementById('total-expenses');
    const netSavingsEl = document.getElementById('net-savings');
    const savingsRateEl = document.getElementById('savings-rate');
    
    // Sample data - in a real app, this would come from calculations on actual data
    const summaryData = {
        totalIncome: 12800,
        totalExpenses: 8500,
        netSavings: 4300,
        savingsRate: 33.6
    };
    
    // Update the UI elements if they exist
    if (totalIncomeEl) totalIncomeEl.textContent = formatCurrency(summaryData.totalIncome);
    if (totalExpensesEl) totalExpensesEl.textContent = formatCurrency(summaryData.totalExpenses);
    if (netSavingsEl) netSavingsEl.textContent = formatCurrency(summaryData.netSavings);
    if (savingsRateEl) savingsRateEl.textContent = `${summaryData.savingsRate}%`;
}

function loadRecentTransactions() {
    const transactionsTable = document.querySelector('.recent-transactions-table tbody');
    if (!transactionsTable) return;
    
    // Sample transactions data - in a real app, this would come from an API or database
    const recentTransactions = [
        { date: '2023-11-20', description: 'Client Payment - XYZ Corp', category: 'Development', amount: 2500, type: 'income' },
        { date: '2023-11-18', description: 'Web Hosting Service', category: 'Software', amount: 29.99, type: 'expense' },
        { date: '2023-11-15', description: 'Office Supplies', category: 'Office', amount: 125.30, type: 'expense' },
        { date: '2023-11-12', description: 'Client Payment - ABC Inc', category: 'Consulting', amount: 1800, type: 'income' },
        { date: '2023-11-10', description: 'Monthly Internet', category: 'Utilities', amount: 89.99, type: 'expense' }
    ];
    
    // Clear existing rows
    transactionsTable.innerHTML = '';
    
    // Add transaction rows
    recentTransactions.forEach(transaction => {
        const row = document.createElement('tr');
        row.className = transaction.type === 'income' ? 'income-row' : 'expense-row';
        
        // Format the date
        const date = new Date(transaction.date);
        const formattedDate = date.toLocaleDateString('en-US', { 
            year: 'numeric', 
            month: 'short', 
            day: 'numeric' 
        });
        
        row.innerHTML = `
            <td>${formattedDate}</td>
            <td>${transaction.description}</td>
            <td>${transaction.category}</td>
            <td class="${transaction.type}-amount">${transaction.type === 'income' ? '+' : '-'} ${formatCurrency(transaction.amount)}</td>
            <td class="actions">
                <button class="action-btn edit-btn" title="Edit Transaction">
                    <i class="fas fa-edit"></i>
                </button>
                <button class="action-btn delete-btn" title="Delete Transaction">
                    <i class="fas fa-trash"></i>
                </button>
            </td>
        `;
        
        // Add click handlers for edit and delete buttons
        const editBtn = row.querySelector('.edit-btn');
        const deleteBtn = row.querySelector('.delete-btn');
        
        if (editBtn) {
            editBtn.addEventListener('click', () => {
                editTransaction(transaction);
            });
        }
        
        if (deleteBtn) {
            deleteBtn.addEventListener('click', () => {
                if (confirm('Are you sure you want to delete this transaction?')) {
                    deleteTransaction(transaction);
                    row.remove();
                }
            });
        }
        
        transactionsTable.appendChild(row);
    });
}

function loadReminders() {
    const remindersContainer = document.querySelector('.reminders-list');
    if (!remindersContainer) return;
    
    // Sample reminder data
    const reminders = [
        { id: 1, title: 'Quarterly Tax Payment', due: '2023-12-15', priority: 'high' },
        { id: 2, title: 'Client Invoice #1234', due: '2023-11-30', priority: 'medium' },
        { id: 3, title: 'Renew Business License', due: '2024-01-10', priority: 'low' }
    ];
    
    // Clear existing reminders
    remindersContainer.innerHTML = '';
    
    // Add reminder cards
    reminders.forEach(reminder => {
        const card = document.createElement('div');
        card.className = `reminder-card priority-${reminder.priority}`;
        
        // Calculate days remaining
        const dueDate = new Date(reminder.due);
        const today = new Date();
        const daysRemaining = Math.ceil((dueDate - today) / (1000 * 60 * 60 * 24));
        
        card.innerHTML = `
            <h4>${reminder.title}</h4>
            <div class="reminder-details">
                <span class="due-date">Due: ${formatDate(reminder.due)}</span>
                <span class="days-remaining">${daysRemaining} days remaining</span>
            </div>
            <div class="reminder-actions">
                <button class="action-btn complete-btn" title="Mark as Complete">
                    <i class="fas fa-check"></i>
                </button>
                <button class="action-btn snooze-btn" title="Snooze Reminder">
                    <i class="fas fa-clock"></i>
                </button>
            </div>
        `;
        
        // Add event listeners for buttons
        const completeBtn = card.querySelector('.complete-btn');
        const snoozeBtn = card.querySelector('.snooze-btn');
        
        if (completeBtn) {
            completeBtn.addEventListener('click', () => {
                card.classList.add('completed');
                setTimeout(() => {
                    card.remove();
                }, 500);
            });
        }
        
        if (snoozeBtn) {
            snoozeBtn.addEventListener('click', () => {
                alert('Reminder snoozed for 1 week');
                card.classList.add('snoozed');
            });
        }
        
        remindersContainer.appendChild(card);
    });
}

function editTransaction(transaction) {
    // Open the transaction modal for editing
    const modal = document.getElementById('transactionModal');
    if (!modal) return;
    
    // Populate the form with transaction data
    document.getElementById('transaction-date').value = transaction.date;
    document.getElementById('transaction-description').value = transaction.description;
    document.getElementById('transaction-amount').value = transaction.amount;
    
    // Select the correct transaction type button
    const incomeBtn = document.querySelector('.toggle-btn[data-type="income"]');
    const expenseBtn = document.querySelector('.toggle-btn[data-type="expense"]');
    
    if (transaction.type === 'income' && incomeBtn) {
        incomeBtn.click();
    } else if (transaction.type === 'expense' && expenseBtn) {
        expenseBtn.click();
    }
    
    // Open the modal
    openModal(modal);
}

function deleteTransaction(transaction) {
    // In a real app, you would call an API to delete the transaction
    console.log('Deleting transaction:', transaction);
    
    // Refresh dashboard data
    updateSummaryCards();
    initIncomeExpenseChart();
    initCategoryDistributionChart();
    initBalanceTrendChart();
}

function formatCurrency(amount) {
    // Format number as currency
    return amount.toLocaleString('en-US', {
        style: 'currency',
        currency: 'USD'
    });
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric' 
    });
}

// ============ Data Export and Import Functionality ============
function initDataExportImport() {
    // Setup export buttons
    setupExportButtons();
    
    // Setup import functionality
    setupImportFunctionality();
}

function setupExportButtons() {
    // Get export buttons
    const exportButtons = {
        'export-csv': exportAsCSV,
        'export-json': exportAsJSON,
        'export-pdf': exportAsPDF
    };
    
    // Add event listeners to export buttons
    for (const [id, handler] of Object.entries(exportButtons)) {
        const button = document.getElementById(id);
        if (button) {
            button.addEventListener('click', handler);
        }
    }
}

function setupImportFunctionality() {
    const importButton = document.getElementById('import-data');
    const importFileInput = document.getElementById('import-file');
    
    if (importButton && importFileInput) {
        importButton.addEventListener('click', () => {
            importFileInput.click();
        });
        
        importFileInput.addEventListener('change', handleImportFile);
    }
}

function exportAsCSV() {
    // In a real app, you would fetch data to export
    const dataToExport = getTransactionsForExport();
    
    // Convert data to CSV format
    let csvContent = 'Date,Description,Category,Amount,Type,Currency,Tax Status\n';
    
    dataToExport.forEach(item => {
        const row = [
            item.date,
            `"${item.description.replace(/"/g, '""')}"`, // Escape quotes in CSV
            item.category,
            item.amount,
            item.type,
            item.currency,
            item.taxStatus
        ].join(',');
        csvContent += row + '\n';
    });
    
    // Create blob and download
    downloadFile(csvContent, 'fintrack-transactions.csv', 'text/csv');
}

function exportAsJSON() {
    // In a real app, you would fetch data to export
    const dataToExport = getTransactionsForExport();
    
    // Convert to JSON string
    const jsonContent = JSON.stringify(dataToExport, null, 2);
    
    // Create blob and download
    downloadFile(jsonContent, 'fintrack-transactions.json', 'application/json');
}

function exportAsPDF() {
    // In a real app, you would use a library like jsPDF to create PDF files
    alert('In a real app, this would generate a PDF using jsPDF or a similar library.');
    
    /* 
    Example implementation with jsPDF:
    
    const doc = new jsPDF();
    
    // Add title
    doc.setFontSize(18);
    doc.text('FinTrack Transactions Report', 14, 22);
    
    // Add date
    doc.setFontSize(11);
    doc.text(`Generated on ${new Date().toLocaleDateString()}`, 14, 30);
    
    // Get transactions
    const transactions = getTransactionsForExport();
    
    // Create table
    doc.autoTable({
        startY: 40,
        head: [['Date', 'Description', 'Category', 'Amount', 'Type']],
        body: transactions.map(t => [
            t.date, 
            t.description, 
            t.category, 
            formatCurrency(t.amount), 
            t.type
        ])
    });
    
    // Save the PDF
    doc.save('fintrack-transactions.pdf');
    */
}

function getTransactionsForExport() {
    // In a real app, you would fetch this from your data store
    // For this demo, we return sample data
    return [
        { date: '2023-11-20', description: 'Client Payment - XYZ Corp', category: 'Development', amount: 2500, type: 'income', currency: 'USD', taxStatus: 'taxable' },
        { date: '2023-11-18', description: 'Web Hosting Service', category: 'Software', amount: 29.99, type: 'expense', currency: 'USD', taxStatus: 'deductible' },
        { date: '2023-11-15', description: 'Office Supplies', category: 'Office', amount: 125.30, type: 'expense', currency: 'USD', taxStatus: 'deductible' },
        { date: '2023-11-12', description: 'Client Payment - ABC Inc', category: 'Consulting', amount: 1800, type: 'income', currency: 'USD', taxStatus: 'taxable' },
        { date: '2023-11-10', description: 'Monthly Internet', category: 'Utilities', amount: 89.99, type: 'expense', currency: 'USD', taxStatus: 'deductible' }
    ];
}

function downloadFile(content, fileName, contentType) {
    const blob = new Blob([content], { type: contentType });
    const url = URL.createObjectURL(blob);
    
    const a = document.createElement('a');
    a.href = url;
    a.download = fileName;
    document.body.appendChild(a);
    a.click();
    
    // Clean up
    setTimeout(() => {
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }, 100);
}

function handleImportFile(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    const fileReader = new FileReader();
    
    fileReader.onload = function(e) {
        try {
            // Determine file type from extension
            if (file.name.endsWith('.csv')) {
                importFromCSV(e.target.result);
            } else if (file.name.endsWith('.json')) {
                importFromJSON(e.target.result);
            } else {
                alert('Unsupported file format. Please use CSV or JSON files.');
            }
        } catch (error) {
            console.error('Error importing file:', error);
            alert('Failed to import data. Please check the file format and try again.');
        }
    };
    
    fileReader.onerror = function() {
        alert('Failed to read the file. Please try again.');
    };
    
    if (file.name.endsWith('.csv') || file.name.endsWith('.json')) {
        fileReader.readAsText(file);
    } else {
        alert('Unsupported file format. Please use CSV or JSON files.');
    }
}

function importFromCSV(csvContent) {
    // Basic CSV parsing
    const lines = csvContent.split('\n');
    const headers = lines[0].split(',');
    
    const transactions = [];
    
    for (let i = 1; i < lines.length; i++) {
        if (!lines[i].trim()) continue;
        
        const values = parseCSVLine(lines[i]);
        const transaction = {};
        
        headers.forEach((header, index) => {
            transaction[header.toLowerCase()] = values[index];
        });
        
        transactions.push(transaction);
    }
    
    processImportedTransactions(transactions);
}

function parseCSVLine(line) {
    const result = [];
    let currentValue = '';
    let insideQuotes = false;
    
    for (let i = 0; i < line.length; i++) {
        const char = line[i];
        
        if (char === '"') {
            if (insideQuotes && i + 1 < line.length && line[i + 1] === '"') {
                // Double quotes inside quotes - add a single quote
                currentValue += '"';
                i++;
            } else {
                // Toggle insideQuotes flag
                insideQuotes = !insideQuotes;
            }
        } else if (char === ',' && !insideQuotes) {
            // End of field
            result.push(currentValue);
            currentValue = '';
        } else {
            currentValue += char;
        }
    }
    
    // Add the last value
    result.push(currentValue);
    
    return result;
}

function importFromJSON(jsonContent) {
    const transactions = JSON.parse(jsonContent);
    processImportedTransactions(transactions);
}

function processImportedTransactions(transactions) {
    // In a real app, you would validate and save these transactions to your data store
    console.log('Imported transactions:', transactions);
    
    // Show success message
    alert(`Successfully imported ${transactions.length} transactions.`);
    
    // Refresh dashboard data
    updateSummaryCards();
    initIncomeExpenseChart();
    initCategoryDistributionChart();
    initBalanceTrendChart();
    loadRecentTransactions();
}

// ============ Tax Calculation and Reporting ============
function initTaxCalculator() {
    const taxCalcPage = document.querySelector('.tax-calculator');
    if (!taxCalcPage) return;
    
    // Initialize tax year selector
    const yearSelector = document.getElementById('tax-year');
    if (yearSelector) {
        // Populate with available years (in a real app, this would be based on data)
        const currentYear = new Date().getFullYear();
        for (let year = currentYear; year >= currentYear - 5; year--) {
            const option = document.createElement('option');
            option.value = year;
            option.textContent = year;
            yearSelector.appendChild(option);
        }
        
        yearSelector.addEventListener('change', () => {
            updateTaxReport(yearSelector.value);
        });
    }
    
    // Initialize tax calculation button
    const calcButton = document.getElementById('calculate-tax');
    if (calcButton) {
        calcButton.addEventListener('click', () => {
            const selectedYear = yearSelector.value;
            calculateTaxes(selectedYear);
        });
    }
    
    // Initial tax report
    updateTaxReport(new Date().getFullYear());
}

function updateTaxReport(year) {
    // Get report containers
    const incomeSection = document.querySelector('.taxable-income');
    const expenseSection = document.querySelector('.tax-deductions');
    const summarySection = document.querySelector('.tax-summary');
    
    if (!incomeSection || !expenseSection || !summarySection) return;
    
    // Fetch transactions for the selected year
    // In a real app, this would come from a database
    const transactions = getTaxTransactionsForYear(year);
    
    // Process transactions for tax reporting
    const taxableIncome = transactions.filter(t => t.type === 'income' && t.taxStatus === 'taxable');
    const nonTaxableIncome = transactions.filter(t => t.type === 'income' && t.taxStatus === 'non-taxable');
    const deductibleExpenses = transactions.filter(t => t.type === 'expense' && t.taxStatus === 'deductible');
    const nonDeductibleExpenses = transactions.filter(t => t.type === 'expense' && t.taxStatus === 'non-deductible');
    
    // Calculate totals
    const totalTaxableIncome = taxableIncome.reduce((sum, t) => sum + parseFloat(t.amount), 0);
    const totalNonTaxableIncome = nonTaxableIncome.reduce((sum, t) => sum + parseFloat(t.amount), 0);
    const totalDeductibleExpenses = deductibleExpenses.reduce((sum, t) => sum + parseFloat(t.amount), 0);
    const totalNonDeductibleExpenses = nonDeductibleExpenses.reduce((sum, t) => sum + parseFloat(t.amount), 0);
    
    // Update income section
    renderTaxCategoryItems(incomeSection, taxableIncome, 'Taxable Income', totalTaxableIncome);
    renderTaxCategoryItems(incomeSection, nonTaxableIncome, 'Non-Taxable Income', totalNonTaxableIncome);
    
    // Update expense section
    renderTaxCategoryItems(expenseSection, deductibleExpenses, 'Deductible Expenses', totalDeductibleExpenses);
    renderTaxCategoryItems(expenseSection, nonDeductibleExpenses, 'Non-Deductible Expenses', totalNonDeductibleExpenses);
    
    // Update summary section
    const netTaxableIncome = totalTaxableIncome - totalDeductibleExpenses;
    const estimatedTax = calculateEstimatedTax(netTaxableIncome);
    
    summarySection.innerHTML = `
        <div class="summary-item">
            <span class="summary-label">Total Taxable Income:</span>
            <span class="summary-value">${formatCurrency(totalTaxableIncome)}</span>
        </div>
        <div class="summary-item">
            <span class="summary-label">Total Tax Deductions:</span>
            <span class="summary-value">${formatCurrency(totalDeductibleExpenses)}</span>
        </div>
        <div class="summary-item">
            <span class="summary-label">Net Taxable Income:</span>
            <span class="summary-value">${formatCurrency(netTaxableIncome)}</span>
        </div>
        <div class="summary-item">
            <span class="summary-label">Estimated Tax Liability:</span>
            <span class="summary-value">${formatCurrency(estimatedTax)}</span>
        </div>
        <div class="tax-actions">
            <button id="export-tax-report" class="btn primary-btn">Export Tax Report</button>
            <button id="save-tax-estimates" class="btn secondary-btn">Save Estimates</button>
        </div>
    `;
    
    // Add event listeners to new buttons
    const exportButton = document.getElementById('export-tax-report');
    const saveButton = document.getElementById('save-tax-estimates');
    
    if (exportButton) {
        exportButton.addEventListener('click', () => {
            exportTaxReport(year, {
                taxableIncome,
                nonTaxableIncome,
                deductibleExpenses,
                nonDeductibleExpenses,
                summary: {
                    totalTaxableIncome,
                    totalDeductibleExpenses,
                    netTaxableIncome,
                    estimatedTax
                }
            });
        });
    }
    
    if (saveButton) {
        saveButton.addEventListener('click', () => {
            saveTaxEstimates(year, {
                totalTaxableIncome,
                totalDeductibleExpenses,
                netTaxableIncome,
                estimatedTax
            });
        });
    }
}

function renderTaxCategoryItems(container, items, categoryTitle, categoryTotal) {
    // Create category section
    const categorySection = document.createElement('div');
    categorySection.className = 'tax-category';
    
    // Add category header
    categorySection.innerHTML = `
        <div class="category-header">
            <h4>${categoryTitle}</h4>
            <span class="category-total">${formatCurrency(categoryTotal)}</span>
        </div>
    `;
    
    // Add items if available
    if (items.length > 0) {
        const itemsList = document.createElement('ul');
        itemsList.className = 'tax-items-list';
        
        items.forEach(item => {
            const listItem = document.createElement('li');
            listItem.className = 'tax-item';
            listItem.innerHTML = `
                <div class="tax-item-details">
                    <span class="tax-item-date">${formatDate(item.date)}</span>
                    <span class="tax-item-desc">${item.description}</span>
                </div>
                <span class="tax-item-amount">${formatCurrency(item.amount)}</span>
            `;
            itemsList.appendChild(listItem);
        });
        
        categorySection.appendChild(itemsList);
    } else {
        // No items message
        const noItems = document.createElement('p');
        noItems.className = 'no-items-message';
        noItems.textContent = `No ${categoryTitle.toLowerCase()} transactions found.`;
        categorySection.appendChild(noItems);
    }
    
    // Add to container
    container.appendChild(categorySection);
}

function calculateTaxes(year) {
    // Show loading indicator
    const calculationStatus = document.querySelector('.calculation-status');
    if (calculationStatus) {
        calculationStatus.innerHTML = '<div class="loading-spinner"></div> Calculating taxes...';
        calculationStatus.style.display = 'block';
    }
    
    // Simulate calculation time
    setTimeout(() => {
        updateTaxReport(year);
        
        // Update status
        if (calculationStatus) {
            calculationStatus.innerHTML = '<div class="success-icon"></div> Tax calculation complete!';
            // Hide after a delay
            setTimeout(() => {
                calculationStatus.style.display = 'none';
            }, 3000);
        }
    }, 1500);
}

function getTaxTransactionsForYear(year) {
    // In a real app, you would fetch data for the specific year from a database
    // For this demo, we use sample data
    return [
        { date: `${year}-01-15`, description: 'Client Payment - XYZ Corp', category: 'Development', amount: 2500, type: 'income', taxStatus: 'taxable' },
        { date: `${year}-02-10`, description: 'Client Payment - ABC Inc', category: 'Consulting', amount: 1800, type: 'income', taxStatus: 'taxable' },
        { date: `${year}-03-05`, description: 'Dividend Payment', category: 'Investment', amount: 350, type: 'income', taxStatus: 'taxable' },
        { date: `${year}-04-20`, description: 'Gift from Family', category: 'Gift', amount: 500, type: 'income', taxStatus: 'non-taxable' },
        { date: `${year}-01-25`, description: 'Web Hosting Service', category: 'Software', amount: 29.99, type: 'expense', taxStatus: 'deductible' },
        { date: `${year}-02-15`, description: 'Office Supplies', category: 'Office', amount: 125.30, type: 'expense', taxStatus: 'deductible' },
        { date: `${year}-03-10`, description: 'Design Software Subscription', category: 'Software', amount: 49.99, type: 'expense', taxStatus: 'deductible' },
        { date: `${year}-04-05`, description: 'Monthly Internet', category: 'Utilities', amount: 89.99, type: 'expense', taxStatus: 'deductible' },
        { date: `${year}-02-28`, description: 'Lunch with Friend', category: 'Meals', amount: 45.00, type: 'expense', taxStatus: 'non-deductible' },
        { date: `${year}-03-15`, description: 'Personal Subscription', category: 'Entertainment', amount: 15.99, type: 'expense', taxStatus: 'non-deductible' }
    ];
}

function calculateEstimatedTax(netTaxableIncome) {
    // This is a simplified tax calculation for demonstration
    // In a real app, you would use proper tax brackets and rates based on user's location
    
    // Sample progressive tax brackets (USA-inspired)
    const taxBrackets = [
        { max: 9950, rate: 0.10 },
        { max: 40525, rate: 0.12 },
        { max: 86375, rate: 0.22 },
        { max: 164925, rate: 0.24 },
        { max: 209425, rate: 0.32 },
        { max: 523600, rate: 0.35 },
        { max: Infinity, rate: 0.37 }
    ];
    
    let remainingIncome = netTaxableIncome;
    let totalTax = 0;
    let previousMax = 0;
    
    for (const bracket of taxBrackets) {
        const taxableInBracket = Math.min(remainingIncome, bracket.max - previousMax);
        if (taxableInBracket <= 0) break;
        
        totalTax += taxableInBracket * bracket.rate;
        remainingIncome -= taxableInBracket;
        previousMax = bracket.max;
        
        if (remainingIncome <= 0) break;
    }
    
    return totalTax;
}

function exportTaxReport(year, data) {
    // In a real app, you would generate a proper tax report
    // For this demo, we'll just create a simple JSON file
    
    const reportData = {
        year,
        preparedOn: new Date().toISOString(),
        data
    };
    
    const jsonContent = JSON.stringify(reportData, null, 2);
    downloadFile(jsonContent, `tax-report-${year}.json`, 'application/json');
    
    alert(`Tax report for ${year} has been exported.`);
}

function saveTaxEstimates(year, estimates) {
    // In a real app, you would save this to a database
    // For this demo, we just save to localStorage
    
    // Get existing estimates or initialize empty object
    const savedEstimates = JSON.parse(localStorage.getItem('taxEstimates') || '{}');
    
    // Save for the specific year
    savedEstimates[year] = {
        ...estimates,
        savedAt: new Date().toISOString()
    };
    
    // Save back to localStorage
    localStorage.setItem('taxEstimates', JSON.stringify(savedEstimates));
    
    alert(`Tax estimates for ${year} have been saved.`);
} 

let receiptInfo = {};  // Store image URL + parsed data here

document.getElementById("receipt-upload").addEventListener("change", async function (event) {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await fetch("/upload-receipt", {
            method: "POST",
            body: formData,
        });

        const result = await response.json();
        const previewImg = document.getElementById("receipt-preview-img");
        const downloadLink = document.getElementById("receipt-download-link");

        // Hide previous previews
        previewImg.style.display = "none";
        downloadLink.style.display = "none";
        downloadLink.href = "";
        downloadLink.textContent = "";

        if (result.success) {
            const imageUrl = result.url;

            // Show preview
            if (file.type.startsWith("image/")) {
                previewImg.src = result.url;
                previewImg.style.display = "block";
            } else if (file.type === "application/pdf") {
                downloadLink.href = result.url;
                downloadLink.textContent = "📄 Download uploaded PDF";
                downloadLink.style.display = "inline-block";
            }

            // Call backend to extract info
            const extractRes = await fetch("/extract-receipt-data", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ image_url: imageUrl }),
            });

            const extractData = await extractRes.json();
            if (extractData.success) {
                const d = extractData.data;
                receiptInfo = { ...d, image_url: imageUrl }; // Save for later use

                // Inject values into modal
                document.getElementById("extracted-date").textContent = d.Date || "-";
                document.getElementById("extracted-vendor").textContent = d.Vendor || "-";
                document.getElementById("extracted-total").textContent = d["Total Amount"] || "-";
                document.getElementById("extracted-currency").textContent = d.Currency || "-";
                document.getElementById("extracted-tax").textContent = d["Tax Amount"] || "-";
                document.getElementById("extracted-category").textContent = d.Category || "-";
            } else {
                alert("Failed to extract receipt info.");
            }
        } else {
            alert("Upload failed: " + (result.error || "Unknown error"));
        }
    } catch (err) {
        alert("Error uploading file");
        console.error(err);
    }
});


