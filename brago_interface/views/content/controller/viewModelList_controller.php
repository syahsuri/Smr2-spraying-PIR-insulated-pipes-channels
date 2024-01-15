<div class="app-content content">
    <div class="content-overlay"></div>
    <div class="content-wrapper">
        <div class="content-header row">
            <div class="content-header-left col-md-6 col-12 mb-2">
                <h3 class="content-header-title">View Model List</h3>
                <div class="row breadcrumbs-top">
                    <div class="breadcrumb-wrapper col-12">
                        <ol class="breadcrumb">
                            <li class="breadcrumb-item"><a href="index.html">Start Menu</a>
                            </li>
                            <li class="breadcrumb-item active">View Model List
                            </li>
                        </ol>
                    </div>
                </div>
            </div>
        </div>
        <div class="content-body">

            <!-- Form wizard with icon tabs section start -->
            <!-- Zero configuration table -->
            <section id="configuration">
                <div class="row">
                    <div class="col-12">
                        <div class="card">
                            <div class="card-header">
                                <h4 class="card-title">Zero configuration</h4>
                                <a class="heading-elements-toggle"><i class="la la-ellipsis-v font-medium-3"></i></a>
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
                                <div class="card-body card-dashboard">
                                    <div class="table-responsive">
                                        <script src="https://code.jquery.com/jquery-3.6.4.min.js"></script>
                                        <button type="button" class="btn btn-info btn-min-width btn-glow  mb-1" data-toggle="modal" data-target="#iconForm">Add Model</button>
                                        <!-- Modal -->
                                        <div class="modal fade text-left" id="iconForm" tabindex="-1" role="dialog" aria-labelledby="myModalLabel34" aria-hidden="true">
                                            <div class="modal-dialog" role="document">
                                                <div class="modal-content">
                                                    <div class="modal-header">
                                                        <h3 class="modal-title" id="myModalLabel34">Add Models</h3>
                                                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                                            <span aria-hidden="true">&times;</span>
                                                        </button>
                                                    </div>
                                                    <form enctype="multipart/form-data" action="\views\content\sql\addModel.php" method="post">
                                                        <div class="modal-body">
                                                            <label>Models Name </label>
                                                            <div class="form-group position-relative has-icon-left">
                                                                <input type="text" placeholder="Models Name" class="form-control" name="name">
                                                                <div class="form-control-position">
                                                                    <i class="la la-envelope font-medium-5 line-height-1 text-muted icon-align"></i>
                                                                </div>
                                                            </div>

                                                            <label>Model Image Product</label>
                                                            <div class="custom-file position-relative ">
                                                                <input type="file" class="custom-file-input" id="inputGroupFileImage" name="img_model">
                                                                <label class="custom-file-label" for="inputGroupFileImage" aria-describedby="inputGroupFileImage">Choose file</label>
                                                            </div>

                                                            <label class="mt-2">Model Orientation</label>
                                                            <div class="custom-file position-relative">
                                                                <input type="file" class="custom-file-input" id="inputGroupFileOrientation" name="img_orientation">
                                                                <label class="custom-file-label" for="inputGroupFileOrientation" aria-describedby="inputGroupFileOrientation">Choose file</label>
                                                            </div>
    
                                                            <label class="mt-2">STL</label>
                                                            <div class="custom-file position-relative">
                                                                <input type="file" class="custom-file-input" id="inputGroupFileSTL" name="stl_name">
                                                                <label class="custom-file-label" for="inputGroupFileSTL" aria-describedby="inputGroupFileSTL">Choose file</label>
                                                            </div>

                                                        </div>
                                                        <div class="modal-footer">
                                                            <div class="modal-footer">
                                                                <input type="reset" class="btn btn-outline-secondary btn-lg" data-dismiss="modal" value="close">
                                                                <input type="submit" class="btn btn-outline-primary btn-lg" name="submit" value="Submit">
                                                            </div>
                                                        </div>
                                                    </form>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    <table id="myTable" class="table table-striped table-bordered zero-configuration">
                                        <thead>
                                            <tr>
                                                <th>No</th>
                                                <th>Name</th>
                                                <th>Model</th>
                                                <th>Orientatione</th>
                                                <th>STL</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                        <tbody>
                                            <?php
                                            // Assuming you have a database connection established
                                            require_once(__DIR__ . '/../sql/db_connection.php');
                                            // Execute the query
                                            $query = "SELECT * FROM tb_qrcode";
                                            $result = $conn->query($query);

                                            // Include the file and display the table rows
                                            require_once(__DIR__ . '/../sql/tb_qrcode.php');
                                            displayTableRows($result);
                                            ?>
                                        </tbody>
                                        </tbody>
                                        <tfoot>
                                            <tr>
                                                <th>No</th>
                                                <th>Name</th>
                                                <th>Model</th>
                                                <th>Orientatione</th>
                                                <th>STL</th>
                                            </tr>
                                        </tfoot>
                                    </table>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
        </div>
        </section>
        <!--/ Zero configuration table -->
        <!-- Form wizard with icon tabs section end -->
    </div>
</div>

<script>
    $(document).ready(function() {
        // Update the file input label with the selected file name
        $('.custom-file-input').on('change', function() {
            var fileName = $(this).val().split('\\').pop();
            $(this).next('.custom-file-label').html(fileName);
        });
    });
</script>