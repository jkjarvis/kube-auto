import argparse
import yaml
import socket
import random

def is_port_open(port):
    if not port:
        raise ValueError("Please give port value")
    ports = port.split(':')
    
    if len(ports) != 2:
        raise ValueError('port must be defined in format: host_port:container_port')
    
    count = len(ports)
    for port in ports:
        port = int(port)
        print(port)
        try:
            # Create a socket object
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                # Try to connect to the specified port
                s.settimeout(1)  # Set a timeout for the connection attempt (in seconds)
                s.connect(("0.0.0.0", port))  # You can change 'localhost' to the specific host if needed
                  # Port is open and accepting connections
        except (ConnectionRefusedError, TimeoutError):
            count -=1 # Port is closed and not accepting connections
    
    return not count

# def get_port(min_port=80, max_port=65535):
#     assigned_port = False

#     while not assigned_port: 
#         port = random.randint(min_port, max_port)
#         if(is_port_open(port)):
#             return port

def remove_none_values(d):
    # Recursively remove keys with None values from the dictionary
    return {k: remove_none_values(v) if type(v) == dict else v for k, v in d.items() if v is not None}

def generate_yaml_file(output_file, requirements):
    is_port_open(requirements.get('port'))
    
    # Create a dictionary with deployment configuration
    deployment_config = {
        "version": "3",
        "services": {
        requirements.service_name if requirements.get("service_name") else "app": {
            "image": requirements.get("image"),
            "ports": [requirements.get("port")],
            "volumes": [f'/tmp:{requirements.get("volume")}'] if requirements.get("volume") else None 
        }
        },
        # Add more deployment options as needed
    }

    # Filter out keys with None values from deployment_config
    filtered_config = remove_none_values(deployment_config)

    # Write the dictionary to a YAML file
    with open(output_file, 'w') as yaml_file:
        yaml.dump(filtered_config, yaml_file, default_flow_style=False)

def main():
    parser = argparse.ArgumentParser(description='Generate YAML file for deployment.')
    parser.add_argument('--image', required=True, help='Docker image name')
    parser.add_argument('--port', help='Port to expose in the container')
    parser.add_argument('--volume', help='Conainer volume to map to')


    args = vars(parser.parse_args())

    output_file = 'deployment.yaml'
    generate_yaml_file(output_file, args)
    print(f'YAML file generated: {output_file}')

if __name__ == "__main__":
    main()
