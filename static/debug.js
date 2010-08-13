function stepinto() {
  $.ajax({
    type: "GET",
    // Use random to avoid browser Ajax bug
    url: '/ajax/' + fname + '?random=' + new Date().getTime(),
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
	  scopes[level] += "<tr><td class=\"name\">" + vname + "</td><td class=\"bindvalue\">" + str.substr(pos+1) + "</td></tr>";
	}
      }
      var html = "<table style=\"text-align: center\">";
      for (var i = 0; i < scopes.length; i++) {
	if (typeof(scopes[i]) == 'undefined') continue;
	html += "<th colspan=\"2\">Level " + i + " binding(s)</th>";
	html += scopes[i];
      }
      html += "</table>";
      $("#scope").html(html);
      if (lineno > 0) {
        $("div.highlighted").removeClass("highlighted");
        $("div.number"+lineno).addClass("highlighted");
      }

    $("#scopewrapper tr:has('th')").toggle(
        function() {
            var next = $(this);
            while (next) {
                next = next.next();
                if ($("td", next).size() > 0) {
                    next.hide();
                }
                else
                    break;
            }
        },
        function() {
            var next = $(this);
            while (next) {
                next = next.next();
                if ($("td", next).size() > 0) {
                    next.show();
                }
                else
                    break;
            }
        });
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
  $("#restartbtn").click(function() {
    location.reload();
  });
});
