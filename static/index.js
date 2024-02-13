
let copyURL = () => {
    //Gets the Text from the HTML
    let text = document.getElementById('shortURL')

    //Copy the text to the clipboard, it needs to in a secure environment to work
    navigator.clipboard.writeText(text.innerText)

    alert('URL Copied!:' + text.innerText)
}
