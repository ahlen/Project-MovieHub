<!DOCTYPE html>
<html>
	<head>
	</head>
	<body>
		<%
			if(request.getParameter("q").equals("test")) {
				out.println("Hello You");
			} else {
				out.println("Set ?q=test");
				out.println(request.getParameter("q"));
			}
		%>
	</body>
</html>