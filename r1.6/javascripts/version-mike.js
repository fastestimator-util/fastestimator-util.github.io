(window.onload = function () {
    setInterval(function () {
      var items = document.querySelectorAll('.md-version__link:not(.changed)');
      var request;
      var redirect_section;
      if(window.XMLHttpRequest)
        request = new XMLHttpRequest();
      else
        request = new ActiveXObject("Microsoft.XMLHTTP");
      if (!items.length) return;
  
      var item = document.querySelector(".md-version__current");
      if (!item) return;
  
      var version_now = item.innerHTML;
      console.log(version_now);
      var i = window.location.pathname.indexOf(version_now) + version_now.length + 1;
      var pathname = window.location.pathname.slice(i);
      const path_elements = pathname.split("/")
      if (path_elements[0] == "fastestimator") {
        redirect_section = "fastestimator/estimator.html"
      } else if (path_elements[0] == "apphub") {
        redirect_section = "apphub/index.html"
      } else if (path_elements[0] == "tutorial") {
        redirect_section = "tutorial/beginner/t01_getting_started.html"
      }
      console.log("pathname", pathname)
      console.log("redirect_path", redirect_section)
  
      for (var item of items) {
        url_test = item.href + pathname
        request.open('GET', url_test, false);
        request.send();
        
        if (request.status === 404) {
          item.href += redirect_section
        } else{
          item.href += pathname;
        }
        console.log("item href", item.href)
        item.className += " changed";
        console.log(item.innerHTML, "change successfully");
      }
    }, 100);
  })();