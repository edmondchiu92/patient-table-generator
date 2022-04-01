console.log('copy_text.js')

function copyTextFromElement(elementID) {
  let element = document.getElementById(elementID); //select the element
  let elementText = element.textContent; //get the text content from the element
  copyText(elementText); //use the copyText function below
}

function copyText(text) {
    text_trim = text.replace(/^\s+|\s+$/gm,'');
    navigator.clipboard.writeText(text_trim);
    console.log(text_trim);
}