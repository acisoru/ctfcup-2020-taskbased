<html>
    <head>
        <title>Resolver</title>
    </head>
    <body style="text-align: center">
        <h1>Resolver</h1>
        <form method="GET" action="/">
            Host: <input type="text" name="hostname" value="<?php 
if (isset($_GET["hostname"])) { 
    echo htmlspecialchars($_GET["hostname"]);
} else { 
    echo "google.com"; 
} 
?>">
<?php
if (isset($_GET["usecurl"])) {
    echo "            <input type=\"hidden\" name=\"usecurl\" value=\"1\">\n";
}
?>          <input type="submit" value="Resolve"> <br>
        </form>
        <textarea id="result" style="width: 1000px; height: 500px;">
<?php

if (isset($_GET["hostname"])) {
    $hostname = $_GET["hostname"];

    if (strlen($hostname) === 0) {
        die("invalid hostname\n");
    }

    if (isset($_GET["usecurl"])) {
        $program = "curl";
    } else {
        $program = "dig";
    }

    $command = "/usr/bin/" . $program . " ANY +nocmd +nocomments +nostats +noquestion +norrcomments " . $hostname;
    
    passthru(escapeshellcmd($command));
}

?>
        </textarea>
    </body>
</html>
