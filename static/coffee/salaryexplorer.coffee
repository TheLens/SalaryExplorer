jQuery ->
  $('#search_button').click -> 
    number = $("#input_box").val().replace(/\s{2,}/g, ' ').replace(/\s{1}/g, '+')
    $.get '/search', (data) ->
        $("#results").html(data)
        $(document).foundation()