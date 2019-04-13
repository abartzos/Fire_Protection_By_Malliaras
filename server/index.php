<!doctype html>

<html>
<head>
    <link rel="shortcut icon" type="image/icon" href=favicon.ico />
    <link rel="stylesheet" type="text/css" href="css/bootstrap.css" />
    <link rel="stylesheet" type="text/css" href="css/style.css" />
<title>Fire protection monitor</title>
</head>


<body>
    <header>
        <p class='title'>Fire protection monitor</p>
        <p>MalliarasPyrasfaleia</p>
    </header>
    <article>
        <h5>Reports</h5>
        <table>
            <tr>
                <th>Datetime</th>
                <th>Location</th>
            </tr>
            <?php
            class database extends Sqlite3 {
                function __construct($database_name) {
                    $this->open($database_name);
                }
            }
            $db = new database('db.db');
            if (!$db) {
                throw new Exception('Problem connecting to the database');
            }
            $res = $db->query('SELECT * FROM alerts');
            while ($row = $res->fetchArray()) {
                echo '<tr>';
                echo '<td>'.$row['datetime'].'</td>'
                .'<td>'.$row['location'].'</td>';
                echo '</tr>';
            }
            ?>
        </table>
    </article>
    <footer>
        Copyright &copy; MalliarasPyrasfaleia 2019<br>
    </footer>
    
    <script src="js/jquery-1.11.1.js"></script>
    <script src="js/bootstrap.js"></script>

    <!-- <script src="js/socket.io-1.2.0.js"></script> -->
    <!-- <script src='js/main.js'></script> -->
</body>
</html>
