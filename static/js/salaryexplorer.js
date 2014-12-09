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
      return $.get(query, function(data) {
        $("#results").html(data);
        return $(document).foundation();
      });
    });
  });

}).call(this);
