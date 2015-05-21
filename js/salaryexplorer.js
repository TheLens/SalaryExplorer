//http://stackoverflow.com/questions/149055/how-can-i-format-numbers-as-money-in-javascript
Number.prototype.formatMoney = function(c, d, t) {
    var n = this,
        c = isNaN(c = Math.abs(c)) ? 2 : c,
        d = d == undefined ? "." : d,
        t = t == undefined ? "," : t,
        s = n < 0 ? "-" : "",
        i = parseInt(n = Math.abs(+n || 0).toFixed(c)) + "",
        j = (j = i.length) > 3 ? j % 3 : 0;
    return s + (j ? i.substr(0, j) + t : "") + i.substr(j).replace(/(\d{3})(?=\d)/g, "$1" + t) + (c ? d + Math.abs(n - i).toFixed(c).slice(2) : "");
};


function fill_autocomplete(list){
  $.get('https://s3-us-west-2.amazonaws.com/lensnola/salaryexplorer/data/' + list + '.csv.gz', function(data) {
   var values = data.split("\n");
   $( "#" + list ).autocomplete({
      source: values
    });
  }, 'text');
}

fill_autocomplete("organizations");
fill_autocomplete("positions");

var PAGE_LENGTH = 20; //20 results per page
var page = 1;

function process_request(request){

    var result = {}, key;

    var output = window.data; //start by assuming all values can be returned, then filter down

    if (request['organization']!=""){
        output = _.filter(output, function(item){ return item['organization'] == request['organization']; });
    }

    if (request['job']!="" && request['job']!="ALL"){
        output = _.filter(output, function(item){ return item['job'].toUpperCase().indexOf(request['job'].toUpperCase()) != -1 });
    }

    if (request['name']!=""){
              
       output = _.filter(output, function(item){ return item['name'].toUpperCase().indexOf(request['name'].toUpperCase()) != -1 });
    }

    return output;

}


//to do: template engine
function get_row(item, id){
    if (typeof item == 'undefined') {
        return ""; //row is blank. can't "render" row
    }
    item['id'] = id;
    if ($(window).width() > 500) {
         var source   = $("#entry-template").html();
         var template = Handlebars.compile(source);
         var html = template(item);
         return html;
    } else {
          $("#thead").remove(); // not in table mode
          return '<div class="tablerow">\
           <div class="namerow"><span class="first">' + item['name'].toUpperCase() + '</span> </div>\
           <div class="detailsrow"><span class="department">' + item['organization'].toUpperCase() + ' | </span><span class="title">'+ item['job'].toUpperCase() +'</span></div>\
           <div><span id="'+ id + '" class="salary">'+ item['rate'].toUpperCase() +'</span></div></div>';
    }
}


function reformat(id) {
    var newval = "$" + Number($(id).html().replace(",","")).formatMoney(2, '.', ',');
    $(id).html(newval);
}


function get_rows(results, page){
    output = "";
    var offset = page - 1;
    if (offset < 0){
        offset = 0;
    }
    for (var i = offset * PAGE_LENGTH; i < offset * PAGE_LENGTH + PAGE_LENGTH; i++) {
        var row = get_row(results[i], i);
        output += row
    }

    return output;
}

function add_table(){
  var table = '<table id="myTable" class="tablesorter"><thead id="thead"><tr>' +
      '<th width="20%">Name</th><th width="20%">Organization</th>' +
      '<th width="20%">Position</th><th width="20%">Salary</th></tr></thead>' +
      '<div id="tbody_div"><tbody id="tbody"></tbody></div></table>';
  return table
}

function loadTable() {
    if ($( "#myTable" ).length == 0){
      var table = add_table();
      $("#results").append(table);
    }
    $("#results_status").html('');
    var name = $('#input_box').val();
    var data = {};
    data['organization'] = $('#organizations').val();
    data['job'] = $('#positions').val();
    data['name'] = name;
    data['page'] = 1;
    $("#tbody").html("");
    var html = $("#myTable").html();
    $("#results_status").html("Searching...");
    var results = process_request(data);
    var pages = Math.ceil(results.length / PAGE_LENGTH);
    if (page > pages){
      page = pages;
    }
    var new_rows = get_rows(results, page);
    $("#tbody").html(new_rows);
    $("#myTable").trigger("update");
    if (results.length > 20 && !$("#nextprev").length !=0){
        $("#tbody_div").append('<div id="nextprev"><a id="previous">Previous</a> | <a id="next">Next</a></div>');
        $("#next").on("click", function() {
           page = page + 1;
           loadTable();
        });

       $("#previous").on("click", function() {
           page = page -1;
           if (page < 1){
              page = 1;
           }
           loadTable();
        });
    }
    var results_status = results.length + " results found";
    if (results.length > 20){
        results_status = results_status + " | page " + page + " of " + pages;
    }
    $("#results_status").html(results_status);
    $.each($(".salary"), function(index, val) {
        reformat("#" + (index));
    });
}

function adjustWidth() {
    if ($(window).width() < 500) {
        $("#thead").hide();
        $("div#ui_components").css("width", "100%");
        $("#searchButton").css("width", "100%");
        console.log('if');
        $("#searchButton").css("float", "right");
        $("#myTable").css("border-color", "white");
        $("table.tablesorter").css('font-size', '1em');
    } else {
        $("#thead").show();
        console.log('else');
        $("div#ui_components").css("width", "100%");
        $("#searchButton").css("width", "20%");
        $("#searchButton").css("float", "right");
        $("#myTable").css("border-color", "#dddddd");
    }
}

$(window).on('resize', function() {
    adjustWidth();
    //loadTable();
});

$(document).ready(function() {

    $(function() {
        $("#myTable").tablesorter();
    });

    $(document).keypress(function(e) {
        if (e.which == 13) {
            loadTable();
        }
    });

    adjustWidth();

    $("#search_button").on("click", function() {
        page = 1; //reset page to page 1 for new search
        loadTable();
    });

});

function process(data){
  var args = data;
  console.log("processing raw data");
  var split = data.split("\n");
  output = [];
  for (var i = 1; i < split.length; i++) {
    var items = split[i].split("\t");
    var item = {};
    item['organization'] = items[0];
    item['unit'] = items[1]
    item['name'] = items[2]
    item['job'] = items[3]
    item['rate'] = items[4]
    if (!_.isUndefined(item['name'])){
      output.push(item);
    }
  }
  console.log("processed raw data");
  window.data = output;
}

$.ajax({
  type: "GET",
  url: "https://s3-us-west-2.amazonaws.com/lensnola/salaryexplorer/data/all.tsv.gz",
  dataType: "text",
  success: function(data) {process(data)}
});