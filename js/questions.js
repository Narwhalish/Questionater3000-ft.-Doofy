jQuery.get('questionGenerator/fill_out.txt', function(data) {
  var text = data.split('\n')
  document.getElementById("fill1").value = text[0]
}
