var page_length = 20; //20 results per page
var page = 1;

function formatCurrency(number) {
  var n = number.split('').reverse().join("");
  var n2 = n.replace(/\d\d\d(?!$)/g, "$&,");
  var return_val = '$' + n2.split('').reverse().join('');
  // console.log(return_val);
  return return_val;
}

function formatThousands(number) {
  if (typeof number === 'number') {
    number = number.toString();
  }
  var n = number.split('').reverse().join("");
  var n2 = n.replace(/\d\d\d(?!$)/g, "$&,");
  var return_val = n2.split('').reverse().join('');
  return return_val;
}

function reformat(id) {
  var new_id = (id).toString();
  var number = $("#" + new_id).html();
  //var newval = "$" + (Number($(id).html()).formatMoney(2, '.', ','));
  var newval = formatCurrency(number);
  $("#" + new_id).html(newval);
}






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

function process_request(request){

    var result = {}, key;

    var output = window.data; //start by assuming all values can be returned, then filter down

    if (request['organization'] !== "") {
        output = _.filter(output, function(item){ return item['organization'] == request['organization']; });
    }

    if (request['job'] !== "" && request['job'] !== "ALL"){
        output = _.filter(output, function(item){ return item['job'].toUpperCase().indexOf(request['job'].toUpperCase()) != -1 });
    }

    if (request['name'] !== ""){
              
       output = _.filter(output, function(item){ return item['name'].toUpperCase().indexOf(request['name'].toUpperCase()) !== -1 });
    }

    return output;

}


//to do: template engine
function get_row(item, id){
    if (typeof item == 'undefined') {
        return ""; //row is blank. can't "render" row
    }
    item['id'] = id;
    var source;
    if ($(window).width() > 500) {
        source = $("#big-template").html();
    } else {
        source = $("#little-template").html();
        $("#thead").remove(); // not in table mode
        $("#myTable").show();
    }
    if (typeof source !== 'undefined') {
      var template = Handlebars.compile(source);
      var html = template(item);
    }
    return html;
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
    for (var i = offset * page_length; i < offset * page_length + page_length; i++) {
        var row = get_row(results[i], i);
        output += row
    }

    return output;
}

function loadTable() {
  if ($("#myTable tr").length > 1){
    $("#myTable").show();
  }
  $("#results_status").html('');
  var name = $('#input-box').val();
  var data = {};
  data['organization'] = $('#organizations').val();
  data['job'] = $('#positions').val();
  data['name'] = name;
  data['page'] = 1;
  $("#tbody").html("");
  var html = $("#myTable").html();
  var results = process_request(data);
  var pages = Math.ceil(results.length / page_length);
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
    $("#myTable").css("border-color", "#DDDDDD");
  }
}

$(window).on('resize', function() {
  adjustWidth();
  //loadTable();
});

// function process(data){
//   var args = data;
//   console.log("processing raw data");
//   var split = data.split("\n");
//   output = [];
//   for (var i = 1; i < split.length; i++) {
//     var items = split[i].split("\t");
//     var item = {};
//     item['organization'] = items[0];
//     item['unit'] = items[1]
//     item['name'] = items[2]
//     item['job'] = items[3]
//     item['rate'] = items[4]
//     if (!_.isUndefined(item['name'])){
//       output.push(item);
//     }
//   }
//   console.log("processed raw data");
//   window.data = output;
// }

function process(data) {
  window.salaries = $.csv.toObjects(data);
}

$.ajax({
  type: "GET",
  url: "https://s3-us-west-2.amazonaws.com/lensnola/state-salaries/data/export/data.csv.gz",
  dataType: "text",
  success: function(data) {
    process(data);
  }
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

  $("#search-button").on("click", function() {
    page = 1; //reset page to page 1 for new search
    loadTable();
  });
});
