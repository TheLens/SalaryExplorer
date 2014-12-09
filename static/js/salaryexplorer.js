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
      var query = '/search/q=' + name_title + agency + department + title;
      var url = document.URL.substring(0, document.URL.length - 1);   //remove the last slash
      url = url + query;
      var stateObj = { foo: "bar" };
      return $.get(query, function(data) {
        $("#results").html(data);
        history.pushState(stateObj, "", query);
        return $(document).foundation();
      });
    });
  });

}).call(this);