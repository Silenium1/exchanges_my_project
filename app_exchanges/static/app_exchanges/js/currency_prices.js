// Load any saved checkbox states from local storage
window.onload = function() {
    const checkboxes = document.querySelectorAll('#filter-form input[type=checkbox]');
    checkboxes.forEach(function(checkbox) {
        const checkboxState = localStorage.getItem(checkbox.id);
        if (checkboxState === 'true') {
            checkbox.checked = true;
        }
    });
    filterTable();
};

// Update the state of a checkbox and filter the table
function updateCheckboxState(checkbox) {
    localStorage.setItem(checkbox.id, checkbox.checked);
    filterTable();
}

// Select or deselect all exchanges
function selectAllExchanges(checkbox) {
    const exchangeCheckboxes = document.getElementsByName('exchange');
    for (let i = 0; i < exchangeCheckboxes.length; i++) {
        exchangeCheckboxes[i].checked = checkbox.checked;
        updateCheckboxState(exchangeCheckboxes[i]);
    }
    filterTable();
}

// Filter the table based on the selected checkboxes
function filterTable() {
    const exchangeCheckboxes = document.getElementsByName('exchange');
    const exchangeTable = document.getElementById('exchange-table');
    const rows = exchangeTable.getElementsByTagName('tr');
    let isAnyCheckboxChecked = false;

    for (let i = 0; i < exchangeCheckboxes.length; i++) {
        if (exchangeCheckboxes[i].checked) {
            isAnyCheckboxChecked = true;
            break;
        }
    }

    for (let i = 1; i < rows.length; i++) {
        const exchangeName = rows[i].getElementsByTagName('td')[0].innerText;
        let shouldDisplay = false;

        if (exchangeName === 'Exchange') {
            shouldDisplay = true; // Display table header
        } else {
            if (isAnyCheckboxChecked) {
                for (let j = 0; j < exchangeCheckboxes.length; j++) {
                    if (exchangeCheckboxes[j].checked && exchangeCheckboxes[j].value === exchangeName) {
                        shouldDisplay = true;
                        break;
                    }
                }
            } else {
                shouldDisplay = true; // Display all rows when no checkboxes are checked
            }
        }

        rows[i].style.display = shouldDisplay ? '' : 'none';
    }
}

// Add change event listener to the form
document.getElementById('filter-form').addEventListener('change', function(event) {
    if (event.target.type === 'checkbox') {
        updateCheckboxState(event.target);
    }
});
