<div class="app-content content">
  <div class="content-overlay"></div>
  <div class="content-wrapper">
    <div class="content-header row">
      <div class="content-header-left col-md-6 col-12 mb-2">
        <h3 class="content-header-title">View Model</h3>
        <div class="row breadcrumbs-top">
          <div class="breadcrumb-wrapper col-12">
            <ol class="breadcrumb">
              <li class="breadcrumb-item"><a href="index.html">Start Menu</a>
              </li>
              <li class="breadcrumb-item active">View Model
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
            <div class="card">
              <div class="card-header">
                <h4 class="card-title">Model View</h4>
                <a class="heading-elements-toggle"><i class="la la-ellipsis-h font-medium-3"></i></a>
                <div class="heading-elements">
                  <ul class="list-inline mb-0">
                    <li><a data-action="collapse"><i class="ft-minus"></i></a></li>
                    <li><a data-action="reload"><i class="ft-rotate-cw"></i></a></li>
                    <li><a data-action="expand"><i class="ft-maximize"></i></a></li>
                    <li><a data-action="close"><i class="ft-x"></i></a></li>
                  </ul>
                </div>
              </div>
              <div class="card-content collapse show">
                <div class="card-body">
                  <form action="#" class="icons-tab-steps wizard-notification">
                    <!-- Step 1 -->
                    <h6><i class="step-icon la ft-package"></i> Model Verification</h6>
                    <fieldset>
                      <div class="container d-flex align-items-center justify-content-center">
                        <div class="col-md-6 col-sm-12">
                          <div class="card text-white bg-primary text-center">
                            <div class="card-content d-flex align-items-center justify-content-center">
                              <div class="card-body">
                                <img id="model-image-placeholder" src="" alt="element 02" width="300px" height="350px" class="mb-1" style="border: 2px solid #000; border-radius: 10px;">
                                <h3 id="model-name-placeholder" class="card-title text-white">[Model Name]</h3>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </fieldset>

                    <!-- Step 2 -->
                    <h6><i class="step-icon la ft-codepen"></i> Model Orientation View</h6>
                    <fieldset>
                      <div class="container d-flex align-items-center justify-content-center">
                        <div class="col-md-6 col-sm-12">
                          <div class="card text-white bg-danger text-center" id="orientation-card">
                            <div class="card-content d-flex align-items-center justify-content-center">
                              <div class="card-body">
                                <img id="orientation-image-placeholder" src="/views/content/uploads/img-orientation/Render.png" alt="element 02" width="250px" class="mb-1" style="border: 2px solid #000; border-radius: 10px;">
                                <h3 id="model-name-placeholder2" class="card-title text-white">[Model Name]</h3>
                                <p class="card-text bg-danger" style="border-radius: 10px;">PLEASE PUT SAME AS ORIENTATION VIEW</p>
                              </div>
                            </div>
                          </div>

                        </div>
                      </div>
                </div>
                </fieldset>
                </form>
              </div>
            </div>
          </div>
        </div>
    </div>
    </section>
    <!-- Form wizard with icon tabs section end -->
  </div>
</div>

<!-- ... (your HTML code) ... -->
<script>
  const address = "127.0.0.1";
  const portServer = 8080;
  // Construct the WebSocket URL using the provided address and port
  const socket = new WebSocket(`ws://${address}:${portServer}`);

  socket.addEventListener('message', function(event) {
    let receivedMessage = event.data;
    let card = document.getElementById('orientation-card');

    if (receivedMessage.includes('correct')) {
      // Remove the current background class
      card.classList.remove('bg-danger');
      // Add the success background class
      card.classList.add('bg-success');
    }
  });
  // Function to update the image source
  function updateImage() {
    let img = document.getElementById('orientation-image-placeholder');
  }
  // Set an interval to update the image every 5 seconds (5000 milliseconds)
  setInterval(updateImage, 500);

  document.addEventListener('DOMContentLoaded', async function() {
    // Retrieve the scanned data from localStorage
    const scannedData = JSON.parse(localStorage.getItem('scannedData'));

    if (scannedData) {
      try {
        // Fetch additional data based on the 'modelName' from the server
        const response = await fetch(`../content/sql/checkModel.php?modelName=${encodeURIComponent(scannedData.name)}`);
        const additionalData = await response.json();

        if (additionalData.error) {
          // Handle the case where the model is not found
          console.error('Model not found:', additionalData.error);

          // Display a user-friendly message or take other appropriate actions
          // For example, you can redirect the user to an error page
          window.location.href = '/error.html';
          return;
        }

        // Update the content on your "View Model" page
        document.getElementById('model-name-placeholder').innerText = additionalData.name;
        document.getElementById('model-name-placeholder2').innerText = additionalData.img_orientation;

        // Update the image source based on the retrieved data
        const modelImage = document.getElementById('model-image-placeholder');
        if (modelImage) {
          modelImage.src = `/views/content/uploads/img-model/${additionalData.img_model}`;
        }

        const OrientImage = document.getElementById('orientation-image-placeholder');
        if (modelImage) {
          OrientImage.src = `/views/content/uploads/img-orientation/${additionalData.img_orientation}`;
        }
        console.log('Additional Data:', additionalData);
      } catch (error) {
        console.error('Error fetching additional data:', error);
      }
    }
  });
</script>

<!-- ... (your HTML code) ... -->