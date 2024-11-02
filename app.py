import time
import typer
import hid
import psutil
from enum import Enum
from rich import print as rprint
from typing_extensions import Annotated

app = typer.Typer()

class DeviceListFormat(str, Enum):
    flat= "flat"
    raw= "raw"

@app.command()
def list(format: Annotated[DeviceListFormat, typer.Option("--format", "-f")] = DeviceListFormat.flat):
    if format == DeviceListFormat.flat:
        for device_dict in hid.enumerate():
            name = device_dict['path'].decode("utf-8")
            rprint(f"🔌 [bold blue] {name} [/bold blue]")
            for k,v in device_dict.items():
                rprint("  ", k, ": ", v)
            print("\n")

    if format == DeviceListFormat.raw:
        for device_dict in hid.enumerate():
            print(device_dict)
            print("\n")

@app.command()
def test(device_path: str):
    print("Find device")

    device = hid.device()
    try:
        device.open_path(device_path.encode('utf-8'))
    except Exception as e:
        print("Cannot open connection to the device. It's is usually your user don't have permission to access the device. Please try again with \"sudo\" or root user.")
        print(f"Error: {type(e).__name__}")
        print(f"Message: {str(e)}")
        return
    device.set_nonblocking(1)
    if ping(device):
        print("Device is connected and responding")
        print("Device is not responding or connection failed")
    print("Device connected! Now closing device.")
    device.close()


@app.command()
def monitoring(device_path: str, update_interval:int=1):
    device = hid.device()
    try:
        print(f"Connecting to {device_path}")
        device.open_path(device_path.encode('utf-8'))
    except Exception as e:
        rprint("[bold red]⚠️ Cannot open connection to the device.[/bold red]")
        rprint("Check [blue]device_path[/blue] or user permission. Suggest to run with [blue]sudo[/blue] or [blue]root[/blue] user.")
        print(f"Error: {type(e).__name__}")
        print(f"Message: {str(e)}")
        return

    device.set_nonblocking(1)
    while True:
        temp = get_cpu_temperature()
        if ping(device, [1,temp]):
            print("Device is connected and responding")
            print("Device is not responding or connection failed")
        time.sleep(int(update_interval))
    print("Closing device")
    device.close()


def ping(device, data=[]):
    if len(data) == 0:
        data =  [0,1]
    device.write(data)
    time.sleep(0.1)
    while True:
        response = device.read(64)
        if response:
            print(response)
            return True
        else:
            break

    return False

def get_cpu_temperature():
    """Gets the CPU temperature in degrees Celsius."""
    temps = psutil.sensors_temperatures()
    cpu_temp = None
    for name, entries in temps.items():
        if name == 'coretemp':
            cpu_temp = entries[0].current
    return int(cpu_temp)


if  __name__=="__main__":
    app()
