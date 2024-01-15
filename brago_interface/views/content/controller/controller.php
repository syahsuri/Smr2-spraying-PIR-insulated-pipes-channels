<div class="app-content content">
    <div class="content-overlay"></div>
    <div class="content-wrapper">
        <div class="content-header row">
            <div class="content-header-left col-md-6 col-12 mb-2">
                <h3 class="content-header-title">Start Menu</h3>
                <div class="row breadcrumbs-top">
                    <div class="breadcrumb-wrapper col-12">
                        <ol class="breadcrumb">
                            <li class="breadcrumb-item"><a href="main.php">Home</a>
                            </li>
                            <li class="breadcrumb-item active">Start Menu
                            </li>
                        </ol>
                    </div>
                </div>
            </div>
        </div>
        <div class="content-body">

            <!-- Active Orders -->
            <div class="row">
                <div class="col-12">
                    <div class="card">
                        <div class="card-header">
                            <h4 class="card-title">Controller</h4>
                            <a class="heading-elements-toggle"><i class="la la-ellipsis-v font-medium-3"></i></a>
                            <div class="heading-elements">
                                <ul class="list-inline mb-0">
                                    <li><a data-action="collapse"><i class="ft-minus"></i></a></li>
                                    <li><a data-action="reload"><i class="ft-rotate-cw"></i></a></li>
                                    <li><a data-action="expand"><i class="ft-maximize"></i></a></li>
                                </ul>
                            </div>
                        </div>
                        <div class="card-content">
                            <!-- Floating Buttons start-->
                            <section id="floating-point">
                                <div class="row">
                                    <div class="col-12">
                                        <div class="card">
                                            <div class="card-content collapse show">
                                                <div class="card-body">
                                                    <div class="row">
                                                        <div class="form-group mx-auto" style="width: 300px;">
                                                        </div>
                                                    </div>
                                                    <div class="row">
                                                        <div class="col-xl-4 col-lg-12 mb-1">
                                                        </div>
                                                        <div class="col-xl-4 col-lg-12 mb-1">
                                                            <div class="form-group text-center">
                                                                <!-- Floating button Regular with text -->
                                                                <a href="/views/pages/viewModelList.php" class="btn btn-float btn-cyan"><i class="la ft-plus-circle"></i><span>add data</span></a>
                                                                <a href="#" class="btn btn-float btn-float-lg btn-pink" style="width: 100px;" onclick="startFunction()"><i class="la ft-power"></i><span>START</span></a>
                                                                <a href="#" class="btn btn-float btn-cyan"><i class="la la-refresh" onclick="refresh()"></i><span>refresh</span></a>
                                                            </div>
                                                        </div>
                                                        <div class="col-xl-4 col-lg-12 mb-">
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </section>
                            <!-- Floating Buttons end -->
                        </div>
                    </div>
                </div>
            </div>
            <!-- Active Orders -->

        </div>
    </div>

    <script>
        function startFunction() {
            // WebSocket connection
            const socket = new WebSocket('ws://localhost:8080');

            socket.onopen = function() {
                console.log('WebSocket connection opened');
                const message = "start"
                // Send the initial message to the WebSocket
                socket.send("[5]"+message); // Replace with the actual model name received
            };
            // Display the initial scanning SweetAlert
            const scanningAlert = Swal.fire({
                title: 'Scan QR Code',
                text: 'Please scan the QR code to proceed.',
                iconHtml: '<i class="la la-qrcode font-large-4"></i>',
                allowOutsideClick: false,
                showCancelButton: true,
                cancelButtonText: 'Cancel',
                didOpen: () => {
                    Swal.showLoading();
                },
            });

            // WebSocket connection
            const ws = new WebSocket('ws://localhost:8080');

            ws.onopen = function() {
                console.log('WebSocket connection opened');
            };

            ws.onmessage = async function(event) {
                const modelName = event.data;

                // Close the initial scanning SweetAlert
                scanningAlert.close();

                try {
                    // Send an HTTP request to the server-side script with the model name
                    const response = await fetch('content/sql/checkModel.php?modelName=' + encodeURIComponent(modelName));
                    const data = await response.json();

                    if (data.error) {
                        // If an error occurred (model not found), show an error message
                        Swal.fire('Model Not Found', data.error, 'error');
                    } else {
                        // If the model exists, display the information
                        Swal.fire({
                            title: 'Model Information',
                            html: `Model Name: ${data.name}<br>ID: ${data.id}<br>Img Model: ${data.img_model}<br>Img Orientation: ${data.img_orientation}`,
                            icon: 'info',
                        }).then((result) => {
                            // Store the data in localStorage
                            localStorage.setItem('scannedData', JSON.stringify(data));

                            const ws = new WebSocket('ws://localhost:8080');

                            ws.onopen = function() {
                                console.log('WebSocket connection opened');

                                // Send the model name to the WebSocket
                                ws.send("[5]" + data.stl_name);

                                // Close the WebSocket connection
                                ws.close();

                                // Redirect to the "View Model" page
                                window.location.href = '/views/pages/viewModel.php';
                            };
                        });
                    }
                } catch (error) {
                    console.error('Error checking model:', error);
                }

                // Close the WebSocket connection after processing the message
                ws.close();
            };

            ws.onclose = function() {
                console.log('WebSocket connection closed');
            };

            // Cancel the operation if the "Cancel" button is clicked
            scanningAlert.then((result) => {
                if (result.dismiss === Swal.DismissReason.cancel) {
                    Swal.fire('Cancelled', 'The process was cancelled.', 'error');
                    ws.close(); // Close the WebSocket connection if cancelled
                }
            });
        }
    </script>