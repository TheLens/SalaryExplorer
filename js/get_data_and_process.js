self.addEventListener("message", function(e) {
  var args = e.data.args;
  console.log("processing raw data");
  var split = args[0]['data'].split("\n");
  output = {};
  for (var i = 1; i < split.length; i++) {
    var items = split[i].split("\t");
    output[i-1] = items;
  }
  console.log("processed raw data");
}, false);