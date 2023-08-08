document.addEventListener("DOMContentLoaded", function () {
    const sortByExpiryButton = document.getElementById("sort-by-expiry");
    const table = document.getElementById("table-content");
    const tableRows = table.querySelectorAll("tr:not(:first-child)");

    sortByExpiryButton.addEventListener("click", function () {
        const sortedRows = Array.from(tableRows).slice(0); // Clone the rows array
        sortedRows.sort(function (a, b) {
            const dateA = new Date(a.cells[2].textContent);
            const dateB = new Date(b.cells[2].textContent);
            return dateA - dateB;
        });

        tableRows.forEach(function (row) {
            row.remove();
        });

        sortedRows.forEach(function (row) {
            table.appendChild(row);
        });
    });
});
