#!/bin/sh

set -e

envsubst < /etc/nginx/default.conf.tpl > /etc/nginx/conf.d/default.conf
nginx -g 'daemon off;'

#  the first command takes the content of the NGINX configuration template file /etc/nginx/default.conf.tpl, performs environment variable substitution, and writes the substituted content to the NGINX configuration file /etc/nginx/conf.d/default.conf. This is often used in container environments to dynamically configure NGINX based on environment variables at runtime. we define environment variable in our Dockerfile.

# the second command starts NGINX with the specified global configuration: daemon off;: This directive instructs NGINX not to daemonize itself, meaning it runs in the foreground and keeps the process attached to the terminal. This is necessary in environments like Docker containers, where the main process is expected to stay in the foreground. If NGINX were to daemonize itself (the default behavior), Docker would mistakenly believe the container has stopped immediately after starting NGINX. -g flag means global configuration and is mandatory.


# In NGINX, the conf.d directory typically holds additional configuration files that are included in the main NGINX configuration file (nginx.conf). This directory structure is commonly used to organize NGINX configurations into smaller, more manageable files.

# The .tpl extension in the file default.conf.tpl typically indicates that the file is a template file. In the context of NGINX configuration, a template file is a file that contains placeholders or variables that will be replaced with actual values during runtime. Template files are often processed using tools like envsubst or template engines to perform variable substitution. These tools parse the template file, replace the placeholders with actual values from the environment or configuration, and produce the final configuration file.
