<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>

<body>
    <form action="#">
        <input type="text" name="ciao" id="ciao">
        <input type="submit" value="ciao2">
    </form>

    <table>
        <tr>
            <th>Testo</th>
            <th>Partecipazione</th>
            <th>Quiz</th>
            <th>Domanda</th>
        </tr>
        <?php
        include_once "./connessioneDB.php";
        $sql = "SELECT * FROM RISPOSTA_UTENTE_QUIZ " . (isset($_GET["ciao"]) ? "WHERE PARTECIPAZIONE = '" . $_GET["ciao"] . "'" : "");
        echo $sql;
        $result = $connessione->query($sql);
		foreach($result as $riga) {
            echo("<p>" . implode(", ", $riga) . "</ p> \n");}
?>
    </table>

</body>

</html>