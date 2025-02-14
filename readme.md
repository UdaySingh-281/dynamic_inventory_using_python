# Dynamic Inventory Generation using Python  

This project demonstrates two approaches for generating a **dynamic Ansible inventory** using Python:  

1. **Using Jinja2 templating** – Dynamically rendering an inventory file from a template.  
2. **Using pure logic** – Writing inventory content directly to a file (`inventory.ini`).  

## Why Dynamic Inventory?  
Dynamic inventories allow flexible infrastructure management by generating host configurations on the fly, making automation more scalable and adaptable.  

## Approaches  

### 1️⃣ Jinja2 Templating Approach  

In this method, we use a **Jinja2 template** (`inventory_template.j2`) to generate the inventory dynamically.  

#### **Example Jinja2 Template (`inventory_template.j2`)**
```jinja2
[webservers]
{% for host in webservers %}
{{ host }} ansible_host={{ webservers[host]['ip'] }} ansible_user={{ webservers[host]['user'] }}
{% endfor %}

[dbservers]
{% for host in dbservers %}
{{ host }} ansible_host={{ dbservers[host]['ip'] }} ansible_user={{ dbservers[host]['user'] }}
{% endfor %}
