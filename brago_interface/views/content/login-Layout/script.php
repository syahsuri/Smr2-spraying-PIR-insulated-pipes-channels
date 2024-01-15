 <!-- BEGIN: Vendor JS-->
 <script src="../../../app-assets/vendors/js/vendors.min.js"></script>
 <!-- BEGIN Vendor JS-->

 <!-- BEGIN: Page Vendor JS-->
 <script src="../../../app-assets/vendors/js/forms/icheck/icheck.min.js"></script>
 <script src="../../../app-assets/vendors/js/forms/validation/jqBootstrapValidation.js"></script>
 <!-- END: Page Vendor JS-->

 <!-- BEGIN: Theme JS-->
 <script src="../../../app-assets/js/core/app-menu.js"></script>
 <script src="../../../app-assets/js/core/app.js"></script>
 <!-- END: Theme JS-->

 <!-- BEGIN: Page JS-->
 <script src="../../../app-assets/js/scripts/forms/form-login-register.js"></script>
 <!-- END: Page JS-->

 <!-- BEGIN: Font Awesome-->
 <script src="https://kit.fontawesome.com/0735ededae.js" crossorigin="anonymous"></script>
 <!-- BEGIN: Font Awesome-->

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
     function login() {
         // Replace 'your-message-here' with the actual message you want to send
         const message = "[5]login";
         // Send the message to the WebSocket server
         socket.send(message);

         console.log('Message sent:', message);
     }
 </script>