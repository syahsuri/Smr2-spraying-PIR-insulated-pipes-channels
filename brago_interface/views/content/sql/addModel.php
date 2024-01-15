<?php
// addModel.php

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $name = $_POST['name'];

    $imgModel = uploadFile('img_model', 'img-model/', ['jpg', 'jpeg', 'png', 'gif']);
    $imgOrientation = uploadFile('img_orientation', 'img-orientation/', ['jpg', 'jpeg', 'png', 'gif']);
    $stlName = uploadFile('stl_name', 'stl-files/', ['stl', 'STL']);

    if ($imgModel !== null && $imgOrientation !== null && $stlName !== null) {
        $db =  new mysqli('localhost', 'root', '', 'DB_brago');

        if ($db->connect_error) {
            die('Connection failed: ' . $db->connect_error);
        }

        $sql = "INSERT INTO tb_qrcode (name, img_model, img_orientation, stl_name) VALUES (?, ?, ?, ?)";
        $stmt = $db->prepare($sql);

        $stmt->bind_param("ssss", $name, $imgModel, $imgOrientation, $stlName);

        if ($stmt->execute()) {
            $stmt->close();
            $db->close();

            // Redirect to a success page or perform other actions
            header('Location: success_page.php');
            exit();
        } else {
            // Handle database insertion error
            echo 'Error inserting data into the database.';
        }
    } else {
        // Handle file upload errors
        echo 'Error uploading one or more files.';
    }
} else {
    // Invalid request
    http_response_code(400);
    echo 'Invalid request';
}

function uploadFile($fileInputName, $targetFolder, $allowedFileTypes)
{
    // Get the root directory of the web server
    $targetDir = '../uploads/' . $targetFolder;

    $originalFileName = basename($_FILES[$fileInputName]['name']);
    $uploadOk = 1;
    $imageFileType = strtolower(pathinfo($originalFileName, PATHINFO_EXTENSION));

    // Construct the correct destination path with DIRECTORY_SEPARATOR
    $targetFile = $targetDir . DIRECTORY_SEPARATOR . $originalFileName;

    // Check file size (adjust as needed)
    if ($_FILES[$fileInputName]['size'] > 500000) {
        echo 'Sorry, your file is too large.';
        $uploadOk = 0;
    }

    // Allow certain file formats (adjust as needed)
    if (!in_array($imageFileType, $allowedFileTypes)) {
        echo 'Sorry, only ' . implode(', ', $allowedFileTypes) . ' files are allowed.';
        $uploadOk = 0;
    }

    // Check if $uploadOk is set to 0 by an error
    if ($uploadOk == 0) {
        echo 'Sorry, your file was not uploaded.';
    } else {
        // Ensure the target directory exists
        if (!is_dir($targetDir)) {
            mkdir($targetDir, 0777, true);
        }

        // Construct the correct destination path with DIRECTORY_SEPARATOR
        $correctTargetFile = $targetDir . DIRECTORY_SEPARATOR . $originalFileName;

        // if everything is ok, try to upload file
        if (move_uploaded_file($_FILES[$fileInputName]['tmp_name'], $correctTargetFile)) {
            // Return the original filename for successful upload
            return $originalFileName;
        } else {
            // Return null for upload failure
            return null;
        }
    }

    return null;
}
