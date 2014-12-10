(function() {

  jQuery(function() {
    return $('#search_button').click(function() {
      var number;
      name_title = $("#input_box").val().replace(/\s{2,}/g, ' ').replace(/\s{1}/g, '+');
      try {
         agency = "&agency=" + $("#agencies").val();
      }
      catch(err) {
         agency = ""; // the dropbox is also set to "Agency" by default 
      }
      try {
         department = "&department=" + $("#departments").val();
      }
      catch(err) {
         department = ""; // the dropbox is also set to "Agency" by default 
      }
      try {
         title = "&title=" + $("#titles").val();
      }
      catch(err) {
         title = ""; // the dropbox is also set to "Agency" by default 
      }          
      var existing_url = document.URL;
      if (existing_url.indexOf("q=") > -1) {
          page = parseInt(document.URL.match("&page=[0-9]+$")[0].replace("&page=", ""));
      }
      else{
          page = "&page=" + 1;
      }
      var query = '/search/q=' + name_title + agency + department + title + page;
      var url = document.URL.substring(0, document.URL.length - 1);   //remove the last slash
      url = url + query;
      var stateObj = { foo: "bar" };
      return $.post(query, function(data) {
        $("#results").html(data);
        history.pushState(stateObj, "", query);
        return $(document).foundation();
      });
    });
    return $('#forward').click(function() {
      alert("hereeee");
    });
    return $('#back').click(function() {
      alert("hereeee");
    });
  });
  jQuery(function() {
    return $('#forward').click(function() {
      alert("hereeee");
    });
  });
  jQuery(function() {
    return $('#back').click(function() {
      alert("hereeee");
    });
  });

}).call(this);