//preview cheque
function previewFile(input) {
  var file = $("#chequeImage").get(0).files[0];
  if (file) {
    var reader = new FileReader();
    reader.onload = function () {
      $("#previewImg").attr("src", reader.result);
    };
    reader.readAsDataURL(file);
  }
}

$(document).ready(function () {
  $("#loader")[0].style.visibility = "hidden";
  $("#submitCheque").click(function () {
    var chequeImage = document.getElementById("chequeImage");

    // no cheque providee
    if (chequeImage.files.length === 0) {
      console.log("empty file");
      Swal.fire({
        icon: "error",
        title: "Oops...",
        text: "Cheque image is not provided!",
      });
    } else {
      // has cheque
      var formData = new FormData();
      var cheque = $("#chequeImage")[0].files[0];
      formData.append("cheque", cheque);
      $.ajax({
        url: "/dashboard/validate-cheque",
        type: "post",
        data: formData,
        beforeSend: function () {
          $("#loader")[0].style.visibility = "visible";
        },
        contentType: false,
        processData: false,
        success: function (response) {
          if (response != 0) {
            if (response.status === "true") {
              Swal.fire({
                icon: "success",
                title: "Congratulations!",
                text: response.output,
              });
            } else {
              Swal.fire({
                icon: "error",
                title: "Error",
                text: response.output,
              });
            }
          } else {
            Swal.fire({
              icon: "error",
              title: "Error",
              text: "Your cheque is not verified. Please upload a valid cheque or try again later",
            });
          }
          $("#loader")[0].style.visibility = "hidden";
        },
      });
    }
  });
});
