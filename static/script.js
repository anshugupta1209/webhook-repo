async function fetchEvents() {
    const res = await fetch('/data');
    const events = await res.json();
    const list = document.getElementById('event-list');
    list.innerHTML = '';

    events.forEach(e => {
        const li = document.createElement('li');
        if (e.type === "push") {
            li.textContent = `${e.author} pushed to ${e.from_branch} at ${new Date(e.timestamp).toLocaleString()}`;
        } else if (e.type === "pull_request") {
            li.textContent = `${e.author} created PR from ${e.from_branch} to ${e.to_branch} at ${new Date(e.timestamp).toLocaleString()}`;
        }
        list.appendChild(li);
    });
}

setInterval(fetchEvents, 15000);
fetchEvents();
