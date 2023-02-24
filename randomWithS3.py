import sys
from braket.circuits import Gate
from braket.circuits import Circuit
from braket.devices import LocalSimulator
from braket.aws import AwsDevice

def executeAWS(s3_folder, machine, circuit, shots):
    if machine=="local":
        device = LocalSimulator()
        result = device.run(circuit, int(shots)).result()
        counts = result.measurement_counts
        return counts
        
    device = AwsDevice(machine)

    if "sv1" not in machine and "tn1" not in machine:
        task = device.run(circuit, s3_folder, int(shots), poll_timeout_seconds=5 * 24 * 60 * 60)
    else:
        task = device.run(circuit, s3_folder, int(shots))
    return 'finished'

def random_number_aws(machine, shots):  # noqa: E501
    gate_machines_arn= { "riggeti_aspen8":"arn:aws:braket:::device/qpu/rigetti/Aspen-8", "riggeti_aspen9":"arn:aws:braket:::device/qpu/rigetti/Aspen-9", "riggeti_aspen11":"arn:aws:braket:::device/qpu/rigetti/Aspen-11", "riggeti_aspen_m1":"arn:aws:braket:us-west-1::device/qpu/rigetti/Aspen-M-1", "DM1":"arn:aws:braket:::device/quantum-simulator/amazon/dm1","oqc_lucy":"arn:aws:braket:eu-west-2::device/qpu/oqc/Lucy", "borealis":"arn:aws:braket:us-east-1::device/qpu/xanadu/Borealis", "ionq":"arn:aws:braket:::device/qpu/ionq/ionQdevice", "sv1":"arn:aws:braket:::device/quantum-simulator/amazon/sv1", "tn1":"arn:aws:braket:::device/quantum-simulator/amazon/tn1", "local":"local"}
    ######
    #RELLENAR S3_FOLDER_ID#
    ######
    s3_folder = ('amazon-braket-jorgecs', 'api') #bucket name, folder name
    ######
    circuit = Circuit()
    circuit.h(0)
    circuit.h(1)
    circuit.h(2)
    circuit.h(3)
    circuit.h(4)
    return executeAWS(s3_folder, gate_machines_arn[machine], circuit, shots)



def execute_quantum_task():
    return random_number_aws('sv1',10)



print(execute_quantum_task())
sys.stdout.flush()
