<div class="app-content content">
    <div class="content-overlay"></div>
    <div class="content-wrapper">
        <div class="content-header row">
            <div class="content-header-left col-md-6 col-12 mb-2">
                <h3 class="content-header-title">Divice Controller</h3>
                <div class="row breadcrumbs-top">
                    <div class="breadcrumb-wrapper col-12">
                        <ol class="breadcrumb">
                            <li class="breadcrumb-item"><a href="main.php">Home</a>
                            </li>
                            <li class="breadcrumb-item active">Divice Controller
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
                            <h4 class="card-title">Divice Controller</h4>
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
                                                                <div class="card border-warning border-3 text-center">
                                                                    <div id="cardBody" class="card-body">
                                                                        <div style="display: block;" class="form-group text-center">
                                                                            <button class="btn btn-float btn-round btn-float-lg btn-danger" onclick="conveyerFrwd()"><i class="la ft-chevrons-up"></i></button>
                                                                        </div>
                                                                        <hr class="border-warning my-1" />
                                                                        <div style="display: block;" class="form-group text-center">
                                                                            <button class="btn btn-float btn-round btn-float-lg btn-danger" onclick="rotateHome()"><i class="la ft-refresh-cw"></i></button>
                                                                            <button class="btn btn-float btn-round btn-float-lg btn-danger" onclick="rotate90degree()"><i class="la ft-rotate-cw"></i></button>
                                                                        </div>
                                                                        <hr class="border-warning my-1">
                                                                        <div style="display: block;" class="form-group text-center">
                                                                            <button class="btn btn-float btn-float-lg btn-danger" onclick="carrierBack()"><i class="la ft-package"></i></button>
                                                                        </div>
                                                                        <div id="status duct" class="form-group text-center">
                                                                        </div>
                                                                    </div>
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
    </div>\
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

    function conveyerFrwd() {
        // Replace 'your-message-here' with the actual message you want to send
        const message = "start";
        // Send the message to the WebSocket server
        socket.send("[2]" + message);

        console.log('Message sent:', message);
    }

    function carrierBack() {
        // Replace 'your-message-here' with the actual message you want to send
        const message = "ready";
        // Send the message to the WebSocket server
        socket.send("[2]" + message);

        console.log('Message sent:', message);
    }

    function rotate90degree() {
        // Replace 'your-message-here' with the actual message you want to send
        const message = "rotate";
        // Send the message to the WebSocket server
        socket.send("[2]" + message);

        console.log('Message sent:', message);
    }

    function rotateHome() {
        // Replace 'your-message-here' with the actual message you want to send
        const message = "turntable";
        // Send the message to the WebSocket server
        socket.send("[2]" + message);

        console.log('Message sent:', message);
    }
</script>