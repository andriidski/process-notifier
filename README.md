# process-notifier
tool to get notified in OS X Notification Center when your commands are finished running from terminal

If you have to run commands in terminal that take a while to complete, you might switch to do some other work, but will not know exactly when those commands are finished

Notifier will update you on completions of any number of processes/commands that you choose to track (flag)

To use:
  - run the python script in a separate terminal window: python notifier.py
  - to have the notifier track your process and notify when its done, just add a --NOTIFY flag to any command ran
  - notifier will send a push notification once the flagged command run is finished!
