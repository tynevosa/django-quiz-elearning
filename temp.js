
  // function changeThumbnail() {
  //   const imgInputFields = document
  //     .querySelectorAll(`input[type=file]`);

  //   imgInputFields.forEach(imgInputField => {
  //     const img = document.createElement("img");
  //     img.style = "height:400px;width:auto";
  //     img.src = "{%if src %}{{ src }}{% endif %}";
  //     img.hidden = img.src != '';
  //     imgInputField.parentElement.appendChild(img);
  
  //     imgInputField
  //       .addEventListener("change", function (e) {
  //         const reader = new FileReader();
  //         reader.onload = function (e) {
  //           img.src = e.target.result;
  //           img.hidden = false;
  //         };
  //         reader.readAsDataURL(this.files[0]);
  //       });
  //   })
  // }

  // function docReady(fn) {
  //   if (document.readyState === "complete" || document.readyState === "interactive") {
  //     setTimeout(fn, 1);
  //   } else {
  //     document.addEventListener("DOMContentLoaded", fn);
  //   }
  // }
  // docReady(changeThumbnail);