<?php
session_start();
session_unset();
session_destroy();

header("Location: ../index.php");
//change to signout - you have signed out!