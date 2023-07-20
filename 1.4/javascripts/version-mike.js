(window.onload = function () {
    setInterval(function () {
      var items = document.querySelectorAll('.md-version__link:not(.changed)');
      if (!items.length) return;
  
      var item = document.querySelector(".md-version__current");
      if (!item) return;
  
      var version_now = item.innerHTML;
      console.log(version_now);
      var i = window.location.pathname.indexOf(version_now) + version_now.length + 1;
      var pathname = window.location.pathname.slice(i);
  
      for (var item of items) {
        item.href += pathname;
        item.className += " changed";
        console.log(item.innerHTML, "change successfully");
      }
    }, 100);
  })();