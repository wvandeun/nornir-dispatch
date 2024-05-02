import time

from nornir import InitNornir
from nornir.core.task import Result, Task
from nornir_dispatch import registry
from nornir_dispatch.plugins.tasks.dispatcher import dispatcher


def get_config_junos(task: Task):
    print("get_config_junos")
    return Result(changed=True, failed=False, host=task.host, result="get_config_junos")


def get_config_ios(task: Task):
    print("get_config_ios")
    return Result(changed=True, failed=False, host=task.host, result="get_config_ios")


def reboot_junos(task: Task):
    print("rebooting junos device")
    time.sleep(2)
    return Result(changed=False, failed=False, host=task.host, result="reboot_junos")


def reboot_ios(task: Task):
    print("rebooting ios device")
    time.sleep(2)
    return Result(changed=False, failed=False, host=task.host, result="reboot_ios")


def main():
    nr = InitNornir(
        inventory={
            "plugin": "SimpleInventory",
            "options": {
                "host_file": "hosts.yaml"
            }
        }
    )

    registry.register_task(platform="ios", action="get_config", task=get_config_ios)
    registry.register_task(platform="junos", action="get_config", task=get_config_junos)
    registry.register_task(platform="ios", action="reboot", task=reboot_ios)
    registry.register_task(platform="junos", action="reboot", task=reboot_junos)

    nr.run(task=dispatcher, action="get_config")
    result = nr.run(task=dispatcher, action="reboot")
    print(result["device2"][0].failed, result["device2"][0].result)

if __name__ == "__main__":
    main()
