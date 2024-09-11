document.addEventListener('DOMContentLoaded', () => {
    const portSelection = document.getElementById('port_selection');
    const customPortsDiv = document.getElementById('custom_ports_div');

    portSelection.addEventListener('change', () => {
        if (portSelection.value === 'custom') {
            customPortsDiv.classList.remove('d-none');
        } else {
            customPortsDiv.classList.add('d-none');
        }
    });
});
