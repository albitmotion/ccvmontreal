// Text
const textInput = document.getElementById("text");
const quotaDiv = document.getElementById("quotaDiv");
quotaDiv.innerHTML = textInput.value;

textInput.onchange = function() {
    quotaDiv.innerHTML = textInput.value;
};


// Author
const authorInput = document.getElementById("author");
const quoteAuthor = document.getElementById("quoteAuthor");
quoteAuthor.innerHTML = authorInput.value;
authorInput.onchange = function() {
    quoteAuthor.innerHTML = authorInput.value;
};

// Organization
const organizationInput = document.getElementById("organization");
const quoteOrganization = document.getElementById("quoteOrganization");
quoteOrganization.innerHTML = organizationInput.value;
organizationInput.onchange = function() {
    quoteOrganization.innerHTML = organizationInput.value;
};

// Font-size
const fontSizeInput = document.getElementById("fontSize");
quotaDiv.style.fontSize = fontSizeInput.value + "px";
fontSizeInput.onchange = function() {
    quotaDiv.style.fontSize = fontSizeInput.value + "px";
};
