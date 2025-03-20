// static/js/myaccount.js

document.addEventListener('DOMContentLoaded', function () {
  var avatar = document.getElementById('avatar');
  if (avatar) {
    avatar.addEventListener('click', function () {
      // get data-url
      var targetUrl = avatar.getAttribute('data-url');
      if (targetUrl) {
        window.location.href = targetUrl;
      }
    });
  }
});
