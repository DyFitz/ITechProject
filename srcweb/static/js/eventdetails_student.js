// static/js/eventdetails_student.js

document.addEventListener('DOMContentLoaded', function() {
    var bookingBtn = document.getElementById('bookingBtn');
    var bookingModal = document.getElementById('bookingModal');
    var closeBookingBtn = document.getElementById('closeBookingBtn');

    // Register a click event for the "Book my place" button to open a popup window.
    if (bookingBtn && bookingModal) {
        bookingBtn.addEventListener('click', function() {
            bookingModal.classList.add('show');
        });
    }

    // Register a click event for the close button to close the popup window
    if (closeBookingBtn && bookingModal) {
        closeBookingBtn.addEventListener('click', function() {
            bookingModal.classList.remove('show');
        });
    }

    // Click on the background of the popup (i.e. modal-overlay) to close it.
    if (bookingModal) {
        bookingModal.addEventListener('click', function(event) {
            //If the target of the click is the popup background itself
            if (event.target === bookingModal) {
                bookingModal.classList.remove('show');
            }
        });
    }
});
