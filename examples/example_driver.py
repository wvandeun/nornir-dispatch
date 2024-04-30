import time

from nornir import InitNornir
from nornir.core.task import Result, Task
from nornir_dispatch import NornirDispatchBaseDriver, registry
from nornir_dispatch.plugins.tasks.dispatcher import dispatcher


class JunosDispatchDriver(NornirDispatchBaseDriver):
    platform = "junos"

    @staticmethod
    def get_config(task: Task):
        print("get_config_junos")
        return Result(changed=True, failed=False, host=task.host, result="get_config_junos")

    @staticmethod
    def reboot(task: Task):
        print("rebooting junos device")
        time.sleep(2)
        return Result(changed=False, failed=False, host=task.host, result="reboot_junos")

class IOSDispatchDriver(NornirDispatchBaseDriver):
    platform = "ios"

    @staticmethod
    def get_config(task: Task):
        print("get_config_ios")
        return Result(changed=True, failed=False, host=task.host, result="get_config_ios")

    @staticmethod
    def reboot(task: Task):
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

    registry.register_tasks(driver=JunosDispatchDriver)
    registry.register_tasks(driver=IOSDispatchDriver)

    nr.run(task=dispatcher, action="get_config")
    result = nr.run(task=dispatcher, action="reboot")

    print(result["device2"][0].failed, result["device2"][0].result)

if __name__ == "__main__":
    main()
