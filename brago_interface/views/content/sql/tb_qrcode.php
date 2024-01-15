<?php
function displayTableRows($result)
{
    if ($result->num_rows > 0) {
        $counter = 1;
        foreach ($result as $row) {
            echo '<tr>';
            echo '<td>' . $counter++ . '</td>';
            echo '<td>' . $row['name'] . '</td>';
            echo '<td>' . $row['img_model'] . '</td>';
            echo '<td>' . $row['img_orientation'] . '</td>';
            echo '<td>' . $row['stl_name'] . '</td>';
            echo '</tr>';
        }
    } 
}
