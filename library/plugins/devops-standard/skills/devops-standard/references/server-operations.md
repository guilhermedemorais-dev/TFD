# Servers and Ansible

Sequence: identify exact host/environment and current state → back up the
affected configuration → bounded approved change → native configuration
validator → approved reload/restart → health and representative service check.
Preserve ownership/permissions and unrelated services. Validate backup location,
integrity and recovery procedure without exposing secrets. Reboot, firewall,
secret rotation and privileged scope changes need explicit human approval.

Ansible: inspect inventory, hosts/limits, roles, collections, lookups, local
actions and privileges first. Use `ansible-lint`, then
`ansible-playbook --syntax-check -i INVENTORY PLAYBOOK`, then authorized
`ansible-playbook --check -i INVENTORY PLAYBOOK --limit TARGET`.
Placeholders identify already-reviewed files/hosts, not commands to run blindly.
Check mode is not a sandbox: modules vary in support; tasks can opt out with
`check_mode: false`, and lookups/plugins may have effects. Audit these before
execution and record skipped/unsupported behavior. `--diff` can reveal secrets;
do not enable without reviewing sensitive tasks/output. A check-mode pass is
not proof of a real host change. Use native validators such as nginx config
tests only when that service actually exists and its command is verified.

Source: [Ansible check/diff mode](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_checkmode.html).
