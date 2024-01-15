<div class="app-content content">
    <div class="content-overlay"></div>
    <div class="content-wrapper">
        <div class="content-header row">
            <div class="content-header-left col-md-6 col-12 mb-2">
                <h3 class="content-header-title">Progression View</h3>
                <div class="row breadcrumbs-top">
                    <div class="breadcrumb-wrapper col-12">
                        <ol class="breadcrumb">
                            <li class="breadcrumb-item"><a href="index.html">View Model</a>
                            </li>
                            <li class="breadcrumb-item active">Progression View
                            </li>
                        </ol>
                    </div>
                </div>
            </div>
        </div>
        <div class="content-body">
            <!-- Form wizard with icon tabs section start -->
            <section id="icon-tabs">
                <div class="row">
                    <div class="col-12">
                        <div class="card bg-warning" style="background: linear-gradient(45deg, #FFA500, #FFA500 33.33%, #FFF 33.33%, #FFF 66.66%, #000 66.66%, #000); padding: 20px;  border-radius: 10px; color: #fff; position: relative;">
                            <div class="card-header">
                                <h4 class="card-title"><b>Progression View</b></h4>
                                <div><a class="heading-elements-toggle"><i class="la la-ellipsis-h font-medium-3"></i></a></div>
                                <div class="heading-elements">
                                    <ul class="list-inline mb-0">
                                        <li><a data-action="collapse"><i class="ft-minus"></i></a></li>
                                        <li><a data-action="reload"><i class="ft-rotate-cw"></i></a></li>
                                        <li><a data-action="expand"><i class="ft-maximize"></i></a></li>
                                        <li><a data-action="close"><i class="ft-x"></i></a></li>
                                    </ul>
                                </div>
                            </div>
                            <div class="card-content collapse show ">
                                <div class="card-body">
                                    <div class="container d-flex align-items-center justify-content-center">
                                        <div class="col-md-6 col-sm-12">
                                            <div class="card border-warning border-3 text-center">
                                                <div id="cardBody" class="card-body">
                                                    <h4 class="card-title">

                                                        <img src="/assets/images/warn.png" alt="element 04" width="210" class="mb-0">
                                                        <button style="display: none;" id="doneButton" class="btn btn-warning" onclick="showProgressBar()">DONE</button>
                                                    </h4>
                                                    <hr class="border-warning my-1" />
                                                    <div style="display: none;" id="buttons" class="form-group text-center">
                                                        <button class="btn btn-float btn-round btn-float-lg btn-danger" onclick="conveyerBckwrd()"><i class="la ft-chevrons-left"></i></button>
                                                        <button class="btn btn-float btn-round btn-float-lg btn-warning" onclick="rotate()"><i class="la ft-refresh-ccw"></i></button>
                                                        <button class="btn btn-float btn-round btn-float-lg btn-danger" onclick="conveyerFrwd()"><i class="la ft-chevrons-right"></i></button>
                                                    </div>
                                                    <button id="firstSection" class="btn btn-warning" type="button" disabled>
                                                        <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                                                        LOAD THE PRODUCT
                                                    </button>
                                                    <div id="status duct" class="form-group text-center">

                                                    </div>
                                                    <!-- <button type="button" class="btn btn-float btn-square btn-float-lg btn-outline-danger" onclick="stopThings()"><i class="la ft-slash"></i></button>
                                                    <button type="button" class="btn btn-float btn-square btn-float-lg btn-outline-danger" onclick="push()"><i class="la ft-activity"></i></button>
                                                    <button type="button" class="btn btn-float btn-square btn-float-lg btn-outline-danger" onclick="rotateHome()"><i class="la ft-activity">rotate home</i></button>
                                                    <button type="button" class="btn btn-float btn-square btn-float-lg btn-outline-danger" onclick="magnet()"><i class="la ft-activity">magnet</i></button> -->
                                                </div>
                                                <div class="card-body progress-div" style="display: none;">
                                                    <div class="card">
                                                        <div class="card-body">
                                                            <h4 class="card-title">Progression POV:</h4>
                                                            <!-- video start-->
                                                            <div id="camera-container">
                                                                <video id="camera" width="100%" height="auto" autoplay playsinline></video>
                                                            </div>
                                                            <!-- video end -->
                                                        </div>
                                                    </div>
                                                    <hr class="border-light my-2" />
                                                    <div class="progress" style="height: 18px;">
                                                        <div id="progressBar" class="progress-bar progress-bar-striped bg-success" role="progressbar" aria-valuenow="20" aria-valuemin="20" aria-valuemax="100" style="width:20%;"></div>
                                                    </div>
                                                </div>
                                                <div id="finishbutton" class="card-body" style="display: none;">
                                                    <h4 class="card-title">

                                                    </h4>
                                                    <img src="/assets/images/warn.png" alt="element 04" width="210" class="mb-1">
                                                    <button style="display: none;" id="doneButton" class="btn btn-success" onclick="finish()">FINISH</button>
                                                    <hr class="border-warning my-1" />
                                                    <div style="display: none;" id="buttons" class="form-group text-center">
                                                        <button class="btn btn-float btn-round btn-float-lg btn-danger" onclick="conveyerBckwrd()"><i class="la ft-chevrons-left"></i></button>
                                                        <button class="btn btn-float btn-round btn-float-lg btn-warning" onclick="rotate()"><i class="la ft-refresh-ccw"></i></button>
                                                        <button class="btn btn-float btn-round btn-float-lg btn-danger" onclick="conveyerFrwd()"><i class="la ft-chevrons-right"></i></button>
                                                    </div>
                                                    <button id="unloadButton" class="btn btn-success" type="button" disabled onclick="unload()">
                                                        <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                                                        UNLOAD THE PRODUCT
                                                    </button>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
        </div>
        </section>
        <!-- Form wizard with icon tabs section end -->
    </div>
