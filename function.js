async function setData() {
    try {
        const response = await fetch('/set_data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ key: 'name', value: 'ODH User' })
        });

        if (response.ok) {
            const data = await response.json();
            document.getElementById('output').innerText = data.message;
        } else {
            document.getElementById('output').innerText = 'Error setting data';
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('output').innerText = 'Error setting data';
    }
}

async function getData() {
    try {
        const response = await fetch('/get_data?key=name', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const data = await response.json();
            document.getElementById('output').innerText = 'Data: ' + data.value;
        } else {
            document.getElementById('output').innerText = 'Error getting data';
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('output').innerText = 'Error getting data';
    }
}

async function clearData() {
    try {
        const response = await fetch('/clear_data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const data = await response.json();
            document.getElementById('output').innerText = data.message;
        } else {
            document.getElementById('output').innerText = 'Error clearing data';
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('output').innerText = 'Error clearing data';
    }
}
