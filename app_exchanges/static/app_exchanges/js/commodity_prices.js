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

function updateCheckboxState(checkbox) {
    localStorage.setItem(checkbox.id, checkbox.checked);
    filterTable();
}

function selectAllExchanges(checkbox) {
    const exchangeCheckboxes = document.getElementsByName('exchange');
    for (let i = 0; i < exchangeCheckboxes.length; i++) {
        exchangeCheckboxes[i].checked = checkbox.checked;
        updateCheckboxState(exchangeCheckboxes[i]);
    }
    filterTable();
}

function filterTable() {
    const exchangeCheckboxes = document.getElementsByName('exchange');
    const exchangeTable = document.querySelector('table');
    const rows = exchangeTable.getElementsByTagName('tr');
    let isAnyCheckboxChecked = false;

    for (let i = 0; i < exchangeCheckboxes.length; i++) {
        if (exchangeCheckboxes[i].checked) {
            isAnyCheckboxChecked = true;
            break;
        }
    }

    for (let i = 1; i < rows.length; i++) {
        const exchangeName = rows[i].getAttribute('class');
        let shouldDisplay = false;
        if (exchangeName) {
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
        } else {
            shouldDisplay = true; // Display rows without class (table header)
        }
        rows[i].style.display = shouldDisplay ? '' : 'none';
    }
}