</div>

<script>
    const address = "127.0.0.1";
    const portServer = 8080;
    // Construct the WebSocket URL using the provided address and port
    const socket = new WebSocket(`ws://${address}:${portServer}`);

    // Event listener for when the WebSocket connection is open
    socket.addEventListener('open', (event) => {
        console.log('WebSocket connection opened');
    });

    // Event listener for when a message is received from the WebSocket server
    socket.addEventListener('message', (event) => {
        console.log('Message from server:', event.data);
    });

    // Event listener for when the WebSocket connection is closed
    socket.addEventListener('close', (event) => {
        console.log('WebSocket connection closed');
    });

    // Function to send a message through WebSocket when the button is clicked
   
    // function magnet() {
    //     // Replace 'your-message-here' with the actual message you want to send
    //     const message = "\x00\x20";
    //     // Send the message to the WebSocket server
    //     socket.send("[6]" + message);

    //     console.log('Message sent:', message);
    // }

    function conveyerBckwrd() {
        // Replace 'your-message-here' with the actual message you want to send
        const message = "\x00\x10";
        // Send the message to the WebSocket server
        socket.send("[6]" + message);

        console.log('Message sent:', message);
    }

    function push() {
        // Replace 'your-message-here' with the actual message you want to send
        const message = "\x00\x40";
        // Send the message to the WebSocket server
        socket.send("[6]" + message);

        console.log('Message sent:', message);
    }

    function rotate() {
        // Replace 'your-message-here' with the actual message you want to send
        const message = "end";
        // Send the message to the WebSocket server
        socket.send("[5]" + message);

        console.log('Message sent:', message);
    }

    function unload() {
        // Send message "end"
        const message = "end"
        socket.send("[5]" + message);

        // Show loading SweetAlert
        Swal.fire({
            title: 'Loading',
            text: 'Please wait...',
            allowOutsideClick: false,
            showConfirmButton: false,
            showCancelButton: true,
            confirmButtonText: 'OK',
            cancelButtonText: 'OK',
            onBeforeOpen: () => {
                Swal.showLoading();
            }
        }).then((result) => {
            // Handle the result after the user clicks the OK button
            if (result.isConfirmed) {
                // You can add additional logic here
                console.log('User clicked OK');
            } else {
                // Handle the case when the user clicks Cancel or outside the SweetAlert
                console.log('User clicked Cancel or closed the dialog');
            }
        });
    }
    // function rotateHome() {
    //     // Toggle the state variable
    //     turnTableHome = "\x04\x00"
    //     turnTabledisable = "\x00\x00"

    //     // Determine the message based on the state
    //     const message = turnTableHome;

    //     // Send the message to the WebSocket server
    //     socket.send("[6]" + message);

    //     console.log('Message sent:', message);
    // }

    // function stopThings() {
    //     // Replace 'your-message-here' with the actual   message you want to send
    //     const message = "\x00\x00";
    //     // Send the message to the WebSocket server
    //     socket.send("[6]" + message);

    //     console.log('Message sent:', message);
    // }

    // Assuming you have a WebSocket connection (`socket` object)

    // Event listener for WebSocket messages

    socket.addEventListener('message', function(event) {
        let receivedMessage = event.data;

        if (receivedMessage.includes("finish")) {
            // Redirect to the main.php page when "finishButton" is received
            window.location.href = '../main.php';
        } else if (receivedMessage.includes("sensorsDONE")) {
            showProgressBar();
        }
    });

    function showProgressBar() {

        // const startMessage = "";

        // // Send the start message to the WebSocket server
        // socket.send("[5]" + startMessage);

        // console.log('Message sent:', startMessage);

        // Get the elements
        let cardBody = document.getElementById('cardBody');
        let button = document.getElementById('doneButton');
        let progressBarContainer = document.querySelector('.progress-div');

        // Hide the card-body div
        cardBody.style.display = 'none';

        // Toggle the display property of the progress bar container
        progressBarContainer.style.display = 'block';

        // Disable the "DONE" button to prevent multiple clicks
        button.disabled = true;

        // Update the progress bar when "sidedone" is received
        let progress = 0; // initial progress value
        let interval; // declare interval globally

        socket.addEventListener('message', function(event) {
            let receivedMessage = event.data;

            if (receivedMessage.includes("sidedone")) {
                // Increment progress by 25% for each "sidedone" message
                progress += 25;

                // Update the progress bar immediately
                updateProgressBar();

                // If interval is already set, clear it and restart
                if (interval) {
                    clearInterval(interval);
                }

                // Set interval to simulate progress update every second
                interval = setInterval(function() {
                    if (progress < 100) {
                        // Update the progress bar
                        updateProgressBar();
                    } else {
                        // If progress reaches 100%, clear the interval
                        clearInterval(interval);
                    }
                }, 1000);
            }
        });

        // Function to update the progress bar
        function updateProgressBar() {
            let progressBar = document.getElementById('progressBar');
            let currentProgress = parseInt(progressBar.getAttribute('aria-valuenow'));

            // Set the new progress value and update the width of the progress bar
            progressBar.setAttribute('aria-valuenow', progress);
            progressBar.style.width = progress + '%';

            if (progress >= 100) {
                // If progress reaches 100%, clear the interval
                clearInterval(interval);

                Swal.fire({
                    icon: 'success',
                    title: 'Spraying is Complete',
                    showConfirmButton: false,
                    timer: 1500
                }).then(() => {
                    // After a delay of 4 seconds, send another message
                    setTimeout(() => {
                        const additionalMessage = "end";
                        socket.send("[5]" + additionalMessage);
                    }, 7000);
                }).then(() => {
                    setTimeout(() => {
                        Swal.fire({
                            imageUrl: '/assets/images/press2buttonwarning.png',
                            title: 'Press and hold',
                            text: 'Until Carrier Is Fully Inside Robot Cell',
                            imageWidth: 300, // Adjust the width of the image as needed
                            imageHeight: 300, // Adjust the height of the image as needed
                            showConfirmButton: false, // Remove the "OK" button
                            customClass: {
                                image: 'custom-swal-image',
                            },
                        }).then((result) => {
                            if (result.isConfirmed) {

                            }
                        });
                    }, 30000)

                });


                let button = document.getElementById('doneButton');
                button.disabled = false;

                let unloadButton = document.getElementById('unloadButton');
                unloadButton.disabled = false;
                unloadButton.innerHTML = 'UNLOAD THE PRODUCT';

                let progressDiv = document.querySelector('.progress-div');
                let finishButtonDiv = document.getElementById('finishbutton');

                progressDiv.style.display = 'none';
                finishButtonDiv.style.display = 'block';
            }

        }

    }

    function finish() {
        window.location.href = '../main.php'; // Replace with your desired page URL

    }

    document.addEventListener('DOMContentLoaded', function() {
        const cameraContainer = document.getElementById('camera-container');
        const camera = document.getElementById('camera');

        // Check if getUserMedia is supported
        if (navigator.mediaDevices && navigator.mediaDevices.enumerateDevices) {
            // Enumerate devices and find the desired camera
            navigator.mediaDevices.enumerateDevices()
                .then(function(devices) {
                    const videoDevices = devices.filter(device => device.kind === 'videoinput');

                    if (videoDevices.length > 1) {
                        // Use the second camera (change the index as needed)
                        const selectedDeviceId = videoDevices[0].deviceId;

                        // Access the user's camera with the specified deviceId
                        navigator.mediaDevices.getUserMedia({
                                video: {
                                    deviceId: {
                                        exact: selectedDeviceId
                                    }
                                }
                            })
                            .then(function(stream) {
                                // Attach the camera stream to the video element
                                camera.srcObject = stream;
                            })
                            .catch(function(error) {
                                console.error('Error accessing camera:', error);
                            });
                    } else {
                        console.error('No additional cameras found.');
                    }
                })
                .catch(function(error) {
                    console.error('Error enumerating devices:', error);
                });
        } else {
            console.error('getUserMedia or enumerateDevices is not supported on this browser.');
        }
    });
</script>