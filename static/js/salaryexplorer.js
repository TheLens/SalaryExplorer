function get_query() {
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
    return '/search/q=' + name_title + agency + department + title;
}


function get_page(){
    var existing_url = document.URL;
    if (existing_url.indexOf("q=") > -1) {
        var page = parseInt(document.URL.match("&page=[0-9]+$")[0].replace("&page=", ""));
    }
    else{
        var page = 1;
    }
    return page;
}

function post_query(page){
    console.log(page);
    page = page || 1;
    console.log(page);
    var query = get_query() + "&page=" + page;
    var url = document.URL.substring(0, document.URL.length - 1);
    url = url + query;
    var stateObj = { foo: "bar" }; 
    return $.post(query, function(data) {
        var agency = $("#agencies").val();
        var department = $("#departments").val();
        var title = $("#title").val();
        $("#results").html(data);
        if (typeof agency != "undefined") {
            $("#agencies").val(agency);
        }
        if (typeof department != "undefined") {
            $("#departments").val(department);
        }
        if (typeof title != "undefined") {
            $("#title").val(title);
        }
        history.pushState(stateObj, "", query);
        set_handlers();
        return $(document).foundation();
    });
}

function set_handlers(){

    $('#forward').click(function() {
        var page = get_page();
        page = parseInt(page) + 1;
        post_query(page);
    });

    $('#back').click(function() {
        var page = get_page();
        if (page > 1) {
            page = parseInt(page -1);
        }else{
            alert("This page shows the first results");
        }
        post_query(page);
    });

    $("#return_to_search").click(function (){
        window.location = document.referrer;
    });

    $('#search_button').click(function() {
      var number;               
      page = get_page();
      post_query(page);
    });

    $("#agencies").change(function () {
        post_query(); //leave page argument blank
    });

    $("#titles").change(function () {
        post_query(); //leave page argument blank
    });

    $("#departments").change(function () {
        post_query(); //leave page argument blank
    });

    $(document).keypress(function(e) {
    if(e.keyCode == 13) 
    {
      var number;               
      page = get_page();
      post_query(page);
    }
  });

}

$(document).ready(function() {
    set_handlers();
});