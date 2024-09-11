from flask import Flask, render_template, request
import nmap

app = Flask(__name__)

# Create an instance of the PortScanner class from the nmap module
nm = nmap.PortScanner()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    target = request.form['target']
    scan_type = request.form['scan_type']
    port_selection = request.form['port_selection']
    custom_ports = request.form.get('custom_ports', '')

    # Determine scan arguments based on scan type
    if scan_type == 'quick':
        scan_args = '-T4 -F'
    elif scan_type == 'full':
        scan_args = '-T4 -p-'
    elif scan_type == 'service':
        scan_args = '-T4 -sV'
    else:
        scan_args = ''

    # Add port arguments based on user selection
    if port_selection == 'top10':
        if scan_type == 'quick':
            scan_args = '-T4 -F'  # `-F` already includes common ports
        else:
            scan_args += ' -p 1,7,9,13,19,23,25,53,80,110'
    elif port_selection == 'top100':
        if scan_type == 'quick':
            scan_args = '-T4 -F'  # `-F` already includes common ports
        else:
            scan_args += ' -p ' + ','.join(map(str, range(1, 101)))
    elif port_selection == 'top1000':
        if scan_type == 'quick':
            scan_args = '-T4 -F'  # `-F` already includes common ports
        else:
            scan_args += ' -p ' + ','.join(map(str, range(1, 1001)))
    elif port_selection == 'custom' and custom_ports:
        if scan_type == 'quick':
            scan_args = '-T4 -F'  # `-F` already includes common ports
        else:
            scan_args += ' -p ' + custom_ports

    print(f"Running nmap scan with arguments: {scan_args}")

    try:
        nm.scan(hosts=target, arguments=scan_args)

        # Check if the target is in the scan results
        if target in nm.all_hosts():
            scan_results = nm[target]
            print(f"Scan results for {target}: {scan_results}")
            formatted_results = []
            for proto in scan_results.all_protocols():
                for port, info in scan_results[proto].items():
                    formatted_results.append({
                        'protocol': proto,
                        'port': port,
                        'state': info['state']
                    })
        else:
            print(f"Target {target} not found in scan results.")
            formatted_results = [{'protocol': 'N/A', 'port': 'N/A', 'state': 'No results found'}]
    except Exception as e:
        formatted_results = [{'protocol': 'N/A', 'port': 'N/A', 'state': 'Error occurred'}]
        print(f"Error during scan: {e}")

    print(f"Formatted results: {formatted_results}")

    return render_template('scan_results.html', results=formatted_results)

@app.route('/help')
def help():
    return render_template('help.html')

if __name__ == '__main__':
    app.run(debug=True)
