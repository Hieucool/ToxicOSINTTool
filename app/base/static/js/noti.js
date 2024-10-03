function toggleActivityLogDropdown() {
    var collapsible = document.getElementById('collapseOne');
    var activityLogLink = document.getElementById('activityLogLink');
    
    if (collapsible.classList.contains('show')) {
        collapsible.classList.remove('show');
        activityLogLink.setAttribute('aria-expanded', 'false');
    } else {
        collapsible.classList.add('show');
        activityLogLink.setAttribute('aria-expanded', 'true');
    }
}