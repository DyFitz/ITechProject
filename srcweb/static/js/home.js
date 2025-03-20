// home.js
document.addEventListener('DOMContentLoaded', function () {
  // Student Login
  var studentBtn = document.getElementById('student-login');
  if (studentBtn) {
    studentBtn.addEventListener('click', function () {
      var target = studentBtn.getAttribute('data-url');
      if (target) {
        window.location.href = target;
      }
    });
  }

  // Staff Login
  var staffBtn = document.getElementById('staff-login');
  if (staffBtn) {
    staffBtn.addEventListener('click', function () {
      var target = staffBtn.getAttribute('data-url');
      if (target) {
        window.location.href = target;
      }
    });
  }

  // Explore
  var exploreBtn = document.getElementById('explore-button');
  if (exploreBtn) {
    exploreBtn.addEventListener('click', function () {
      var target = exploreBtn.getAttribute('data-url');
      if (target) {
        window.location.href = target;
      }
    });
  }
});
