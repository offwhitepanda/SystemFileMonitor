import platform
from plyer import notification

image_path = "warning.png"


def show_notification(title, message):
    notification.notify(
        title=title,
        message=message,
        timeout=10,
        toast=True,
        app_name="File Hash Checker",
        # Specify the path to your image file
        app_icon=None
    )


def send_toast_if_changes_detected(bool_hash_change, num_of_files_changed):
    if "Ubuntu" in platform.version():
        if bool_hash_change:
            print("Warning! - Some file hashes have changed Ⓧ")
        else:
            print("All Clear! - File hashes matched ✔")
    else:
        if bool_hash_change:
            show_notification("Warning!", f"{num_of_files_changed} file hashes have changed Ⓧ")
        else:
            show_notification("All Clear!", "File hashes matched ✔")

