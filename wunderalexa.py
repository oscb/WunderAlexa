import WunderPython

wunder = WunderPython.WunderClient.create_client(
    "",
    "")


def main():
    wunder.build("")
    lists = wunder.get_lists()
    microsoft = None

    # List of lists
    for i in lists:
        i.get_tasks()
        print("List %s (%d)" % (i.title, len(i.tasks)))
        # print("List %s" % i.title)
        if i.title == 'Microsoft':
            microsoft = i


    # Create a Task
    if microsoft is not None:
        print("Adding task to %s" % microsoft.title)
        newtask = microsoft.create_task("Alexa Test")
        newtask.save()


if __name__ == "__main__":
    main()

