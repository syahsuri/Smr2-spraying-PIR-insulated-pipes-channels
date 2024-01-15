<?php
session_start();
?>

<!-- Place this where you want the alert to appear -->
<?php if (isset($_SESSION['login_message']) && isset($_SESSION['login_alert_type'])) : ?>
    <div class="alert round bg-<?php echo $_SESSION['login_alert_type']; ?> alert-icon-left alert-arrow-left alert-dismissible mb-2" role="alert">
        <span class="alert-icon"><i class="la la-<?php echo ($_SESSION['login_alert_type'] === 'success') ? 'thumbs-o-up' : 'thumbs-o-down'; ?>"></i></span>
        <button type="button" class="close" data-dismiss="alert" aria-label="Close">
            <span aria-hidden="true">&times;</span>
        </button>
        <strong><?php echo ucfirst($_SESSION['login_alert_type']); ?>!</strong> <?php echo $_SESSION['login_message']; ?>
    </div>
<?php
    unset($_SESSION['login_message']);
    unset($_SESSION['login_alert_type']);
endif;
?>

<!DOCTYPE html>
<html class="loading" lang="en" data-textdirection="ltr">

<!-- BEGIN: Head-->

<head>
    <?php include 'content/login-layout/header.php'; ?>
</head>
<!-- END: Head-->

<!-- BEGIN: Body-->

<body class="vertical-layout vertical-menu 1-column   blank-page" data-open="click" data-menu="vertical-menu" data-col="1-column">
    <!-- BEGIN: Content-->
    <div class="app-content content">
        <div class="content-overlay"></div>
        <div class="content-wrapper">
            <div class="content-header row">
            </div>
            <div class="content-body">
                <section class="row flexbox-container">
                    <div class="col-12 d-flex align-items-center justify-content-center">
                        <div class="col-lg-4 col-md-8 col-10 box-shadow-2 p-0">
                            <div class="card border-grey border-lighten-3 m-0">
                                <div class="card-header border-0">
                                    <div class="card-title text-center">
                                        <div class="p-1">
                                            <h3 class="brand-text"><i class="fa-solid fa-spray-can-sparkles"></i> Brago Interface</h3>
                                        </div>
                                    </div>
                                    <h6 class="card-subtitle line-on-side text-muted text-center font-small-3 pt-2"><span><b>Login</b></span>
                                    </h6>
                                </div>
                                <div class="card-content">
                                    <div class="card-body">
                                        <form class="form-horizontal form-simple" action="/views/content/sql/process_login.php" method="post" novalidate>
                                            <fieldset class="form-group position-relative has-icon-left mb-0">
                                                <input type="text" class="form-control" id="user-name" name="username" placeholder="Username" required>
                                                <div class="form-control-position">
                                                    <i class="la la-user"></i>
                                                </div>
                                            </fieldset>
                                            <fieldset class="form-group position-relative has-icon-left">
                                                <input type="password" class="form-control" id="user-password" name="password" placeholder="Password" required>
                                                <div class="form-control-position">
                                                    <i class="la la-key"></i>
                                                </div>
                                            </fieldset>
                                            <button type="submit" class="btn btn-info btn-block"><i class="ft-unlock" onclick="login()"></i> Login</button>
                                        </form>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>
            </div>
        </div>
    </div>

    <!-- END: Content-->

    <!-- END: Content-->
    <?php include 'content/login-layout/script.php'; ?>
    <!-- END: Content-->
</body>
<!-- END: Body-->


</html>