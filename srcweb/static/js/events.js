// static/js/events.js

document.addEventListener('DOMContentLoaded', function() {
  const dropdownIcon = document.getElementById('dropdownIcon');
  const dropdownMenu = document.getElementById('dropdownMenu');
  const rightHeader = document.getElementById('rightHeader');

  //  dropdownIcon
  if (dropdownIcon) {
    dropdownIcon.addEventListener('click', function(e) {
      e.stopPropagation();
      if (dropdownMenu.style.display === '' || dropdownMenu.style.display === 'none') {
        dropdownMenu.style.display = 'block';
      } else {
        dropdownMenu.style.display = 'none';
      }
    });
  }

  // Hide dropdownMenu
  document.addEventListener('click', function(e) {
    if (!rightHeader.contains(e.target)) {
      dropdownMenu.style.display = 'none';
    }
  });
});
