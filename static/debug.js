function stepinto() {
  $.ajax({
    type: "GET",
    // Use random to avoid browser Ajax bug
    url: '/ajax/function_test?random=' + new Date().getTime(),
    timeout: 1000,
    success: function(data) {
      lines = data.split('\n');
      lineno = -1;
      len = lines.length;
      var scopes = Array();
      for (var i = 0; i < len; i++) {
        if (lines[i].charAt(0) == '#') {
	  lineno = parseInt(lines[i].substr(1));
        }
        if (lines[i].charAt(0) == '?' && lines[i].charAt(1) == '?') {
	  alert("Terminated");
	  return;
        }
	level = -1;
	str = lines[i];
	while (str.length > 2 && str.charAt(0) == '*' && str.charAt(1) == '*') {
	  str = str.substr(2);
	  level ++;
	}
	if (level >= 0) {
	  pos = str.indexOf(":");
	  vname = str.substr(0, pos);
	  str = str.replace('>', '&gt;');
	  str = str.replace('<', '&lt;');
	  if (scopes[level] == null)
	    scopes[level] = "";
	  scopes[level] += "<tr><td>" + vname + "</td><td>" + str.substr(pos+1) + "</td></tr>";
	}
      }
      var html = "<table style=\"text-align: center\">";
      for (var i = 0; i < scopes.length; i++) {
	if (typeof(scopes[i]) == 'undefined') continue;
	html += "<th colspan=\"2\" style=\"background-color: #ccc\">Level " + i + " binding(s)</th>";
	html += scopes[i];
      }
      html += "</table>";
      $("#scope").html(html);
      if (lineno > 0) {
        $("div.highlighted").removeClass("highlighted");
        $("div.number"+lineno).addClass("highlighted");
      }
    },
    error: function(obj, error) {
      alert("Ajax error " + error);
    }
  });
}

$(function () {
  SyntaxHighlighter.all();
  $("#nextbtn").click(function() {
    stepinto();
    return false;
  });
});
