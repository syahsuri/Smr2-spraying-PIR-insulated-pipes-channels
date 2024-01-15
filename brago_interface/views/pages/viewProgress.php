<!DOCTYPE html>
<html class="loading" lang="en" data-textdirection="ltr">
<!-- BEGIN: Head-->

<head>
    <style>
        /* Define your custom styles here */
        .custom-swal-image {
            border-radius: 10px;
            /* Adjust the border-radius as needed */
        }
    </style>
    <?php include '../content/layout/header.php'; ?>

    <script>
        sendMessageToServer('ok');
        // Assuming you have received the message and stored it in a variable like receivedMessage

        document.addEventListener('DOMContentLoaded', function() {
            // Variable to track whether the process is ongoing
            let isProcessOngoing = false;

            // Event listener for beforeunload
            window.addEventListener('beforeunload', function(e) {
                if (isProcessOngoing) {
                    // Display a warning message
                    const confirmationMessage = 'Are you sure you want to leave? The ongoing process will be interrupted.';
                    (e || window.event).returnValue = confirmationMessage; // Standard
                    return confirmationMessage; // IE/Edge
                }
            });

            // Function to set the process status
            function setProcessStatus(ongoing) {
                isProcessOngoing = ongoing;
            }

            setProcessStatus(true);


            const sweetAlertOptions = {
                imageUrl: '/assets/images/press2buttonwarning.png',
                title: 'Press and hold',
                text: 'Until Carrier Is Fully Inside Robot Cell',
                imageWidth: 300,
                imageHeight: 300,
                showConfirmButton: false, // Remove the "OK" button
                customClass: {
                    image: 'custom-swal-image',
                },
            };

            Swal.fire(sweetAlertOptions);
            const address = "127.0.0.1";
            const portServer = 8080;
            // Construct the WebSocket URL using the provided address and port
            const socket = new WebSocket(`ws://${address}:${portServer}`);

            socket.addEventListener('message', function(event) {
                let receivedMessage = event.data;
                let card = document.getElementById('orientation-card');

                if (receivedMessage.includes('go')) {
                    // Close the SweetAlert
                    Swal.close();
                }
            });

            // Assuming you have received a "go" message from the server
        });


        // Example function to send a message to the server using WebSocket
        function sendMessageToServer(message) {
            let websocket;
            const address = "127.0.0.1";
            const portServer = 8080;

            const socket = new WebSocket(`ws://${address}:${portServer}`);

            socket.addEventListener('open', (event) => {
                // Send the message to the server
                socket.send("[5]" + message);
            });

            socket.addEventListener('close', (event) => {
                console.log('Connection closed');
            });

            socket.addEventListener('error', (event) => {
                console.error('Error occurred:', event);
            });
        }
    </script>
    <style>
        .progress-div {
            transition: opacity 0.5s ease-in-out;
        }
    </style>
</head>
<!-- END: Head-->

<!-- BEGIN: Body-->

<body class="vertical-layout vertical-menu 2-columns fixed-navbar p" data-open="click" data-menu="vertical-menu" data-col="2-columns">

    <!-- BEGIN: Navbar-->
    <?php include '../content/layout/navbar.php'; ?>
    <!-- END: Navbar-->


    <!-- BEGIN: Sidebar-->
    <?php include '../content/layout/sidebar.php'; ?>
    <!-- END: Sidebar-->

    <!-- BEGIN: Content-->
    <?php include '../content/controller/viewProgress_controller.php'; ?>
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