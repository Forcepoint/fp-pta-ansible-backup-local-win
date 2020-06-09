# backup-local-win

Zip up the given directory or registry key to the specified folder, retain the specified number of backups, and do so on the given 
frequency via a scheduled task. This role doesn't transfer the zips off the host. This is assumed to be handled afterwards 
by another process. The simplest transfer would be to utilize a secondary drive as the target backup folder so the files 
are moved automatically when the zip is created.

For information about PTA and how to use it with this Ansible role please visit https://github.com/Forcepoint/fp-pta-overview/blob/master/README.md

## Requirements

Python37 must be installed.

## Role Variables

REQUIRED
* backup_local_win_name: The name for the backup. This must be unique on the host so there's no collision between jobs. 
  Alphanumeric with underscores is recommended. No spaces.
* backup_local_win_target: The folder or registry key to zip up. Ensure there's no trailing slashes. Registry targets
  should begin with one of the following root keys: HKLM, HKCU, HKCR, HKU, HKCC (see the KeyName parameter 
  https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/reg-export).
* backup_local_win_destination: The folder in which the zip is to be placed. Ensure there's no trailing slashes.

OPTIONAL
* backup_local_win_retention_number: The number of backups to retain. 0 means infinite (no cleanup). Defaults to 10.
* backup_local_win_days_of_week: A comma separated list of the days of the week to run the job. Defaults to Mon-Fri.
* backup_local_win_time: The time of day to run the job. Uses a 24 based time (HH:MM:SS).

## Dependencies

None

## Example Playbook

This performs a backup a folder, Monday, Wednesday, and Friday at 6 AM, retaining the 10 most recent backups.

    - hosts: servers
      vars:
        backup_local_win_name: "App Config"
        backup_local_win_target: "C:\Program Files (x86)\App\Config"
        backup_local_win_destination: D:\backups
        backup_local_win_time: "06:00:00"
        backup_local_win_days_of_week: monday,wednesday,friday
      roles:
         - role: backup-local-win

This performs a backup a registry key, Monday, Wednesday, and Friday at 6 AM, retaining the 10 most recent backups.

    - hosts: servers
      vars:
        backup_local_win_name: "Reg Config"
        backup_local_win_target: "HKLM\SOFTWARE\Python"
        backup_local_win_destination: D:\backups
        backup_local_win_time: "06:00:00"
        backup_local_win_days_of_week: monday,wednesday,friday
      roles:
         - role: backup-local-win

## License

BSD-3-Clause

## Author Information

Jeremy Cornett <jeremy.cornett@forcepoint.com>
