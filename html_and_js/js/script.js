// Insert row function
var rows_count = 1;

$(document).ready(function() {

    $("#insert_row").click(function() {

        $('#rows' + rows_count).html("<td>" + (rows_count + 1) + "</td>" +
            "<td><input name='Layer_depth" + rows_count + "' type='text' placeholder='Layer depth'/> </td>" +
            "<td><input  name='Unit weigh" + rows_count + "' type='text' placeholder='Unit weight' ></td>" +
            "<td><input  name='Primary modulus" + rows_count + "' type='text' placeholder='Primary modulu' ></td>" +
            "<td><input  name='Secondary modulus" + rows_count + "' type='text' placeholder='Secondary modulu' ></td>");

        $('#myTable').append('<tr id="rows' + (rows_count + 1) + '"></tr>');
        rows_count++;
    });
    // Delete row function
    $("#delete_row").click(function() {
        if (rows_count > 1) {
            $("#rows" + (rows_count - 1)).html('');
            rows_count--;
        }
    });


    // Get data from table form, changing it into proper array for computing
    $("#compute").click(function() {
        var soil_data_table = document.getElementById('myTable');
        all_row_data = []
        for (var r = 1; r <= rows_count; r++) {
            for (var c = 1, m = soil_data_table.rows[r].cells.length; c < m; c++) {
                var value_from_table = Number.parseFloat(soil_data_table.rows[r].cells[c].children[0].value);
                all_row_data.push(value_from_table);
            }
        }
        var number_of_parameters = 4;
        window.soil_layers_data = []
        for (var i = 0; i < number_of_parameters; i++) {
            one_type_parameter = [];
            for (var j = i; j < all_row_data.length; j += 4) {
                one_type_parameter.push(all_row_data[j]);
            }
            soil_layers_data.push(one_type_parameter)
        }
        // Auxiliary function to display results on website;
        function updatePageWithNewResult(result) {
            updatePageData("max_depth", result.depth_affect_settlements);
            updatePageData("settlemets", result.total_settlements);

            var vertical_stresses = {
                x: result.vertical_stresses_data,
                y: result.depth_data,
                type: 'lines',
                name: 'Vertical stresses',
                fill: 'tozerox',
            };

            var excavation_stresses = {
                x: result.excavation_stresses_data,
                y: result.depth_data,
                type: 'lines',
                name: 'Stresses caused by excavation',
                fill: 'tozerox',
                line: {
                    color: 'rgb(255,124,0)',
                }

            };

            var additional_stresses = {
                x: result.additional_stresses_data,
                y: result.depth_data,
                type: 'lines',
                name: 'Additional stresses',
                fill: 'tozerox',

            };

            var data = [vertical_stresses, excavation_stresses, additional_stresses];
            var layout = {
                title: 'Stresses under concrete foundation',
                xaxis: {
                    title: 'stresses [kPa]'
                },
                yaxis: {
                    title: 'depth under foundation [m]',
                }
            };
            Plotly.newPlot('myDiv', data, layout);
        }

        function updatePageData(div_id, value) {
            var place_to_display_content = document.getElementById(div_id);
            var content = document.createTextNode(value);
            place_to_display_content.appendChild(content);
        }

        // send ajax
        $.ajax({
            url: 'http://127.0.0.1:8080/tasks',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                width: Number.parseFloat($('#width').val()),
                length: Number.parseFloat($('#length').val()),
                excavation_depth: Number.parseFloat($('#excavation_depth').val()),
                evenly_distributed_load: Number.parseFloat($('#evenly_distributed_load').val()),
                soil_layers_data: soil_layers_data,
            }),
            success: updatePageWithNewResult,

            error: function(xhr, resp, text) {
                console.log(xhr, resp, text);
            },

        })


    });
});