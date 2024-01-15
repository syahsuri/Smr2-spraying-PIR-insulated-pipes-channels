<?php
session_start();

// Check if the user is logged in
if (!isset($_SESSION['username'])) {
    header("Location: login.php"); // Redirect to the login page if not logged in
    exit();
}
?>

<!DOCTYPE html>
<html class="loading" lang="en" data-textdirection="ltr">
<!-- BEGIN: Head-->

<head>
    <?php include 'content/layout/header.php'; ?>
</head>
<!-- END: Head-->

<!-- BEGIN: Body-->

<body class="vertical-layout vertical-menu 2-columns   fixed-navbar" data-open="click" data-menu="vertical-menu" data-col="2-columns">

    <!-- BEGIN: Navbar-->
    <?php include 'content/layout/navbar.php'; ?>
    <!-- END: Navbar-->


    <!-- BEGIN: Sidebar-->
    <?php include 'content/layout/sidebar.php'; ?>
    <!-- END: Sidebar-->

    <!-- BEGIN: Content-->
    <?php include 'content/controller/controller.php'  ?>
    <!-- END: Content-->

    <!-- BEGIN: Footer-->
    <footer class="footer footer-light navbar-border navbar-shadow" style="margin-left: auto; margin-top: 200px;">
        <?php include 'content/layout/footer.php'; ?>
    </footer>
    <!-- END: Footer-->

    <div class="sidenav-overlay"></div>
    <div class="drag-target"></div>

    <!-- BEGIN: Script.JS-->
    <?php include 'content/layout/script.php'; ?>
    <!-- BEGIN: Script.JS-->

    <script>
        let websocket;
        const address = "127.0.0.1";
        const portServer = 8080;

        function connectWebSocket() {
            const socketUrl = `ws://${address}:${portServer}`;

            websocket = new WebSocket(socketUrl);
            const sendId = "3";
            websocket.addEventListener("open", () => {
                console.log("WebSocket connected");
                websocket.send(sendId);
            });
        }

        connectWebSocket();
    </script>
</body>
<!-- END: Body-->

</html>