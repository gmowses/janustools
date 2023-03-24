from flask import Flask, render_template, request
from werkzeug.datastructures import CombinedMultiDict
import dns.resolver

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/qos', methods=['GET', 'POST'])
def qos():
    output = None
    if request.method == 'POST':
        form_data = CombinedMultiDict((request.files, request.form))
        down = form_data['down']
        up = form_data['up']
        interface = form_data['interface']

        downkbps = (int(down)) * 1024
        upkbps = (int(up)) * 1024

        if interface == "":
            output = f"qos car cir {downkbps} cbs 1250000 green pass red discard inbound\nqos car cir {upkbps} cbs 1250000 green pass red discard outbound"
        else:
            output = f"qos car cir {downkbps} cbs 1250000 green pass red discard inbound vlan {interface}\nqos car cir {upkbps} cbs 1250000 green pass red discard outbound vlan {interface}"

    return render_template('qos.html', output=output)

@app.route('/whois', methods=['GET', 'POST'])
def whois():
    disabled = False
    output = ''

    if request.method == 'POST':
        try:
            asn_number = request.form['asn_number']
            result = dns.resolver.resolve(f'AS{asn_number}.asn.cymru.com', 'TXT')
            output = str(result[0]).split("|")[4].strip()[:-1]
        except dns.resolver.NXDOMAIN:
            output = 'Error: Domain not found'
        except Exception as e:
            output = f'Error: {str(e)}'

    return render_template('whois.html', disabled=disabled, output=output)

if __name__ == '__main__':
    app.run(debug=True)
