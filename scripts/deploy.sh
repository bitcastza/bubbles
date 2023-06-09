#!/bin/bash
set -e

which ssh-agent || ( apt-get update -y && apt-get install openssh-client -y )
eval $(ssh-agent -s)
echo "$SSH_KEY" | tr -d '\r' | ssh-add - > /dev/null
mkdir ~/.ssh && chmod 700 ~/.ssh

git clone https://gitlab.com/bubbles/ansible ~/ansible
cd ~/ansible

ansible-playbook site.yml --inventory=./hosts --extra-vars="bubbles_key=$BUBBLES_KEY" --ssh-common-args="-C -o ControlMaster=auto -o ControlPersist=60s -o StrictHostKeyChecking=no"
