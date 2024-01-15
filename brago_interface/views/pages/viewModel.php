<!DOCTYPE html>
<html class="loading" lang="en" data-textdirection="ltr">
<!-- BEGIN: Head-->

<head>
    <style>
        #orientation-card {
            transition: background-color 0.5s ease;
            /* Adjust the duration and easing as needed */
        }

        .bg-success {
            background-color: green;
            /* You can set your desired success color */
        }
    </style>
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
    <?php include '../content/controller/viewModel_controller.php'; ?>
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