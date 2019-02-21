
function format_row(obj){

html = `<tr>` +
    `<td><p> Input File:` + obj.file + `</p>` +
    `<img src=` + obj.url + ` alt="/static/images/NoImage.png" style="width:300px;height:300px;">` +
    `</td>` +
    `<td><p> Cropper File:</p>` +  + `<td>`
    `</tr>`

return html;
}


function test(){

var json_data = {};
var html_data = "";

$.ajax({
    type: 'GET',
    url: '/summary/0',
    success: function (json_data) {
    // On success code
    var receipt_images = json_data.receipt_images;
    // receipt_images
    for (var key in receipt_images) {
       if (receipt_images.hasOwnProperty(key)) {
          var obj = receipt_images[key];
             html_data = html_data + format_row(obj);
          }
       }
    // receipt_images - output
    document.getElementById("show_image_data22").innerHTML = html_data;
        }

    })


// end of function
}

test()