function onReady() {
    const dataTableElements = document.querySelectorAll('.data-table');
    if (dataTableElements.length > 0) {
        dataTableElements.forEach(table => {
            new simpleDatatables.DataTable(table);

        });
    }
}
if (document.readyState !== "loading") {
    onReady(); // Or setTimeout(onReady, 0); if you want it consistently async
} else {
    document.addEventListener("DOMContentLoaded", onReady);
}