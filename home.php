<?php
echo "
<!DOCTYPE HTML>

<html>

  <body>

    <h1> HEROKU PHP DEPLOY </h1>

      <b> UwU </b>
      <br/>
      <b> OwO </b>

  </body>

</html>";

  $con = "dbname=da5pslrps1jns5 host=ec2-79-125-12-48.eu-west-1.compute.amazonaws.com port=5432 user=kllwqbimfzujcz password=e5996fb5d16c7abceb6cb6c922a817019b15e6ccf09851241330777a7a4d7bb4 sslmode=require";


  if (!$con)
  {
    echo "Database connection failed.";
  }
  else
  {
    echo "Database connection success.";
  }


?>
