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

def generate_service_config(service):
        if service.get("ports"):
            is_port_open(service.get('ports'))
        
        service_config = { service["service_name"] : {
            "image": service.get("image"),
            "ports": [service.get("ports")],
            "volumes": [service.get("volumes")] 
        }
        }

        print(service_config)
        return service_config


def generate_yaml_file(output_file, requirements):
    print("keys ",requirements.keys())
    # Create a dictionary with deployment configuration
    deployment_config = {
        "version": "3",
        "services": [
            generate_service_config(requirements[i]) for i in requirements.keys()
        ],
        # Add more deployment options as needed
    }

    # Filter out keys with None values from deployment_config
    filtered_config = remove_none_values(deployment_config)

    # Write the dictionary to a YAML file
    with open(output_file, 'w') as yaml_file:
        yaml.dump(filtered_config, yaml_file, default_flow_style=False)


def prompt_user(yml_config, service_number):
    service_name = input(f"Enter service name (Leave empty if want to use 'service_{service_number}'): ") or f"service_{service_number}"
    image = input(f"Image for service {service_number}: ")
    image_tag = input(f"Image tag for service {service_number} (Leave empty for 'latest'): ") or "latest"
    port_mapping = input(f"Enter port mapping in format 'HostPort : ContainerPort' for service {service_number} (Leave empty if do not want port mapping): ") or None
    volume_mapping = input(f"Enter volume mapping in format 'HostPath : VolumePath' for service {service_number} (Leave empty if do not want volume mapping): ") or None

    yml_config[service_name] = {
        "service_name": service_name,
        "image": f"{image}:{image_tag}",
        "port_mapping": port_mapping,
        "volume_mapping": volume_mapping
    }


def main():
    deployment_yml_config = {}
    number_of_services = int(input("How many services do you want to create ? (Please type in whole number): "))

    for i in range(number_of_services):
        print("i is ",i)
        prompt_user(deployment_yml_config, i+1)

    print(deployment_yml_config)
    output_file = 'deployment.yaml'
    generate_yaml_file(output_file, deployment_yml_config)
    print(f'YAML file generated: {output_file}')

if __name__ == "__main__":
    main()
