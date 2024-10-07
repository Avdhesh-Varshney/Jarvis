async function summarizeText() {
    const inputText = document.getElementById("inputText").value;
    const summaryTextElement = document.getElementById("summaryText");
    const spinner = document.getElementById("spinner");

    // Clear any previous summary and show the spinner
    summaryTextElement.innerText = '';
    spinner.classList.remove("hidden");

    if (!inputText.trim()) {
        alert("Please enter some text to summarize.");
        spinner.classList.add("hidden");  // Hide spinner if input is invalid
        return;
    }

    try {
        const response = await fetch('http://localhost:5000/summarize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: inputText }),
        });

        const data = await response.json();

        // Hide the spinner and show the summary
        spinner.classList.add("hidden");
        summaryTextElement.innerText = data.summary;

    } catch (error) {
        console.error('Error:', error);
        alert('There was an error summarizing the text.');
        spinner.classList.add("hidden");  // Hide spinner on error
    }
}
