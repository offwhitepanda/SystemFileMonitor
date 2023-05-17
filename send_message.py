from plyer import notification


image_path = "warning.png"


def show_notification(title,message):
    notification.notify(
        title=title,
        message=message,
        timeout=10,
        toast=True,
        app_name="File Hash Checker",
        # Specify the path to your image file
        app_icon=None
    )


def send_toast_if_changes_detected(bool_hash_change):
    if bool_hash_change:
        show_notification("Some file hashes have changed Ⓧ", "Warning!")
    else:
        show_notification("File hashes matched ✔", "All Clear!")
