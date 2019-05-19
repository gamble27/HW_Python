HTML_MAIN = """<html>
<title>Маршруты</title>
<body>
<form method=POST action="">
<h1 style="text-align: center">Опции</h1>
<p style="text-align: center">
<font size="4" color="blue">Выберите режим:</font>
<table align="center">
<tr>
<td><input type="radio" id="option0" name="opt" value="lists_r"></td>
<td><label for="option0">Список маршрутов</label></td>
<td><input type="radio" id="option1" name="opt" value="lists_p"></td>
<td><label for="option0">Список пассажиров</label></td>
</tr>
<tr>
<td><input type="radio" id="option2" name="opt" value="add_pass"></td>
<td><label for="option1">Добавить пассажира</label></td>
<td><input type="radio" id="option3" name="opt" value="add_route"></td>
<td><label for="option2">Добавить маршрут</label></td>
</tr>
</table>
<br>
<input type=submit value="Обработать">
</form>
</body>
</html>
"""

HTML_ADD_ROUTE = """<html>
<title>Маршруты</title>
<body>
<form method=POST action="">
<h1 style="text-align: center">Добавить маршрут</h1>
<p style="text-align: center">
<font size="4" color="blue">Укажите города:</font><br>
<table align="center" style="text-align: center">
<tr>
<td>Город №1:</td>
<td>Город №2:</td>
</tr>
<td><input type=text name=from_city value=""></td>
<td><input type=text name=to_city value=""></td>
<tr>
</tr>
</table>
<font size="4" color="blue">Укажите дополнительную информацию:</font><br>
<table align="center" style="text-align: center">
<tr>
<td>Длина маршрута:</td>
<td>Стоимость за 1 км:</td>
</tr>
<td><input type=text name=length value=""></td>
<td><input type=text name=cost_per_km value=""><br></td>
<tr>
</tr>
</table>
<input type=submit value="Сохранить">
<br>
</form>
</body>
</html>
"""

HTML_ADD_PASSENGER = """<html>
<title>Маршруты</title>
<body>
<form method=POST action="">
<h1 style="text-align: center">Добавить пассажира</h1>
<p style="text-align: center">
<font size="4" color="blue">Внесите информацию о пассажире:</font><br>
<table align="center" style="text-align: center">
<tr>
<td>Имя пассажира:</td>
<td>Маршрут:</td>
</tr>
<tr>
<td><input type=text name=pass_name value=""></td>
<td>{}</td>
</tr>
</table>
<input type=submit value="Сохранить">
<br>
</form>
</body>
</html>
"""

HTML_ROUTES_LIST = """<html>
<title>Маршруты</title>
<body>
<form method=POST action="">
<h1 style="text-align: center">Список маршрутов</h1>
<table align="center">
<tr>
<td style="color: red">Откуда:</td>
<td style="color: red">Куда:</td>
<td style="color: red">Стоимость:</td>
</tr>
{}
</table>
<p style="text-align: center">
<input type=submit value="Вернуться на главную страницу">
</form>
</body>
</html>
"""

HTML_PASSENGERS_LIST = """<html>
<title>Маршруты</title>
<body>
<form method=POST action="">
<h1 style="text-align: center">Список пассажиров</h1>
<table align="center">
<tr>
<td style="color: red">Пассажир:</td>
<td style="color: red">Маршрут:</td>
<td style="color: red">Стоимость поездки:</td>
</tr>
{}
</table>
<p style="text-align: center">
<input type=submit value="Вернуться на главную страницу">
</form>
</body>
</html>
"""