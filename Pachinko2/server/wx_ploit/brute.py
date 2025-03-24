import requests
import json

# Set up the API endpoint
url = 'http://activist-birds.picoctf.net:54131/check'

# Example function to test different circuit combinations
def try_circuit(input1, input2, output):
    circuit = [{"input1": input1, "input2": input2, "output": output}]
    payload = {"circuit": circuit}
    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, data=json.dumps(payload), headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        print(f"Success! Response: {result}")
        return result
    else:
        print(f"Failed to submit circuit with input1={input1}, input2={input2}, output={output}")
        return None

# Brute-force approach: Test different combinations of inputs/outputs
for input1 in range(0, 256, 1):  # Testing all possible values for input1 (0-255)
    for input2 in range(0, 256, 1):  # Testing all possible values for input2 (0-255)
        output = 255  # We are setting output to 255, which might trigger the flag
        result = try_circuit(input1, input2, output)
        if result and "flag" in result['status'].lower() and 'flag2' in result['flag'].lower():
            print("Found Flag 2!")
            break
