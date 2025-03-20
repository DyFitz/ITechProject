// static/js/eventdetails_staff.js

document.addEventListener('DOMContentLoaded', function() {
    // get“Attendance Checking” button
    var attendeeModalBtn = document.getElementById('attendeeModalBtn');
    // get modal
    var attendeeModal = document.getElementById('attendeeModal');
    // get close button
    var closeAttendeeBtn = document.getElementById('closeAttendeeBtn');

    // Click “Attendance Checking” button shows modal
    if (attendeeModalBtn && attendeeModal) {
        attendeeModalBtn.addEventListener('click', function() {
            attendeeModal.classList.add('show');
        });
    }

    // Click the close button to close the modal
    if (closeAttendeeBtn && attendeeModal) {
        closeAttendeeBtn.addEventListener('click', function() {
            attendeeModal.classList.remove('show');
        });
    }

    // Clicking on the modal background closes the modal (or closes it if the target of the click is the modal itself)
    if (attendeeModal) {
        attendeeModal.addEventListener('click', function(event) {
            if (event.target === attendeeModal) {
                attendeeModal.classList.remove('show');
            }
        });
    }
});
