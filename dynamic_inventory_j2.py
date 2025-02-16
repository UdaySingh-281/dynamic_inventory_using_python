import boto3
import os
from jinja2 import Template

# Directory where keys will be stored
KEY_DIR = os.path.expanduser("~/keys/")
os.makedirs(KEY_DIR, exist_ok=True)  # Ensure the directory exists

# jinja2 Template path
TEMPLATE_FILE = "inventory_template.j2"

def get_key_for_instance(instance_id):
    key_file_path = os.path.join(KEY_DIR, f"{instance_id}.pem")

    if os.path.exists(key_file_path):
        print(f"Private key found for {instance_id}: {key_file_path}")
        return key_file_path
    else:
        print(f"No private key found for {instance_id}.")
        key_path = input(f"Enter the full path of the private key for {instance_id} (or press Enter to create a new one): ").strip()

        if key_path and os.path.exists(key_path):
            return key_path

        print(f"Enter the private key for instance {instance_id} (Paste your key and press Ctrl+D when done):")
        private_key_content = []
        while True:
            try:
                line = input()
            except EOFError:  # Pressing Ctrl+D will break the loop
                break
            private_key_content.append(line)

        with open(key_file_path, "w") as key_file:
            key_file.write("\n".join(private_key_content) + "\n")

        os.chmod(key_file_path, 0o600)

        print(f"Private key saved at: {key_file_path}")
        return key_file_path

def get_instances():
    ec2 = boto3.client('ec2', region_name='ap-south-1')
    instances = ec2.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])

    inventory = {}

    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            private_ip = instance.get('PrivateIpAddress', '')

            tags = {tag['Key']: tag['Value'] for tag in instance.get('Tags', [])}
            group_name = tags.get('Ansible_Group')

            instance_name = tags["Name"]
            if instance_name.lower() != 'control-node' or instance_name.lower() != 'master-node':
                print("\n Inside if..... ", instance_name.lower())
                key_path = get_key_for_instance(instance_name)  # Get or create key dynamically
                inventory.setdefault(group_name, []).append((private_ip, key_path))
                print(inventory,"\n")


    # Read the Jinja2 template
    with open(TEMPLATE_FILE) as template_file:
        template = Template(template_file.read())

    # Render the template with the gathered inventory data
    inventory_content = template.render(inventory=inventory)

    with open("inventory.ini", "w") as f:
        f.write(inventory_content)

    print("Inventory file created: inventory.ini")

if __name__ == "__main__":
    get_instances()
