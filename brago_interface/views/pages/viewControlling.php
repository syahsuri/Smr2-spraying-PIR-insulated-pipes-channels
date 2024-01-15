<!DOCTYPE html>
<html class="loading" lang="en" data-textdirection="ltr">
<!-- BEGIN: Head-->

<head>
    <?php include '../content/layout/header.php'; ?>
</head>
<!-- END: Head-->

<!-- BEGIN: Body-->

<body class="vertical-layout vertical-menu 2-columns   fixed-navbar" data-open="click" data-menu="vertical-menu" data-col="2-columns">

    <!-- BEGIN: Navbar-->
    <?php include '../content/layout/navbar.php'; ?>
    <!-- END: Navbar-->


    <!-- BEGIN: Sidebar-->
    <?php include '../content/layout/sidebar.php'; ?>
    <!-- END: Sidebar-->

    <!-- BEGIN: Content-->
    <?php include '../content/controller/viewControlling_controller.php'; ?>
    <!-- END: Content-->

     <!-- BEGIN: Footer-->
    <footer class="footer footer-light navbar-border navbar-shadow" style="margin-left: auto; margin-top: 140px;">
        <?php include '../content/layout/footer.php'; ?>
    </footer>
    <!-- END: Footer-->

    <div class="sidenav-overlay"></div>
    <div class="drag-target"></div>

    <!-- BEGIN: Script.JS-->
    <?php include '../content/layout/script.php'; ?>
    <!-- BEGIN: Script.JS-->
</body>
<!-- END: Body-->

</html>